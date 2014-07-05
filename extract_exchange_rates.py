#!/usr/bin/python

from bs4 import BeautifulSoup
from datetime import datetime
import argparse

DAYS = {'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'}
DATE_PATTERN = '%d/%m/%Y'
OUTPUT_DATE_PATTERN = '%Y-%m-%d'
EX_SUFFIX = ' CNY'

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--html_file', required=True)
  parser.add_argument('--ex_file', required=True)
  args = parser.parse_args()

  soup = BeautifulSoup(open(args.html_file, 'r'))
  tables = soup.find_all('table')
  assert len(tables) == 1
  trs = tables[0].find_all('tr')
  assert len(trs) > 0
  tds = trs[0].find_all('td')
  assert len(tds) == 4
  assert tds[0].get_text() == 'Historical Date'
  assert tds[1].get_text() == 'US Dollar'
  assert tds[2].get_text() == 'Chinese Yuan'
  assert tds[3].get_text() == 'Analysis'

  ex_map = dict()
  for i in range(1, len(trs)):
    tds = trs[i].find_all('td')
    assert len(tds) == 5
    assert tds[0].get_text() in DAYS
    date = datetime.strptime(tds[1].get_text(), DATE_PATTERN)
    assert tds[2].get_text() == '1 USD ='
    ex_str = tds[3].get_text()
    assert ex_str.endswith(EX_SUFFIX)
    ex = float(ex_str[:-len(EX_SUFFIX)])
    assert tds[4].get_text() == (
        'USD CNY rate for %s' % date.strftime(DATE_PATTERN))
    date = date.strftime(OUTPUT_DATE_PATTERN)
    if date in ex_map:
      assert ex == ex_map[date]
    else:
      ex_map[date] = ex

  with open(args.ex_file, 'w') as fp:
    for date in sorted(ex_map.keys()):
      print >> fp, '%s %f' % (date, ex_map[date])

if __name__ == '__main__':
  main()

