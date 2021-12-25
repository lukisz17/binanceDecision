import numpy as np
import pandas as pd
import pandas_ta as ta
from flask import Flask, request
from flask_restful import Api, Resource
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import BinanceRestApiManager
from datetime import datetime
from dataframe.DataFrameLoader import createDataFrame, createDataFrameFromHistoricalData
from calculation.DMI import calculateDMI
from simulation.Simulation import simulation

app = Flask(__name__)
api = Api(app)

class DecisionRsponse(Resource):
    def get(self):
        return {"status": "Please use POST instead"}

    def post(self):
        klines = np.array(request.json['klines'])
        df = createDataFrame(klines, False)
        df = calculateDMI(df)

        print(df)
        return {"status": "OK"}

api.add_resource(DecisionRsponse, "/decision")

def getKLines(apiManager, symbol, interval):
    data = apiManager.get_historical_klines(
        symbol=symbol,
        interval=interval,
        start_str=1640028590000
    )

    return data

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calculate')
def calculate():
    apiManager = BinanceRestApiManager('api_key', 'api_secret', exchange="binance.com")
    print('Loading Klines...')
    data = np.array(getKLines(apiManager, "XRPUSDT", '1m'))
    print('Loading Klines... DONE')
    df = createDataFrameFromHistoricalData(data)
    df = calculateDMI(df)
    pd.set_option('display.max_columns', None)
    df = df[df['PSARDMP'].notnull()]

    maxProfit = 0;
    adxBuy = 1
    adxSell = 1
    totalProfit = 0

    for i in range(1, 50):
        print(i, maxProfit)
        for j in range(1, 50):
            subDf = df[['DMP_BUY', 'DMN_BUY', 'DMP_SELL', 'DMN_SELL', 'ADX', 'hlc3']]
            array = subDf.to_numpy()
            totalProfit = simulation(array, ADX_BUY=i, ADX_SELL=j)
            if totalProfit > maxProfit:
                maxProfit = totalProfit
                adxBuy = i
                adxSell = j

    print('TOTAL PROFIT ', maxProfit, adxBuy, adxSell)
    return str(maxProfit)

if __name__ == '__main__':
    app.run()
