elite-proxy-finder
==================

Finds elite anonymity proxies using gatherproxy.com. Just scrapes their first page of L1 proxies and concurrently tests them all against cnn.com so you cross reference gatherproxy's ping rating with a local live test and snag the fastest one. Not sure the timeouts and concurrency are working as well as they should but gets the job done.


Usage:
```shell
python elite-proxy-finder.py
```
