


# Z-Index using the Engle-Granger as a precursor

Small project I wrote over a couple of evenings for analyzing certain 'basket' crypto
pairs for cointegration which I then use to determine likely retracements on Z-Index
charts over a years hourly data. Currently back testing...

## TODO:
- Clean up files and improve efficiency of coint tests
- Introduce single pair analysis as command line parameter
- Introduce actual date stamps on Z-Index x axis
- Tune up what qualifies as a signal after backtesting
- Introduce % complete log on jobs running for processing of tests
- Improve rate limit issue with mass data retrieval

## Example Command To Use:

```
python main.py --timeframe 1h --starting_date '2023-01-01T00:00:00Z'
```

--basket - Specify grouping of assets to analyze as per .env file i.e '--basket CHINA'
--timeframe - Specify the candle timeframe i.e '--timeframe 1h'
--starting_date - Date to start analysis from, earlier the better for test coverage i.e '--starting_date '2023-01-01T00:00:00Z'' (YYYY-MM-DD)
--reuse_data - If you have previously run searches and you wish to reuse CSVs that were already generated use this tag (If one is missing you'll need to re run entirely)

*** You will need to download [here](https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.5/) for console Z-Index graphing and install pip requirements ***


![Example](https://raw.githubusercontent.com/CacheMoneyPlaya/cointegration-pair-v1/main/Images/eg1.png?raw=true)
![FVG detection](https://raw.githubusercontent.com/CacheMoneyPlaya/cointegration-pair-v1/main/Images/eg2.png?raw=true)
![The numbers Mason](https://tenor.com/view/what-do-they-mean-random-numbers-gif-10654449.gif)
