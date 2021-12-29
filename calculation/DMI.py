import numpy as np
import pandas as pd
import pandas_ta as ta

def calculateDMI(df, adxLength, DMsmoothingLength):
    adx = ta.adx(close=df['close'], high=df['high'], low=df['low'], length=8)
    adx = ta.adx(close=df['close'], high=df['high'], low=df['low'], length=adxLength)
    df['DMP'] = ta.ema(adx['DMP_' + str(adxLength)], length=DMsmoothingLength) # ta.linreg
    df['DMN'] = ta.ema(adx['DMN_' + str(adxLength)], length=DMsmoothingLength)  # to 14 i  24 musi byc parametrem
    df['ADX'] = adx['ADX_' + str(adxLength)]

    #df = df[df['ADX'].notnull()]
    df['ADX_slope_ta'] = ta.slope(df['ADX'], length=2)

    return df[df['ADX_slope_ta'].notnull()]