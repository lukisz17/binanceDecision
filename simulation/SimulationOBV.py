import numpy as np
from calculation.OBV import calculateOBV


def testOBVstrategy(df):
    print('Starting OBV strategy')

    pow = [0.5, 1.0, 1.1, 1.15, 1.2, 1.25, 1.27, 1.3, 1.35]
    maxProfit = -100000000

    for ema in range(20,25): #(20, 80):
        for signalSmoothing in range(14, 25): #(14, 80):
            for power in pow:
                for rsiP in [20, 30,  40, 70]:
                    resDF = calculateOBV(df, ema, signalSmoothing, power)
                    array = resDF.to_numpy()
                    totalProfit, winTrades, lostTrades = simulation(array, rsiP)
                    if totalProfit >= 1:
                        print(f'{totalProfit}, {winTrades}, {lostTrades}, {ema}, {signalSmoothing}, {power}, {rsiP}')
                    if totalProfit > maxProfit:
                        maxProfit = totalProfit

    print('OBV strategy complete, profit=', maxProfit)

def simulation(array, rsiP):

    ADX_SLOPE_INDEX = 9

    openTrade = False
    capital = 100.0
    commision = 0.2
    buyVolume = 0.0
    totalProfit = 0.0
    winTrades = 0
    lostTrades = 0

    for x in range(len(array)):
        row = array[x]
        closeTime = row[0]
        close = row[4]
        obv_osc = row[8]
        o_ma = row[9]
        o_ma_s = row[10]
        rsi = row[11]


        if not openTrade and o_ma > o_ma_s and rsi <= rsiP:

            openTrade = True
            buyVolume = capital / close
            #print('Buy at ', closeTime, close, rsi)

        if openTrade:

            newCapital = buyVolume * close
            profit = newCapital - capital - commision

            if profit >= 2 or profit <= -1: #o_ma < o_ma_s:
                openTrade = False
                totalProfit = totalProfit + profit

                #print('Sell at ', closeTime, close, newCapital, profit)
                if profit >= 0:
                    winTrades = winTrades + 1
                else:
                    lostTrades = lostTrades + 1


    return totalProfit, winTrades, lostTrades