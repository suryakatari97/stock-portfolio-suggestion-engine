import requests
from datetime import datetime, timedelta

stocks = {
    'Ethical Investing': ["AAPL", "TSLA", "ADBE"],
    'Growth Investing': ["OXLC", "ECC", "AMD"],
    'Index Investing': ["VOO", "VTI", "ILTB"],
    'Quality Investing': ["NVDA", "MU", "CSCO"],
    'Value Investing': ["INTC", "BABA", "GE"]
}

apikey="8df9d2285918ef03c05b5f216583a6cc"
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
    return requests.get(root_url + historical_price + symbol + filter_date +  "&apikey=" + apikey)

def convertToString(strategyList):
    companies = ''
    for currStrategy in strategyList:
        companies = companies + ',' + ','.join(stocks[currStrategy])
    return companies

def suggest_stocks(amount, strategyList):

    allocated_stocks = {}
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
        allocated_stocks[symbol] = {"stocks": number_of_stocks, "price": stock_price, "strategy": data.get("strategy")}
        pie_chart_data.append({"name": symbol, "value": number_of_stocks * stock_price})

    return {"allocation": allocated_stocks, "weekly_trend": get_history(strategyList, allocated_stocks),
            "pie_chart_data": pie_chart_data}


def get_history(strategyList, allocated_stocks):
    # "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL,MSFT?from=2019-12-10&to=2019-12-12"

    #history_data = {"total": {}}
    history_data = []
    
    start_date = (datetime.today() - timedelta(days=8)).strftime('%Y-%m-%d')
    end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    filter_date = '?from={}&to={}'.format(start_date, end_date)

    for strategy in strategyList:
        for symbol in stocks.get(strategy):
            response = request_historical_data(symbol, filter_date)
            if response.status_code != 200:
                Exception("API Error")
            response_json = response.json()
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

                # history_data[symbol][date] = final_allotment
                history_data[history_idx][symbol] = final_allotment
                if history_data[history_idx].get("Total Portfolio") is None:
                    history_data[history_idx]["Total Portfolio"] = final_allotment
                else:
                    history_data[history_idx]["Total Portfolio"] += final_allotment

                # if history_data["total"].get(date) is None:
                #     history_data["total"][date] = final_allotment
                # else:
                #     history_data["total"][date] += final_allotment

    # add today's portfolio value to weekly trend
    hist_elem = {'name': 'Latest Value'}
    history_data.append(hist_elem)
    history_idx = history_data.index(hist_elem)
    portfolio_value = 0
    for symbol, data in allocated_stocks.items():
        history_data[history_idx][symbol] = data.get("stocks") * data.get("price")
        # history_data.get(symbol)["latest"] = data.get("stocks") * data.get("price")
        portfolio_value += data.get("stocks") * data.get("price")
    # date_today = (datetime.today()).strftime('%Y-%m-%d')
    # history_data["total"]["latest"] = portfolio_value
    history_data[history_idx]["Total Portfolio"] = portfolio_value

    return history_data


def get_strategy(symbol):
    for stock_strategy, symbols in stocks.items():
        if symbol in symbols:
            return stock_strategy
