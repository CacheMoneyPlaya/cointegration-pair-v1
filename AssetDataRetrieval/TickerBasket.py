from dotenv import load_dotenv, dotenv_values
from colorist import Color

load_dotenv()
config = dotenv_values(".env")

def getBasket(basket):
    if basket == None:
        tickers = []
        for x in config.values():
            tickers.extend(x.split(','))
        return tickers

    return config[basket].split(',')
