from flask import Flask
from unicorn_binance_rest_api.unicorn_binance_rest_api_manager import BinanceRestApiManager
import numpy as np

app = Flask(__name__)


def getKLines(apiManager, symbol, interval):
    data = apiManager.get_klines(
        symbol=symbol,
        interval=interval,
        limit=200
    )

    return data

@app.route('/')
def hello_world():  # put application's code here
    apiManager = BinanceRestApiManager('api_key', 'api_secret', exchange="binance.com")
    data = np.array(getKLines(apiManager, "ETHUSDT", '1m'))
    return 'Hello World!' + str(len(data))


if __name__ == '__main__':
    app.run()
