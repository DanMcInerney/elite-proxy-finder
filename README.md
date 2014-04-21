elite-proxy-finder
==================

Finds elite anonymity (L1) HTTP proxies using gatherproxy.com and letushide.com then tests them all concurrently. Scrapes 25 L1 proxies which were checked on by gatherproxy.com within the last 2-5 minutes and all L1 proxies checked within the last 3 days by letushide.com. Tests them all against 3 IP checking URLs including one which is https to check for that compatibility. If it finds the proxy IP address in the HTML of the page then it will display the time it took to get a response,
otherwise it will display the error that occurred.


Usage:
------
```shell
python elite-proxy-finder.py
```
Display the time it took each proxy to send a request and receive a reply from https://yahoo.com printing the fastest ones first.

```shell
python elite-proxy-finder.py -s 5
```
Print only the first 5 proxy results.



Requirements:
------
* Tested on Kali 1.0.6
* Python 2.7
    -gevent
    -requests


NOTE FOR KALI USERS:


Kali has gevent 0.13 in its repo and you will need gevent 1.0 to get the -s option working.

```shell
apt-get install python-dev gevent
pip install --upgrade gevent
```

