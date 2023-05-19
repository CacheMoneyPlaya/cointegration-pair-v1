import os
import sys
import time
import pandas as pd
import multiprocessing
from colorist import Color
from alive_progress import alive_bar
import statsmodels.tsa.stattools as ts
from sklearn.preprocessing import minmax_scale

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)
PAIR_P_VALUE = list()
ITTERATED = dict()

def handle(assets: list) -> list:

    for assetOne in assets:
        matchPairs(assetOne, assets, PAIR_P_VALUE, ITTERATED)

    return sorted(PAIR_P_VALUE, key=lambda x: x['p-value'])


def loadAndNormalizeData(asset: str):
    df = pd.read_csv(root + '/cointegration-pair-v1/TimeSeriesData/' + asset + '_USDT.csv')
    df_close_normalized = minmax_scale(df['close'])

    return df_close_normalized


def loadData(asset: str):
    return pd.read_csv(root + '/cointegration-pair-v1/TimeSeriesData/' + asset + '_USDT.csv')


def runEngleGranger(df1, df2) -> int:
    return ts.coint(df1, df2)[1]


def matchPairs(assetOne, assets, PAIR_P_VALUE, ITTERATED):
    a1 = loadAndNormalizeData(assetOne)
    for assetTwo in assets:
        a2 = loadAndNormalizeData(assetTwo)
        reverseKey = assetTwo+assetOne
        # If we dont have the same df and lengths are same and is not same as reverse
        if assetOne != assetTwo and len(a1) == len(a2) and reverseKey not in ITTERATED:
            key_name = assetOne+assetTwo
            ITTERATED.update({key_name:True})
            p_value = runEngleGranger(a1, a2)
            PAIR_P_VALUE.append(
                {
                    'pair': {
                        'a': assetOne,
                        'b': assetTwo,
                    },
                    'quote': 'USDT',
                    'p-value': p_value,
                }
            )
