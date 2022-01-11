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
from calculation.OBV import calculateOBV
from simulation.SimulationEMAs import simulation
from simulation.SimulationOBV import testOBVstrategy
from calculation.BollingerBands import calculateBollingerBands

app = Flask(__name__)
api = Api(app)

class DecisionRsponse(Resource):
    def get(self):
        return {"status": "Please use POST instead"}

    def post(self):
        calculateBollingerBands(request)
        #print(request.json['array1m'][49])
        #print(request.json['array5m'][49])
        print(request.json['array15m'][49])
        print(request.json['array15m'][48])
        print(request.json['array15m'][47])
        print(request.json['array15m'][46])
        #print(request.json['array30m'][49])
        #print(request.json['array1h'][49])
        #print(request.json['array1d'][49])
        #klines = np.array(request.json['klines'])
        #df = createDataFrame(klines, False)
        #df = calculateDMI(df)

        #print(df)
        return {"status": "OK"}

api.add_resource(DecisionRsponse, "/decision")

def getKLines(apiManager, symbol, interval):
    data = apiManager.get_historical_klines(
        symbol=symbol,
        interval=interval,
        start_str=1638345491000, # 1 grudnia
        #start_str=1635780897000
        #start_str=1636349289000,
        #end_str=1637671915000
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

    testOBVstrategy(df)
    #testDMIstrategy(df)

if __name__ == '__main__':
    app.run()
