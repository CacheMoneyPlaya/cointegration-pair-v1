from CointegrationEvaluation import EngleGranger as eg
import termplotlib as tpl
import numpy as np
import scipy

import pandas as pd
def handle(p_test_values):
    mapValidTests(p_test_values)

def generateRetuns(df):
    return df.pct_change()


def mapValidTests(p_test_values):
    p_test_values = list(filter(lambda d: d['p-value'] < 0.05, p_test_values))
    fig = tpl.figure()

    for result in p_test_values[:50]:
        a_ticker = result['pair']['a']
        b_ticker = result['pair']['b']

        pair = a_ticker + 'USDT' + '/' + b_ticker + 'USDT'

        df1 = eg.loadData(a_ticker)
        df2 = eg.loadData(b_ticker)

        # Calculate returns in each df respective to close
        df1_returns = generateRetuns(df1['close'])
        df2_returns = generateRetuns(df2['close'])

        # Compute spread
        spread = df1_returns - df2_returns

        # Remove any void values
        spread = spread.replace([np.inf, -np.inf], np.nan)
        spread = spread.dropna(axis=0)

        # Compute Z-Score
        z_score = scipy.stats.zscore(spread)

        # Chart 100*T candles
        y = z_score[-100:]

        x = list(range(0, len(y), 1))

        fig.plot(x, y, label=pair, width=150, height=45)

    print(fig.get_string())
