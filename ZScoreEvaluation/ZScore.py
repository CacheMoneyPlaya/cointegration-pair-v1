from CointegrationEvaluation import EngleGranger as eg
from dotenv import load_dotenv
import termplotlib as tpl
import matplotlib.pyplot as plt
import numpy as np
import scipy
import pandas as pd

POSITIVE_TESTS = []

def handle(p_test_values, consoleDisplay):
    return mapValidTests(p_test_values, consoleDisplay)

def generateRetuns(df):
    return df.pct_change()


def mapValidTests(p_test_values, consoleDisplay):
    p_test_values = list(filter(lambda d: d['p-value'] < 0.05, p_test_values))
    fig = tpl.figure()

    for result in p_test_values:
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
        if z_score.iloc[-1] >= 1.5 or z_score.iloc[-1] <= -1.5:
            y = z_score[-100:]
            x = list(range(0, len(y), 1))
            if consoleDisplay:
                fig.plot(x, y, label=pair, width=150, height=45)
            else:
                plt.style.use('dark_background')
                plt.axhline(y=1.5,color='red')
                plt.axhline(y=-1.5,color='green')
                plt.plot(x, y)
                plt.title(a_ticker + '-' + b_ticker, fontsize=14)
                plt.xlabel('N*T', fontsize=14)
                plt.ylabel('Z-SCORE', fontsize=14)
                plt.savefig('./ZScoreEvaluation/Charts/' + a_ticker + '_' + b_ticker + '.png')
                plt.clf()
            POSITIVE_TESTS.append({
                'a_ticker': a_ticker,
                'b_ticker': b_ticker,
                'z_score_n': round(z_score.iloc[-1], 3),
                'p_value': round(result['p-value'], 5)
            })

    if consoleDisplay:
        print(fig.get_string())

    return POSITIVE_TESTS
