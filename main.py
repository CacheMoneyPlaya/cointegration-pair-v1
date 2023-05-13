import argparse
from AssetDataRetrieval import FetchTimeSeries as fts
from AssetDataRetrieval import TickerBasket as tb
from dotenv import load_dotenv, dotenv_values
from CointegrationEvaluation import EngleGranger as eg
from colorist import Color
from DataOutput import Output as o
from ZScoreEvaluation import ZScore as zs
from DiscordUpdate import DiscordUpdate as du

CONFIG = None

def entry():

    basket = CONFIG['basket']
    timeframe = CONFIG['timeframe']
    since = CONFIG['starting_date']
    reuse_data = CONFIG['reuse_data']
    console_display = CONFIG['display']
    tickers = tb.getBasket(basket)
    total_pairs = (len(tickers)**2)

    fts.clearPng()

    if reuse_data == False:
        fts.clearTimeSeries()
        print(f"{Color.YELLOW}Scraping specified ticker candle data...{Color.OFF}")
        fts.fetchAllTimeSeriesData(tickers, timeframe, since, console_display)

    print(f"{Color.YELLOW}Running Engle-Granger tests on {total_pairs} unique pairs assuming 95% confidence interval ...{Color.OFF}")
    p_test_values = eg.handle(tickers, total_pairs)

    if console_display:
        o.output_p_values(p_test_values)

    # Take top x p-value pairs and chart z-scores
    signals = zs.handle(p_test_values, console_display)
    du.update_discord_channel(signals)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-b", "--basket", help="Baskey to calculate cointegration coefficient, defined in .env", required=False)
    parser.add_argument("-t", "--timeframe", help="OHLC Timeframe i.e. 1m,5m,15m..", required=True)
    parser.add_argument("-d", "--starting_date", help="Datascrape start date i.e. '2020-05-20'", required=True)
    parser.add_argument("-r", "--reuse_data", help="Reuse saved data for asset", required=False, action="store_true")
    parser.add_argument("-c", "--engle_granger_threshold", help="Minimum truthy theshold", required=False)
    parser.add_argument("-dc", "--display", help="Display Charts in console", required=False, action="store_true")

    args, unknown = parser.parse_known_args()
    CONFIG = vars(args)

    entry()
