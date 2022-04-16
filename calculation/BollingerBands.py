import numpy as np
import pandas as pd
import pandas_ta as ta
from dataframe.DataFrameLoader import createDataFrame

def calculateBollingerBands(request):

    array1m = request.json['array1m']
    array5m = request.json['array5m']
    array15m = request.json['array15m']
    array30m = request.json['array30m']
    array1h = request.json['array1h']
    array1d = request.json['array1d']

    calculateBB(array1m, 20)
    calculateBB(array5m, 10)
    calculateBB(array5m, 20)
    calculateBB(array5m, 30)
    calculateBB(array15m, 20)
    calculateBB(array15m, 30)
    calculateBB(array30m, 20)
    calculateBB(array30m, 24)
    calculateBB(array30m, 30)
    calculateBB(array1h, 24)
    calculateBB(array1h, 30)
    calculateBB(array1d, 5)
    calculateBB(array1d, 7)

def calculateBB(array, maLength):
    data = np.array(array)
    df = createDataFrame(data)

    bb_1 = ta.bbands(close=df['close'], length=maLength, std=1, mamode="sma")
    bb_2 = ta.bbands(close=df['close'], length=maLength, std=2, mamode="sma")

    df2 = df[['closeTime', 'close']]
    df2['bbpB_' + str(maLength) + '_1'] = bb_1['BBP_' + str(maLength) + '_1.0']
    df2['bbpB_' + str(maLength) + '_2'] = bb_2['BBP_' + str(maLength) + '_2.0']
    df2['ma'] = bb_2['BBM_' + str(maLength) + '_2.0']

    stoch_k = 14
    stoch_d = 5
    stoch_smooth_k = 5
    stochastic = ta.stoch(close=df['close'], high=df['high'], low=df['low'], k=stoch_k, d=stoch_d, smooth_k=stoch_smooth_k)
    df2['STOCHk'] = stochastic['STOCHk_' + str(stoch_k) + '_' + str(stoch_d) + '_' + str(stoch_smooth_k)]
    df2['STOCHd'] = stochastic['STOCHd_' + str(stoch_k) + '_' + str(stoch_d) + '_' + str(stoch_smooth_k)]
    sig = ta.xsignals(df2['STOCHk'], df2['STOCHd'], df2['STOCHd'], above=True)

    df2['TS_Entries'] = sig['TS_Entries']  # 1 = oversold crossover just happened
    df2['TS_Exits'] = sig['TS_Exits']  # 1 = overbought crossover just happened
    df2 = df2.drop(['close'], axis=1)


    print(df2.to_json(orient="records"))


    return df2[df2['ma'].notnull()]