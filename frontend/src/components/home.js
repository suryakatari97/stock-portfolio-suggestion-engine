import React, { Component } from 'react';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import InputAdornment from '@material-ui/core/InputAdornment';
import FormControl from '@material-ui/core/FormControl';
import Button from '@material-ui/core/Button';
import FormLabel from '@material-ui/core/FormLabel';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import Checkbox from '@material-ui/core/Checkbox';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from "axios";
import swal from 'sweetalert';
import { Redirect } from 'react-router';
import { Pie } from 'react-chartjs-2';
import Navbar from "./Navbar";
import {
    Row,
    Col,
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardFooter
} from "reactstrap";
import {ResponsiveContainer, ComposedChart, Line, Area,XAxis, YAxis, CartesianGrid, Tooltip, Legend} from  'recharts';


 class home extends Component {
    constructor(props) {
    super(props);
    this.state = {amount: 5000, strategies: [], loading: false, stocks : [],comName :[], value :[], linedata :[]};
  }

  changeAmount = e => {
    this.setState({amount: e.target.value});
  };

  changeStrategy  = strategy => event => {
    if(event.target.checked) {
      this.setState({strategies: this.state.strategies.concat(strategy)});
    } else {
      this.setState({strategies: this.state.strategies.filter( s => s !== strategy)});
    }
  };

   handleSubmit = () => {
       const data = {
           amount : this.state.amount,
           strategyList : this.state.strategies
       }

    this.setState({"loading": true});
     axios("/suggestStocks", {
      method: "post",
      data: data,
    })
      .then((response) => {
          console.log("This is response",response.data);
          let name = [];
          let val = [];
          response.data.pie_chart_data.forEach((item) => {
                     name.push(item.name);
                     val.push(item.value)
                 });
        this.setState({
        stocks: response.data.allocation,
        linedata:response.data.weekly_trend,
        comName:name,
        value:val,
        "loading": false
      })
        console.log("This is stocks",this.state.stocks);
      })
      .catch((error) => {
        console.log("add project not 2xx response");
      });
  };

  getLines = ()=> {
    let lines = [];
    let colors = ["#6a0dad", "#2E86C1", "#EC7063" , "#B03A2E", "#21618C", "#F4D03F"];
    if(!this.state.linedata || this.state.linedata.length === 0) {
      return lines;
    }
    let count = 0;
    for (let [key, value] of Object.entries(this.state.linedata[0])) {
      if(key !== "Total Portfolio" && key !== "name") {
        lines.push(<Line type='monotone' key={key} dataKey={key} stroke={colors[count]} activeDot={{ r: 8 }}/>)
        count++;
      }
    }
    return(lines);
  };
    render() {
        let stockstable;
        // if (this.state.stocks != undefined) {
        //     var stocksdata = this.state.stocks
        //     console.log(stocksdata);
        //     //stockstable = []
        //     for(let i=0; i<stocksdata.length; i++){
        //         let stock = stocksdata[i]
        //         stockstable.push(
        //             <tr>
        //                  <td>{stock.price}</td>
        //                  <td>
        //                  </td>
        //             </tr>
        //         )
        //     }
        // }
        const data = {
            labels: this.state.comName,
            datasets: [
              {
                label: 'Total Money Spent($)',
                data: this.state.value,
                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#f8981c","#a9014b","#3f0f3e"]
              }
            ]
          };
        const options = {
            title: {
              display: true,
              text: 'Total Money Spent($)'
            }
          };
        
        if (this.state.stocks != undefined) {
            
            stockstable = this.state.stocks.map((stock) => {
                console.log("This is stock", stock);
      return (
        <tr>
                        <td>{stock.symbol}</td>
                        <td>{stock.companyName}</td>
                        <td>{stock.numOfStocks}</td>
                        <td>{stock.latestPrice.toFixed(2)}</td>
                        <td>{stock.totalHoldingValue.toFixed(2)}</td>
                        <td>{stock.strategy}</td>
                        
                    </tr>
      )
    })
        }
        const names = [
      "Ethical Investing",
      "Growth Investing",
      "Index Investing",
      "Quality Investing",
      "Value Investing"
    ];
        return (
            <div>
                <Navbar/>
                <div className="container">
            <FormControl fullWidth className={""}>
            {/* <InputLabel htmlFor="standard-adornment-amount">Enter Investment Amount</InputLabel> */}
            <h4>Enter Investment Amount</h4>
            <Input
              type="number"
              id="standard-adornment-amount"
              value={this.state.amount}
              onChange={this.changeAmount}
              startAdornment={<InputAdornment position="start">$</InputAdornment>}
            />
          </FormControl>
          {this.state.amount < 5000 &&
          <FormHelperText className={"fix-width"} error={true}>Minimum amount should be $5000</FormHelperText>}
          {this.state.amount >= 5000 &&
          <div className="fix-width"> </div>}

            <div className={"form-element"}>
                <div className="fixwidth"> </div>
          <FormControl component="fieldset" className={""}>
            <FormLabel component="legend">Pick one or two investment Strategies</FormLabel>
            <FormGroup>
                  {names.map(name => (
                    <FormControlLabel
                      key={name}
                      control={<Checkbox color={"primary"} checked={this.state.strategies.indexOf(name) > -1}
                                         onChange={this.changeStrategy(name)} value={name} />}
                      label={name}
                    />
                  ))}
            </FormGroup>
            {this.state.strategies.length > 2 &&
            <FormHelperText className={"fix-width"} error={true}>Maximum two strategies can be picked at a time.</FormHelperText>}
            {this.state.strategies.length <= 2 &&
            <div className="fix-width"> </div>}
          </FormControl>

        </div>
                     <Button disabled={this.state.strategies.length < 1 || this.state.strategies.length > 2
        || this.state.loading || this.state.amount<5000}
                variant="contained" color="primary" className={"form-element submit-button"}
                onClick={this.handleSubmit}>
          {this.state.loading && <CircularProgress size={24} />}
          Submit
        </Button>


                        <Row>
        <div>
    {this.state.stocks.length > 0 ? (
         <table className="table table-striped table-bordered lead">
                                            <thead>
                                                <tr>
                                                    <th>Symbol</th>
                                                    <th>Company Name</th>
                                                    <th>No.of Stocks</th>
                                                    <th>Latest Price</th>
                                                    <th>Holding Value</th>
                                                    <th>Strategy</th>
                                                </tr>
                                            </thead>
                                            <tbody>{stockstable}</tbody>
                                        </table>
        
    )
     : ('')}
</div> 
</Row>
<Row>
    <Col>
    {this.state.stocks.length > 0 ? (
        <Card className="card-chart">
                    <CardHeader>
                        <h5 className="card-category">Store</h5>
                      <CardTitle tag="h3">
                          <i className="tim-icons icon-bell-55 text-info" /> Expenditure</CardTitle>
                      {/* <p className="card-category">Money spent</p> */}
                    </CardHeader>
                    <CardBody>
                      <Pie ref="chart" data={data} options={options}/>
                    </CardBody>
                    <CardFooter>
                      <div className="stats">
                        <i className="fas fa-bars" /> Category wise
                        Expenditure
                      </div>
                    </CardFooter>
                  </Card>

    ) : ('')}
    </Col>
    <Col>
    {this.state.stocks.length > 0 ? (
        <ResponsiveContainer width={"100%"} height={400}>
        <ComposedChart data={this.state.linedata}
                       margin={{top: 20, right: 20, bottom: 20, left: 20}}>
          <CartesianGrid strokeDasharray="3 3"/>
          <XAxis dataKey="name"/>
          <YAxis />
          <Tooltip/>
          <Legend/>
          <Area type='monotone' dataKey='Total Portfolio' fill='#F2F4F4' stroke='#145A32' />
          {this.getLines()}
        </ComposedChart>
      </ResponsiveContainer>

    ) : ('')}
    
    </Col>
</Row>

                </div>

              
            </div>
        )
    }
}

export default home;
