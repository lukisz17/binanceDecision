import numpy as np
import pandas as pd
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
        klines = request.json['klines']
        print(klines[49]['closeTimeString'])
        return {"status": "OK"}

api.add_resource(DecisionRsponse, "/decision")

def getKLines(apiManager, symbol, interval):
    data = apiManager.get_klines(
        symbol=symbol,
        interval=interval,
        limit=200
    )

    return data


def createDataFrame(data):
    minPrice = 1000000
    maxPrice = 0

    OPEN_PRICE_INDEX = 1
    HIGH_PRICE_INDEX = 2
    LOW_PRICE_INDEX = 3
    CLOSE_PRICE_INDEX = 4
    VOLUME_INDEX = 5
    QUOTE_VOLUME_INDEX = 7
    TAKER_BUY_VOLUME_INDEX = 9
    TAKER_BUY_QUOTE_VOLUME_INDEX = 10

    dict = []

    MFI_LEN = 10  # 14

    for i in range(MFI_LEN, len(data)):

        element = data[i]
        closeTime = int(element[0]) / 1000
        volume = float(element[VOLUME_INDEX])
        takerBuyVolume = float(element[TAKER_BUY_VOLUME_INDEX])
        close = float(element[CLOSE_PRICE_INDEX])
        open = float(element[OPEN_PRICE_INDEX])
        low = float(element[LOW_PRICE_INDEX])
        high = float(element[HIGH_PRICE_INDEX])

        demandMoneyFlow = 0
        supplyMoneyFlow = 0

        for j in range(i - MFI_LEN + 1, i + 1):
            elem = data[j]
            elemPrev = data[j - 1]

            typicalPrice = (float(elem[CLOSE_PRICE_INDEX]) + float(elem[LOW_PRICE_INDEX]) + float(
                elem[HIGH_PRICE_INDEX])) / 3

            if typicalPrice < minPrice:
                minPrice = typicalPrice
            if typicalPrice > maxPrice:
                maxPrice = typicalPrice

            # ---
            vol = float(elem[VOLUME_INDEX])
            demandVol = float(elem[TAKER_BUY_VOLUME_INDEX])
            supplyVol = vol - demandVol

            demandMoneyFlow += demandVol * typicalPrice
            supplyMoneyFlow += supplyVol * typicalPrice

        demandSupplyMoneyRatio = 0

        if supplyMoneyFlow > 0:
            demandSupplyMoneyRatio = demandMoneyFlow / supplyMoneyFlow
        else:
            demandSupplyMoneyRatio = 0

        MFI_SD = (100 - (100 / (1 + demandSupplyMoneyRatio)))

        dict.append({
            'closeTime': datetime.fromtimestamp(closeTime).strftime('%Y-%m-%d %H:%M:%S'),
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'MFI_SD': MFI_SD,
            'typicalPrice': typicalPrice
        })

    dataFrame = pd.DataFrame(dict)
    dataFrame['closeTime'] = pd.to_datetime(dataFrame['closeTime'])
    return dataFrame, minPrice, maxPrice

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/calculate')
def calculate():
    apiManager = BinanceRestApiManager('api_key', 'api_secret', exchange="binance.com")
    data = np.array(getKLines(apiManager, "ETHUSDT", '1m'))
    df, minPrice, maxPrice = createDataFrame(data)
    return str(df.size)

if __name__ == '__main__':
    app.run()
