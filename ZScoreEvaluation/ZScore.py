import scipy
import numpy as np
import pandas as pd
import termplotlib as tpl
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from CointegrationEvaluation import EngleGranger as eg
import statsmodels.api as sm

POSITIVE_TESTS = []


def handle(p_test_values, consoleDisplay, updateMode):
    return mapValidTests(p_test_values, consoleDisplay, updateMode)


def generateRetuns(df):
    return df.pct_change()


def mapValidTests(p_test_values, consoleDisplay, updateMode):

    if updateMode == False:
        p_test_values = list(filter(lambda d: d['p-value'] < 0.05, p_test_values))

    fig = tpl.figure()

    for result in p_test_values:
        a_ticker = result['pair']['a']
        b_ticker = result['pair']['b']
        pair = a_ticker + 'USDT' + '/' + b_ticker + 'USDT'

        # Load pair data
        df1 = eg.loadData(a_ticker)
        df2 = eg.loadData(b_ticker)

        # Generate the mean of the time series for Z=0
        pair_price_df = df1['close']/df2['close']
        z_zero = pair_price_df.mean()

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

        half_life = calculate_half_life(df1['close'], df2['close'])

        # Chart 100*T candles
        if ((z_score.iloc[-1] >= 1.5 or z_score.iloc[-1] <= -1.5) and half_life < 10) or updateMode == True:
            # Generic axis data
            y = z_score[-100:]
            x = list(range(0, len(y), 1))

            # Display to console to chart if setting is given
            if consoleDisplay:
                fig.plot(x, y, label=pair, width=150, height=45)
            else:
                # Otherwise create a PNG Ffor emission
                chartZScore(a_ticker, b_ticker, x, y)

            # Track passing tests
            POSITIVE_TESTS.append({
                'a_ticker': a_ticker,
                'b_ticker': b_ticker,
                'z_score_n': round(z_score.iloc[-1], 3),
                'p_value': round(result['p-value'], 5),
                'half_life': half_life,
                'z_zero': round(z_zero, 6),
            })

    # Print all ASCII chart instances
    if consoleDisplay:
        print(fig.get_string())

    return POSITIVE_TESTS


def calculate_half_life(df1, df2):
    # Compute spread
    spread = df1 - df2
    # Remove any void values
    spread = spread.replace([np.inf, -np.inf], np.nan)
    spread = spread.dropna(axis=0)
    lag = np.roll(spread, 1)
    lag[0] = 0
    ret = spread - lag
    lag2 = sm.add_constant(lag)
    model = sm.OLS(ret, lag2)
    res = model.fit()
    return round(-np.log(2) / res.params[1], 2)


def chartZScore(a, b, x , y):
    plt.style.use('dark_background')

    plt.axhline(y=1.5,color='red')
    plt.axhline(y=-1.5,color='green')
    plt.axhline(y=0,color='white')

    plt.plot(x, y)

    plt.title(a + '-' + b, fontsize=14)
    plt.xlabel('N*T', fontsize=14)
    plt.ylabel('Z-SCORE', fontsize=14)

    plt.savefig('./ZScoreEvaluation/Charts/' + a + '_' + b + '.png')
    plt.clf()
