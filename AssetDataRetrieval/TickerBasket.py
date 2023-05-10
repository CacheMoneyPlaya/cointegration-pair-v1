from dotenv import load_dotenv, dotenv_values
from colorist import Color

load_dotenv()
config = dotenv_values(".env")

def getBasket(basket):
    if basket == None:
        if input(f"{Color.YELLOW}This will likely cause a rate limit, are you sure? (y/n){Color.OFF}") != "y":
            exit()
        tickers = []
        for x in config.values():
            tickers.extend(x.split(','))
        return tickers

    return config[basket].split(',')
