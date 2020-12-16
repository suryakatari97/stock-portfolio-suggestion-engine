import requests
from datetime import datetime, timedelta
#"TXN"
# "AMZN", "GOOGL"
#"ECL", "NEE"
# "JNJ"
stocks = {
    'Ethical Investing': ["TSLA", "CRM", "FLR"],
    'Growth Investing': ["AAPL", "FB", "MSFT"],
    'Index Investing': [ "SPY", "VOO", "IVV"],
    'Quality Investing': ["TCS", "ABBV", "AVGO"],
    'Value Investing': [ "DIS", "JPM", "VZ"]
}

companyNames = {
    "FNILX":"Fidelity Zero large cap index",
    "SPY" : "SPDR S&P 500 ETF",
    "VOO" : "Vanguard S&P 500 ETF",
    "IVV" : "iShare core S&P 500 ETF",
    "SWPPX" : "Schwab S&P 500 Index Fund",
    "TCS"  :"Tata consulting services",
    "ABBV" :"Abbvie",
    "AVGO" :"Broadcom",
    "ECL"  :"Ecolab",
    "NEE"  :"NextEra energy",
    "AAPL" : "Apple Inc",
    "CRM"  : "Salesforce",
    "TSLA" : "Tesla Inc",
    "ADBE" : "Adobe Inc",
    "AAPL" : "Apple",
    "FLR"  : "Fluor",
    "TXN"  : "Texas Instruments",
    "BRK.B"  : "Berkshire Hathaway class B",
    "DIS" : "Walt Disney",
    "VZ" : "Verizon",
    "JNJ" : "Johnson and Johnson",
    "JPM" : "JP Morgan chase and co",
    "HNNMY" : "Hennes and Mauritz AB",
    "FB"   : "Facebook",
    "MSFT" : "Microsoft",
    "AMZN" : "Amazon",
    "GOOGL" : "Alphabet class A",
    "ECC": "Eagle Point CR/COM",
    "AMD": "Advanced Micro Devices, Inc",
    "VOO": "VANGUARD IX FUN/S&P 500",
    "VTI": "VANGUARD IX FUN",
    "ILTB": "ISHARES TR",
    "NVDA": "NVIDIA Corporation",
    "MU": "Micron Technology, Inc",
    "CSCO": "Cisco Systems, Inc",
    "INTC": "Intel Corporation",
    "BABA": "Alibaba Group Holding",
    "GE": "General Electric Company"
}

apikey="b20d42fa67bbc5730606055df79afa8f"
root_url ='https://financialmodelingprep.com/api/v3/'


def get_price_details(strategyList):
    price_details = {}
    companies = convertToString(strategyList)
    # for currStrategy in strategyList:
    #     companies = companies + ',' + ','.join(stocks[currStrategy])

    priceValues = request_price_Values(companies)
    if priceValues.status_code != 200:
        Exception("Error in getting real time prices")
        return price_details

    priceValues = priceValues.json()
    for companyItem in priceValues['companiesPriceList']:
        price_details[companyItem['symbol']] = {"price": companyItem['price'], "strategy": get_strategy(companyItem['symbol'])}

    return price_details

def request_price_Values(companies):
    real_time_price_url = 'stock/real-time-price/'
    return requests.get(root_url + real_time_price_url + companies + "?apikey=" + apikey)

def request_historical_data(symbol, filter_date):
    historical_price = 'historical-price-full/'
    full_url = root_url + historical_price + symbol + filter_date +  "&apikey=" + apikey
    #print(full_url)
    return requests.get(full_url)

def convertToString(strategyList):
    companies = ''
    for currStrategy in strategyList:
        companies = companies + ',' + ','.join(stocks[currStrategy])
    return companies

def get_date(delta):
    format = '%Y-%m-%d'
    return (datetime.today() - timedelta(days=delta)).strftime(format)

def suggest_stocks(amount, strategyList):

    #allocated_stocks = {}
    resp_allocated_stocks = []
    param_allocated_stocks = {}
    pie_chart_data = []

    price_details = get_price_details(strategyList)
    price_details = {key: value for key, value in sorted(price_details.items(), key=lambda priceItem: priceItem[1]["price"], reverse=True)}

    remaining_price = 0
    amount_per_stock = 0
    if len(price_details) > 0:
        amount_per_stock = amount / len(price_details)

    for symbol, data in price_details.items():
        stock_price = float(data.get("price"))
        number_of_stocks = int((amount_per_stock + remaining_price)/stock_price)
        remaining_price = (remaining_price + amount_per_stock) - (number_of_stocks * stock_price)
        param_allocated_stocks[symbol] = {"stocks": number_of_stocks, "price": stock_price, "strategy": data.get("strategy")}
        resp_allocated_stocks.append({"symbol": symbol, "companyName": companyNames[symbol], "totalHoldingValue": number_of_stocks * stock_price ,"numOfStocks": number_of_stocks, "latestPrice": stock_price, "strategy": data.get("strategy")})
        pie_chart_data.append({"name": symbol, "value": number_of_stocks * stock_price})

    return {"allocation": resp_allocated_stocks, "weekly_trend": get_history(strategyList, param_allocated_stocks),
            "pie_chart_data": pie_chart_data}


def get_history(strategyList, allocated_stocks):
    # "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL,MSFT?from=2019-12-10&to=2019-12-12"

    history_data = []
    
    #start_date = (datetime.today() - timedelta(days=8)).strftime('%Y-%m-%d')
    #end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = get_date(8)
    end_date = get_date(1)
    
    filter_date = '?from={}&to={}'.format(start_date, end_date)

    for strategy in strategyList:
        for symbol in stocks.get(strategy):
            response = request_historical_data(symbol, filter_date)
            if response.status_code != 200:
                Exception("API Error")
            response_json = response.json()
            #print(response_json)
            symbol = response_json['symbol']
            # history_data[symbol] = {}

            for trend in response_json['historical']:
                date = trend['date']
                filtered_history = (history_data.index(x) for x in history_data if x['name'] == date)
                history_idx = next(filtered_history, None)
                if history_idx is None:
                    hist_elem = {'name': date}
                    history_data.append(hist_elem)
                    history_idx = history_data.index(hist_elem)

                final_allotment = trend['close'] * allocated_stocks.get(symbol).get("stocks")
                history_data[history_idx][symbol] = final_allotment
                if history_data[history_idx].get("Total Portfolio") is None:
                    history_data[history_idx]["Total Portfolio"] = final_allotment
                else:
                    history_data[history_idx]["Total Portfolio"] += final_allotment

    # add today's portfolio value to weekly trend
    hist_elem = {'name': 'Latest Value'}
    history_data.append(hist_elem)
    history_idx = history_data.index(hist_elem)
    total_value = 0
    for symbol, data in allocated_stocks.items():
        calculated_price =  data.get("price") * data.get("stocks")
        history_data[history_idx][symbol] =  calculated_price
        total_value += calculated_price
    history_data[history_idx]["Total Portfolio"] = total_value
    return history_data


def get_strategy(symbol):
    for stock_strategy, symbols in stocks.items():
        if symbol in symbols:
            return stock_strategy
