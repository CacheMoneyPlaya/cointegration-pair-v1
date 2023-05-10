import argparse
from AssetDataRetrieval import FetchTimeSeries as fts
from dotenv import load_dotenv, dotenv_values
from CointegrationEvaluation import EngleGranger as eg
from colorist import Color

CONFIG = None

def entry():

    assets = CONFIG['assets']
    timeframe = CONFIG['timeframe']
    since = CONFIG['starting_date']
    reuse_data = CONFIG['reuse_data']
    engle_granger_threshold = CONFIG['reuse_data']

    if assets is None:
        assets = [
            # 'SOL','ADA','AVAX','ATOM','ALGO','BNB','MATIC','SUSHI','LINK',
            # 'AAVE','RLC','FET','PHB','OCEAN','GRT','LDO','FXS','FTM','NEAR','NEO'
            # 'MKR','RUNE','DYDX','COMP','YFI','CRV','SNX','KAVA','UNI','VET',
            # 'ZIL','FIL','JASMY','DOGE','SHIB','MASK','GALA','SAND','ALICE','MANA',
            # 'THETA','ICP','CHZ','XRP','DASH','LTC','EOS','ETC','XLM','PEOPLE','OMG',
            # 'QTUM','APE',
                'MASK', 'GALA', 'SAND', 'ALICE', 'MANA', 'THETA', 'ICP', 'APE', 'CHZ',
            ]

    total_pairs = (len(assets)**2)-len(assets)

    # Fetch all tickers data and store locally
    if reuse_data == False:
        print(f"{Color.BLUE}Scraping specified ticker candle data...{Color.OFF}")
        fts.fetchAllTimeSeriesData(assets, timeframe, since)

    # Compute Engle-Granger test for each possible combination
    print(f"{Color.BLUE}Running Engle-Granger tests on {total_pairs} unique pairs ...{Color.OFF}")

    p_test_values = eg.handle(assets, total_pairs)

    for i, p_test in enumerate(p_test_values[:10]):
        if i%2 == 0:
            print(f"{Color.RED}{p_test}{Color.OFF}")


    #compute z score chart

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-a", "--assets", help="Asset to calculate cointegration coefficient, comma sepperated", required=False)
    parser.add_argument("-t", "--timeframe", help="OHLC Timeframe i.e. 1m,5m,15m..", required=True)
    parser.add_argument("-d", "--starting_date", help="Datascrape start date i.e. '2020-05-20'", required=True)
    parser.add_argument("-r", "--reuse_data", help="Reuse saved data for asset", required=False, action="store_true")
    parser.add_argument("-c", "--engle_granger_threshold", help="Minimum truthy theshold", required=False)

    args, unknown = parser.parse_known_args()
    CONFIG = vars(args)

    entry()
