import numpy as np

def simulation(array, ADX_BUY, ADX_SELL):

    openTrade = False
    capital = 100.0
    buyVolume = 0.0
    totalProfit = 0.0

    for x in range(len(array)):
        row = array[x]
        DMP_BUY = row[0]
        DMN_BUY = row[1]
        DMP_SELL = row[2]
        DMN_SELL = row[3]
        ADX = row[4]

        if not openTrade and ADX >= ADX_BUY:
            if DMN_BUY == True and DMP_BUY == True:
               openTrade = True
               buyVolume = capital / row[5]
               #print('Buy at ', row['closeTime'])

        if openTrade and ADX >= ADX_SELL:
            if DMN_SELL == True and DMP_SELL == True:
                openTrade = False
                newCapital = buyVolume * row[5]
                profit = newCapital - capital
                totalProfit = totalProfit + profit
                #print('Sell at ', row['closeTime'], profit)

    return totalProfit