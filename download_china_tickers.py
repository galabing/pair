#!/usr/bin/python

import argparse
import os

WGET = '/usr/local/bin/wget'

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--category', required=True)
  parser.add_argument('--num_pages', required=True)
  parser.add_argument('--download_dir', required=True)
  args = parser.parse_args()

  assert args.category in {'ash', 'bsh', 'asz', 'bsz'}

  for i in range(int(args.num_pages)):
    url = ('http://stock.gtimg.cn/data/index.php?appn=rank&t=rank%s'
           '/code&p=%d&o=0&l=50&v=vRESULT' % (args.category, i+1))
    output_path = '%s/page%d.js' % (args.download_dir, i+1)
    cmd = '%s -q -O %s "%s"' % (WGET, output_path, url)
    print cmd
    assert os.system(cmd) == 0

if __name__ == '__main__':
  main()

