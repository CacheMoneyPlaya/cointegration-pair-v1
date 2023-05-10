import statsmodels.tsa.stattools as ts
from sklearn.preprocessing import minmax_scale
from alive_progress import alive_bar
import pandas as pd
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

PAIR_P_VALUE = list()

def handle(assets: list, combinations: int) -> list:
    with alive_bar(combinations) as bar:
        for assetOne in assets:
            a1 = loadAndNormalizeData(assetOne)
            for assetTwo in assets:
                a2 = loadAndNormalizeData(assetTwo)
                if assetOne != assetTwo and len(a1) == len(a2):
                    p_value = runEngleGranger(a1, a2)
                    PAIR_P_VALUE.append(
                        {
                            'pair': assetOne + 'USDT' + '-' + assetTwo + 'USDT',
                            'p-value': p_value,
                        }
                    )

                    bar()

    return sorted(PAIR_P_VALUE, key=lambda x: x['p-value'])


def loadAndNormalizeData(asset: str):
    df = pd.read_csv(root + '/cointegration-pair-v1/TimeSeriesData/' + asset + '_USDT.csv')
    df_close_normalized = minmax_scale(df['close'])

    return df_close_normalized


def runEngleGranger(df1, df2) -> int:
    return ts.coint(df1, df2)[1]
