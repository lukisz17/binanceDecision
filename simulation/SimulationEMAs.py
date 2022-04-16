import numpy as np

def strategy():
    shortSamples = [5, 10, 14, 17, 20, 24]
    mediumSamples = [9, 7, 10, 14, 20, 24]

    maxProfit = -100000000

    for short in range(3, 4):
        for medium in range(10, 14):
            for long in range(25, 26):
                if short < medium and medium < long:
                    resDF = calculate4Emas(df, shortLength=short, mediumLength=medium, longLength=long)
                    array = resDF.to_numpy()
                    totalProfit, winTrades, lostTrades = simulation(array)
                    print('Calculation ', short, medium, long, totalProfit, winTrades, lostTrades)
                    if totalProfit > maxProfit:
                        maxProfit = totalProfit

    return maxProfit


def simulation(array):

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
        typicalPrice = row[5]
        demaShort = row[6]
        demaMedium = row[7]
        demaLong = row[8]
        dema100 = row[9]
        dema200 = row[10]

        if not openTrade and demaMedium > demaLong and dema100 > dema200:
            openTrade = True
            buyVolume = capital / close
            #print('Buy at ', closeTime, close)

        if openTrade:

            newCapital = buyVolume * close
            if demaShort < demaMedium:
                openTrade = False
                profit = newCapital - capital - commision
                totalProfit = totalProfit + profit

                #print('Sell at ', closeTime, close, newCapital, profit)
                if profit >= 0:
                    winTrades = winTrades + 1
                else:
                    lostTrades = lostTrades + 1


    return totalProfit, winTrades, lostTrades