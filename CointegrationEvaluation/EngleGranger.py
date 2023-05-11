import statsmodels.tsa.stattools as ts
from sklearn.preprocessing import minmax_scale
from alive_progress import alive_bar
import pandas as pd
import os
import sys
import multiprocessing
import time

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)
running = multiprocessing.Value('i', 0)


def handle(assets: list, combinations: int) -> list:
    jobs = []
    t0 = time.perf_counter()

    with multiprocessing.Manager() as manager:
        PAIR_P_VALUE = manager.list()

        for assetOne in assets:
            p = multiprocessing.Process(target=matchPairs, args=(assetOne, assets, PAIR_P_VALUE))
            jobs.append(p)
            p.start()
            while len(jobs) > 8:
                jobs = [job for job in jobs if job.is_alive()]
        print('waiting on jobs...')
        for job in jobs:
            job.join()

        return sorted(PAIR_P_VALUE, key=lambda x: x['p-value'])

def loadAndNormalizeData(asset: str):
    df = pd.read_csv(root + '/cointegration-pair-v1/TimeSeriesData/' + asset + '_USDT.csv')
    df_close_normalized = minmax_scale(df['close'])

    return df_close_normalized


def runEngleGranger(df1, df2) -> int:
    return ts.coint(df1, df2)[1]


def matchPairs(assetOne, assets, PAIR_P_VALUE):
    a1 = loadAndNormalizeData(assetOne)
    for assetTwo in assets:
        a2 = loadAndNormalizeData(assetTwo)
        if assetOne != assetTwo and len(a1) == len(a2):
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
