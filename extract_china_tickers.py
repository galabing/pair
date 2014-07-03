#!/usr/bin/python

import argparse
import os

PREFIX = "data:'"
SUFFIX = "'};"
CATEGORY_MAP = {'sh': 'ss', 'sz': 'sz'}

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--base_dir', required=True)
  parser.add_argument('--categories', required=True)
  parser.add_argument('--ticker_file', required=True)
  args = parser.parse_args()

  tickers = set()
  categories = args.categories.split(',')
  for category in categories:
    input_dir = '%s/%s' % (args.base_dir, category)
    assert os.path.isdir(input_dir)
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.js')]
    for input_file in input_files:
      with open('%s/%s' % (input_dir, input_file), 'r') as fp:
        content = fp.read()
      p = content.find(PREFIX)
      assert p > 0
      p += len(PREFIX)
      q = content.find(SUFFIX, p)
      assert q > p
      items = content[p:q].split(',')
      for item in items:
        c = item[:2]
        n = item[2:]
        assert c in CATEGORY_MAP
        ticker = '%s.%s' % (n, CATEGORY_MAP[c])
        assert ticker not in tickers
        tickers.add(ticker)

  with open(args.ticker_file, 'w') as fp:
    for ticker in sorted(tickers):
      print >> fp, ticker

if __name__ == '__main__':
  main()

