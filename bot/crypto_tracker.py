import requests


def curs_btc():
    response = requests.get(
            'https://blockchain.info/ticker',
        ) 

    curs_btc =  int(response.json()['RUB']['15m'])
    return curs_btc




def curs_usd():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
        curr = ["RUB=X"]
        curr_data = "https://query1.finance.yahoo.com/v7/finance/quote?symbols={}".format(",".join(curr))
        curr_info = requests.get(curr_data, headers=headers).json()["quoteResponse"]
        data = {}
        for i in curr_info['result']:
            data[i["shortName"]] = {
                'price': i['regularMarketPrice']
            }
        for i in data:
            usd = data[i]['price']
            return usd
    except Exception as err:
            print(err)