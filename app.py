import numpy as np
import pandas as pd
import pandas_ta as ta
from flask import Flask, request
from flask_restful import Api, Resource
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import BinanceRestApiManager
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class DecisionRsponse(Resource):
    def get(self):
        return {"status": "Please use POST instead"}

    def post(self):
        klines = np.array(request.json['klines'])
        df = createDataFrame(klines, False)
        adx = ta.adx(close=df['close'], high=df['high'], low=df['low'])
        df['DMN_14_24'] = ta.ema(adx['DMN_14'], length=24)  # to 14 i  24 musi byc parametrem
        df2 = ta.psar(df['DMN_14_24'], df['DMN_14_24'])  # tutaj to tez musza byc parametry
        df['PSARl_0.02_0.2'] = df2['PSARl_0.02_0.2']
        print(df)
        return {"status": "OK"}

api.add_resource(DecisionRsponse, "/decision")

def getKLines(apiManager, symbol, interval):
    data = apiManager.get_klines(
        symbol=symbol,
        interval=interval,
        limit=200
    )

    return data


def createDataFrame(data, isColab):

    dict = []

    for i in range(len(data)):

        element = data[i]
        closeTime = int(element['closeTime']) / 1000
        volume = float(element['volume'])
        takerBuyVolume = float(element['takerBuyBaseAssetVolume'])
        close = float(element['close'])
        open = float(element['open'])
        low = float(element['low'])
        high = float(element['high'])
        hlc3 = float((high + low + close)/3.0)

        dict.append({
            'closeTime': datetime.fromtimestamp(closeTime).strftime('%Y-%m-%d %H:%M:%S'),
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'hlc3': hlc3
        })

    dataFrame = pd.DataFrame(dict)
    dataFrame['closeTime'] = pd.to_datetime(dataFrame['closeTime'])
    return dataFrame

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calculate')
def calculate():
    apiManager = BinanceRestApiManager('api_key', 'api_secret', exchange="binance.com")
    data = np.array(getKLines(apiManager, "ETHUSDT", '1m'))
    df = createDataFrame(data, False)
    print(df)
    return str(df.size)

if __name__ == '__main__':
    app.run()
