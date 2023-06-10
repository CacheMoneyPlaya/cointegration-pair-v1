import argparse
from AssetDataRetrieval import FetchTimeSeries as fts
from AssetDataRetrieval import TickerBasket as tb
from dotenv import load_dotenv, dotenv_values
from CointegrationEvaluation import EngleGranger as eg
from colorist import Color
from DataOutput import Output as o
from ZScoreEvaluation import ZScore as zs
from DiscordUpdate import DiscordUpdate as du
import arrow


CONFIG = None

def entry():

    try:
        basket = CONFIG['basket']
        timeframe = CONFIG['timeframe']
        # since = CONFIG['starting_date']
        # 1000 Hours/Data points
        since = arrow.utcnow().shift(days=-42).format("YYYY-MM-DDTHH:mm:ss.SSS[Z]")
        reuse_data = CONFIG['reuse_data']
        console_display = CONFIG['display']
        pair_update = CONFIG['update']

        # If update mode run Z-Score scan against single pair
        if pair_update:
            return update_mode(pair_update, timeframe, since)

        tickers = tb.getBasket(basket)

        fts.clearPng()

        if reuse_data == False:
            fts.clearTimeSeries()
            print(f"{Color.YELLOW}Scraping specified ticker candle data...{Color.OFF}")
            fts.fetchAllTimeSeriesData(tickers, timeframe, since, console_display)

        print(f"{Color.YELLOW}Running Engle-Granger tests assuming 95% confidence interval ...{Color.OFF}")
        p_test_values = eg.handle(tickers)

        if console_display:
            o.output_p_values(p_test_values)

        signals = zs.handle(p_test_values, console_display, False)

        if console_display == False:
            du.update_discord_channel(signals)

    except Exception as e:
        raise e

def update_mode(tickers, timeframe, since):
    tickers = tickers.split('-')
    fts.clearTimeSeries()
    fts.fetchAllTimeSeriesData(tickers, timeframe, since, False)
    p_test_values = eg.handle(tickers)

    signals = zs.handle(p_test_values, True, True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-b", "--basket", help="Baskey to calculate cointegration coefficient, defined in .env", required=False)
    parser.add_argument("-t", "--timeframe", help="OHLC Timeframe i.e. 1m,5m,15m..", required=True)
    # parser.add_argument("-d", "--starting_date", help="Datascrape start date i.e. '2020-05-20'", required=True)
    parser.add_argument("-r", "--reuse_data", help="Reuse saved data for asset", required=False, action="store_true")
    parser.add_argument("-c", "--engle_granger_threshold", help="Minimum truthy theshold", required=False)
    parser.add_argument("-dc", "--display", help="Display Charts in console", required=False, action="store_true")
    parser.add_argument("-u", "--update", help="Fetches latest Z-Scores for supplied pairs", required=False)

    args, unknown = parser.parse_known_args()
    CONFIG = vars(args)

    entry()
