useful links:
- yahoo download: http://blog.csdn.net/stanmarsh/article/details/9795485

- download russell 3000 membership list from
    https://www.russell.com/documents/indexes/membership/membership-russell-3000.pdf
- ctrl-a/c to membership-russell-3000.txt, remove the nontable portion
- extract tickers
    ./extract_r3000_tickers.py --raw_file data/us/membership-russell-3000.txt --ticker_file data/us/r3000.txt

- download ash, bsh, asz, bsz from
    http://stock.finance.qq.com/hqing/hqst/paiminglist1.htm
    ./download_china_tickers.py --category ash --num_pages 18 --download_dir data/china/ash/
    ./download_china_tickers.py --category bsh --num_pages 1 --download_dir data/china/bsh/
    ./download_china_tickers.py --category asz --num_pages 29 --download_dir data/china/asz/
    ./download_china_tickers.py --category bsz --num_pages 1 --download_dir data/china/bsz/
- extract tickers
    ./extract_china_tickers.py --base_dir data/china/ --categories ash,bsh,asz,bsz --ticker_file data/china/tickers.txt

- download exchange rates from
    http://www.currency-converter.org.uk/currency-rates/historical/table/USD-CNY.html

