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
running = multiprocessing.Value('i', 0)


def handle(assets: list) -> list:
    jobs = []

    with multiprocessing.Manager() as manager:
        PAIR_P_VALUE = manager.list()
        ITTERATED = manager.dict()

        for assetOne in assets:
            p = multiprocessing.Process(target=matchPairs, args=(assetOne, assets, PAIR_P_VALUE, ITTERATED))
            jobs.append(p)
            p.start()
            while len(jobs) > multiprocessing.cpu_count():
                jobs = [job for job in jobs if job.is_alive()]
        for job in jobs:
            job.join()

        print(f"{Color.YELLOW}Waiting for all tasks to complete..{Color.OFF}")

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
