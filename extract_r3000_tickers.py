#!/usr/bin/python

import argparse

SKIP_LINES = {'', 'Company Ticker'}
SKIP_SUFFIXES = {'As of 6/27/2014 Russell Indexes.'}

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--raw_file', required=True)
  parser.add_argument('--ticker_file', required=True)
  args = parser.parse_args()

  with open(args.raw_file, 'r') as fp:
    lines = fp.read().splitlines()
  tickers = set()
  for line in lines:
    line = line.strip()
    for suffix in SKIP_SUFFIXES:
      if line.endswith(suffix):
        line = line[:-len(suffix)]
        line = line.strip()
        break
    if line in SKIP_LINES:
      continue
    p = line.rfind(' ')
    assert p > 0
    ticker = line[p+1:]
    assert ticker not in tickers
    tickers.add(ticker)

  with open(args.ticker_file, 'w') as fp:
    for ticker in sorted(tickers):
      print >> fp, ticker

if __name__ == '__main__':
  main()

