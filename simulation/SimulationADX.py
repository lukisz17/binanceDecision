import numpy as np
from calculation.DMI import calculateDMI


def testDMIstrategy(df):
    print('Starting ADX strategy')
    resDF = calculateDMI(df, 8, 12)
    array = resDF.to_numpy()

    totalProfit, winTrades, lostTrades = simulation(array, 4, 1, 20)

    print('ADX strategy complete, profit=', totalProfit)

def simulation(array, lookBackForADXChange, lookBackCurrentConfirmation, DMNegativePositiveTreshold):

    ADX_SLOPE_INDEX = 9

    openTrade = False
    capital = 100.0
    commision = 0.2
    buyVolume = 0.0
    totalProfit = 0.0
    winTrades = 0
    lostTrades = 0

    for x in range(lookBackForADXChange+1,  len(array)):
        row = array[x]
        closeTime = row[0]
        close = row[4]
        typicalPrice = row[5]
        DMP = row[6]
        DMN = row[7]
        ADX = row[8]
        ADXslope = row[ADX_SLOPE_INDEX]
        rsi = row[10]

        # ADX reversal = slope change from positive to negative
        # moneyInHands4.ipynb to understand it
        if not openTrade:
            #print(closeTime, ADXslope)
            if ADXslope < 0 and DMN - DMP >= DMNegativePositiveTreshold:
                allLookbackPositive = True
                allLookbackConfirmationNegative = True

                for k in range(x - lookBackForADXChange + 1, x - lookBackCurrentConfirmation + 1):
                    if array[k][ADX_SLOPE_INDEX] < 0: allLookbackPositive = False

                for k in range(x - lookBackCurrentConfirmation + 1, x):
                    if array[k][ADX_SLOPE_INDEX] > 0: allLookbackConfirmationNegative = False

                if allLookbackPositive and allLookbackConfirmationNegative:
                    openTrade = True
                    buyVolume = capital / close
                    print('Buy at ', closeTime, close, DMN - DMP, rsi)

        if openTrade:

            newCapital = buyVolume * close
            profit = newCapital - capital - commision

            if profit > 1 or profit < -3:
                openTrade = False
                totalProfit = totalProfit + profit

                print('Sell at ', closeTime, close, newCapital, profit)
                if profit >= 0:
                    winTrades = winTrades + 1
                else:
                    lostTrades = lostTrades + 1


    return totalProfit, winTrades, lostTrades