# -*- coding: utf-8 -*-

import os
import sys
import csv
import multiprocessing
import random
import time


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from colorist import Color
import ccxt


def fetchAllTimeSeriesData(assets: list, timeframe: str, since: str, console_display: bool) -> None:
    jobs = []
    for index, asset in enumerate(assets):

        if index % 2 == 0:
            time.sleep(5)

        exchange = 'binance'
        asset_and_quote = asset + '/USDT'
        file_name = asset + '_USDT' + '.csv'
        p = multiprocessing.Process(target=scrape_candles_to_csv, args=(file_name, exchange, 3, asset_and_quote, timeframe, since, 100, console_display))
        jobs.append(p)
        p.start()

    while len(jobs) > 0:
        jobs = [job for job in jobs if job.is_alive()]
        time.sleep(1)

    print(f"{Color.GREEN}DOWNLOAD COMPLETE{Color.GREEN}")


def retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, since, limit):
    num_retries = 0
    try:
        num_retries += 1
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
        # print('Fetched', len(ohlcv), symbol, 'candles from', exchange.iso8601 (ohlcv[0][0]), 'to', exchange.iso8601 (ohlcv[-1][0]))
        return ohlcv
    except Exception as inst:
        if num_retries > max_retries:
            raise  # Exception('Failed to fetch', timeframe, symbol, 'OHLCV in', max_retries, 'attempts')


def scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit, console_display):
    timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
    timeframe_duration_in_ms = timeframe_duration_in_seconds * 1000
    timedelta = limit * timeframe_duration_in_ms
    now = exchange.milliseconds()
    all_ohlcv = []
    fetch_since = since
    if console_display:
        print(f"{Color.YELLOW}'Downloading {symbol} time series data...'{Color.OFF}")

    while fetch_since < now:
        ohlcv = retry_fetch_ohlcv(exchange, max_retries, symbol, timeframe, fetch_since, limit)
        fetch_since = (ohlcv[-1][0] + 1) if len(ohlcv) else (fetch_since + timedelta)
        all_ohlcv = all_ohlcv + ohlcv

        if len(all_ohlcv):
            pass
        elif console_display:
            print(f"{Color.WHITE}'{len(all_ohlcv)} candles in total from {exchange.iso8601(fetch_since)}' {Color.WHITE}")

    return exchange.filter_by_since_limit(all_ohlcv, since, None, key=0)


def write_to_csv(filename, data):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.join(current_dir, '../TimeSeriesData/') + filename
    headers = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    with open(target_dir, mode='w+') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(headers)
        csv_writer.writerows(data)


def scrape_candles_to_csv(filename, exchange_id, max_retries, symbol, timeframe, since, limit, console_display):
    # instantiate the exchange by id
    exchange = getattr(ccxt, exchange_id)()
    # convert since from string to milliseconds integer if needed
    if isinstance(since, str):
        since = exchange.parse8601(since)
    # preload all markets from the exchange
    exchange.load_markets()
    # fetch all candles
    ohlcv = scrape_ohlcv(exchange, max_retries, symbol, timeframe, since, limit, console_display)
    # save them to csv file
    write_to_csv(filename, ohlcv)
    if console_display:
        print(f"{Color.GREEN}'Saved {len(ohlcv)} candles from {exchange.iso8601(ohlcv[0][0])} to {exchange.iso8601(ohlcv[-1][0])} to {filename}' {Color.OFF}")

# -----------------------------------------------------------------------------
# Binance's BTC/USDT candles start on 2017-08-17

def clearTimeSeries():
    dir = './TimeSeriesData'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def clearPng():
    dir = './ZScoreEvaluation/Charts'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
