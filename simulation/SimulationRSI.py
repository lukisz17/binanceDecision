import numpy as np
from calculation.RSI import calculateRSI


def testRSIstrategy(df, rsiLength):
    print('Starting RSI strategy ', rsiLength)
    resDF = calculateRSI(df, rsiLength)
    array = resDF.to_numpy()

    totalProfit, winTrades, lostTrades = simulation(array)

    print('RSI strategy complete, profit=', totalProfit)

def simulation(array):

    ADX_SLOPE_INDEX = 9

    openTrade = False
    capital = 100.0
    commision = 0.01
    buyVolume = 0.0
    totalProfit = 0.0
    winTrades = 0
    lostTrades = 0

    rsiChangedStartLong = False;

    for x in range(1,  len(array)):
        row = array[x]
        closeTime = row[0]
        close = row[4]
        high = row[2]
        typicalPrice = row[5]
        rsi = row[7]

        if not openTrade:
            if array[x-1][7] <= 50 and array[x][7] > 50:
                openTrade = True
                buyVolume = capital / close
                #print('Buy at ', closeTime, close)

        if openTrade:

            newCapital = buyVolume * high
            possibleProfit = newCapital - capital - commision

            if possibleProfit/capital >= 0.005 or ( array[x-1][7] >= 50 and array[x][7] < 50):

                openTrade = False
                totalProfit = totalProfit + capital*0.005

                #print('Sell at ', closeTime, close, newCapital, profit)
                if profit >= 0:
                    winTrades = winTrades + 1
                else:
                    lostTrades = lostTrades + 1


    return totalProfit, winTrades, lostTrades