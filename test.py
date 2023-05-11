import statsmodels.tsa.stattools as ts
from sklearn.preprocessing import minmax_scale
from alive_progress import alive_bar
import pandas as pd
import os
import sys
import multiprocessing
import time
from functools import partial
from random import *


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

global PAIR_P_VALUE

def handle(assets: list, combinations: int) -> list:
    PAIR_P_VALUE = list()
    with alive_bar(len(assets)) as bar:
        for assetOne in assets:
            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                res = pool.map(partial(matchPairs, assetOne), assets)
                PAIR_P_VALUE.extend(res)

            bar()
    filtered =list(filter(lambda x: x is not None, PAIR_P_VALUE))

    return sorted(filtered, key=lambda x: x['p-value'])

def loadAndNormalizeData(asset: str):
    df = pd.read_csv(root + '/cointegration-pair-v1/TimeSeriesData/' + asset + '_USDT.csv')
    df_close_normalized = minmax_scale(df['close'])

    return df_close_normalized


def runEngleGranger(df1, df2) -> int:
    return ts.coint(df1, df2)[1]


def matchPairs(assetOne, assetTwo):
    a1 = loadAndNormalizeData(assetOne)
    a2 = loadAndNormalizeData(assetTwo)
    if assetOne != assetTwo and len(a1) == len(a2):
        p_value = runEngleGranger(a1, a2)
        return {
            'pair': assetOne + 'USDT' + '-' + assetTwo + 'USDT',
            'p-value': p_value,
        }
