from CointegrationEvaluation import EngleGranger as eg
import termplotlib as tpl
import numpy

import pandas as pd
def handle(p_test_values):
    mapValidTests(p_test_values)

def generateRetuns(df):
    return df.pct_change()


def mapValidTests(p_test_values):
    p_test_values = list(filter(lambda d: d['p-value'] < 0.05, p_test_values))
    for result in p_test_values:
        a_ticker = result['pair']['a']
        b_ticker = result['pair']['b']

        pair = a_ticker + '-' + b_ticker

        df1 = eg.loadAndNormalizeData(a_ticker)
        df2 = eg.loadAndNormalizeData(b_ticker)

        df1 = pd.DataFrame(data = df1, columns = ['figure'])
        df2 = pd.DataFrame(data = df2, columns = ['figure'])

        # Calculate returns in each df
        df1_returns = generateRetuns(df1)
        df2_returns = generateRetuns(df2)

        # Compute spread
        spread = df1_returns - df2_returns

        z_score = (spread - spread.mean()) / spread.std()

        # Charts the z-score
        y = z_score[-100:]['figure']

        x = list(range(0, len(y), 1))

        fig = tpl.figure()
        fig.plot(x, y, label=pair, width=150, height=45)
        string = fig.get_string()
        print(string)
