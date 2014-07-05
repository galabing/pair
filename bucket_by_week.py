#!/usr/bin/python

""" Averages price data into weekly buckets; outputs <week_id> <avg_price>
    pairs for each yahoo data file.

    <week_id> is the offset from the week of 1900-01-01, which is assumed
    to be earlier than all stock data.

    For missing weeks: output as is.  For US stocks this is rare (sometimes
    happens at the beginning of a stock's life).  For Chinese stocks this
    happens around 10/1 holidays.
"""

from datetime import datetime, timedelta
import argparse
import os

DATE_PATTERN = '%Y-%m-%d'
MIN_DATE = '1900-01-01'

def get_min_date():
  """ Returns the first Monday on or before MIN_DATE.
      Thus taking the offset of any date divided by 7 will give the <week_id>.
  """
  date = datetime.strptime(MIN_DATE, DATE_PATTERN)
  one_day = timedelta(days=1)
  while date.weekday() != 0:
    date -= one_day
  return date

def date_to_week(date, min_date):
  assert date > min_date
  delta = date - min_date
  return int(delta.days/7)

def week_to_date(week, min_date):
  return min_date + timedelta(days=week*7)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--yahoo_dir', required=True)
  parser.add_argument('--bucket_dir', required=True)
  parser.add_argument('--overwrite', action='store_true')
  args = parser.parse_args()

  min_date = get_min_date()
  print 'using the week of %s as week zero, the monday of the week is %s' % (
      MIN_DATE, min_date.strftime(DATE_PATTERN))

  output_set = set()
  if not args.overwrite:
    for f in os.listdir(args.bucket_dir):
      if f.endswith('.txt'):
        output_set.add(f.replace('.txt', '.csv'))
  print 'skipping %d previous output' % len(output_set)

  input_files = [f for f in os.listdir(args.yahoo_dir)
                 if f.endswith('.csv') and f not in output_set]
  print 'processing %d files from %s' % (len(input_files), args.yahoo_dir)

  for i in range(len(input_files)):
    if i % 100 == 0:
      print '(%d done)' % i
    with open('%s/%s' % (args.yahoo_dir, input_files[i]), 'r') as fp:
      lines = fp.read().splitlines()
    assert len(lines) > 0
    assert lines[0] == 'Date,Open,High,Low,Close,Volume,Adj Close'
    data = dict()
    for j in range(1, len(lines)):
      dt, op, hi, lo, cl, vo, ac = lines[j].split(',')
      week = date_to_week(datetime.strptime(dt, DATE_PATTERN), min_date)
      ac = float(ac)
      if week not in data:
        data[week] = [ac, 1]
      else:
        data[week][0] += ac
        data[week][1] += 1
    with open('%s/%s.txt' % (args.bucket_dir, input_files[i][:-4]), 'w') as fp:
      for week in sorted(data.keys(), reverse=True):
        print >> fp, '%d %f' % (week, data[week][0]/data[week][1])

if __name__ == '__main__':
  main()

