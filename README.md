elite-proxy-finder
==================

Finds elite anonymity (L1) HTTP proxies using gatherproxy.com and letushide.com then tests them all concurrently. Scrapes 25 L1 proxies which were most recently checked on by gatherproxy.com (within the last 2-5 minutes) and all L1 proxies checked within the last 3 days by letushide.com. This will usually lead to 100+ recently checked proxies all tested locally in <20 seconds (dependant on your internet speed).


Usage:
------
```shell
python elite-proxy-finder.py
```
Display the time it took each proxy to send a request and receive a reply from https://yahoo.com printing the fastest ones first.

```shell
python elite-proxy-finder.py -s 5
```
Print only the 5 fastest proxies amongst the entire proxy selection.
