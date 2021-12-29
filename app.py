import numpy as np
import pandas as pd
import pandas_ta as ta
from flask import Flask, request
from flask_restful import Api, Resource
from simulation.SimulationADX import testDMIstrategy
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import BinanceRestApiManager
from datetime import datetime
from dataframe.DataFrameLoader import createDataFrame, createDataFrameFromHistoricalData
from calculation.DMI import calculateDMI
from calculation.FourEmas import calculate4Emas
from simulation.SimulationEMAs import simulation

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
        start_str=1636349289000,
        end_str=  1636995289000
        #end_str=1636475289000
    )

    return data

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calculate')
def calculate():
    apiManager = BinanceRestApiManager('api_key', 'api_secret', exchange="binance.com")
    pd.set_option('display.max_columns', None)
    print('Loading Klines...')
    data = np.array(getKLines(apiManager, "ETHUSDT", '5m'))
    print('Loading Klines... DONE')
    df = createDataFrameFromHistoricalData(data)

    testDMIstrategy(df)

if __name__ == '__main__':
    app.run()
