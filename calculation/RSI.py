import numpy as np
import pandas as pd
import pandas_ta as ta

def calculateRSI(df, rsiLength):
    df['rsi'] = ta.rsi(close=df['close'], length=rsiLength)
    return df[df['rsi'].notnull()]