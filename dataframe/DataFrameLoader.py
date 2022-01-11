from datetime import datetime
import pandas as pd

def createDataFrameFromHistoricalData(data):

    OPEN_PRICE_INDEX = 1
    HIGH_PRICE_INDEX = 2
    LOW_PRICE_INDEX = 3
    CLOSE_PRICE_INDEX = 4
    VOLUME_INDEX = 5
    QUOTE_VOLUME_INDEX = 7
    TAKER_BUY_VOLUME_INDEX = 9
    TAKER_BUY_QUOTE_VOLUME_INDEX = 10

    dict = []
    onBalanceQuoteVolume = 0

    for i in range(len(data)):
        element = data[i]
        closeTime = int(element[0]) / 1000
        volume = float(element[VOLUME_INDEX])
        quoteVolume = float(element[QUOTE_VOLUME_INDEX])
        takerBuyVolume = float(element[TAKER_BUY_VOLUME_INDEX])
        takerBuyQuoteVolume = float(element[TAKER_BUY_QUOTE_VOLUME_INDEX])
        close = float(element[CLOSE_PRICE_INDEX])
        open = float(element[OPEN_PRICE_INDEX])
        low = float(element[LOW_PRICE_INDEX])
        high = float(element[HIGH_PRICE_INDEX])
        hlc3 = float((high + low + close) / 3.0)

        demandQuoteVolume = takerBuyQuoteVolume
        supplyQuoteVolume = quoteVolume - demandQuoteVolume
        onBalanceQuoteVolume = onBalanceQuoteVolume + demandQuoteVolume - supplyQuoteVolume

        dict.append({
            'closeTime': datetime.fromtimestamp(closeTime).strftime('%Y-%m-%d %H:%M:%S'),
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'typicalPrice': hlc3,
            'onBalanceQuoteVolume': onBalanceQuoteVolume
        })

    dataFrame = pd.DataFrame(dict)
    dataFrame['closeTime'] = pd.to_datetime(dataFrame['closeTime'])
    return dataFrame

def createDataFrame(data):

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