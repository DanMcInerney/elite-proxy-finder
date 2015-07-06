elite-proxy-finder
==================

This script was not working for a few months. I just fixed it 7/6/15. Only uses gatherproxy.com now.

Finds elite anonymity (L1) HTTP proxies then tests them all in parallel. Tests each proxy against 3 IP checking URLs including one which is HTTPS to make sure it can handle HTTPS requests. Then checks the proxy headers to confirm it's an elite L1 proxy that will not leak any extra info. By default the script will only print the proxy IP, request time, and country code of proxies that pass all four tests but you can see all the results including errors in any of the tests with the -a (--all) option. 

Requirements:
------
* Tested on Kali 1.0.6
* Python 2.7
  * gevent 1.0
  * requests 1.2.0+ 

If you are on a system with requests <1.2.0 you won't see any output because every test will result in an error referring to the request not having an attribute "elapsed". Use the -a option to check the errors.

Kali has gevent 0.13 in its repo and you will need gevent 1.0 if you want the -s option to work. Works fine with 0.13 other than that.
```
apt-get install python-dev python-gevent
pip install --upgrade gevent
```

Usage:
------
```python elite-proxy-finder.py```

Show proxies that pass all four tests, their country code, and the time it took for each request to complete. Prints the fastest proxies first.

```python elite-proxy-finder.py -s 10```

Show only the fastest 10 proxy results.

```python elite-proxy-finder.py -a```

Show all proxy results including the errors that occurred.

```python elite-proxy-finder.py -q```

Print only the IP address and port of proxies that pass all four tests.



License
-------

Copyright (c) 2014, Dan McInerney
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Dan McInerney nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


***
* [danmcinerney.org](http://danmcinerney.org)
* [![Flattr this](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=DanMcInerney&url=https://github.com/DanMcInerney/elite-proxy-finder&title=elite-proxy-finder&language=&tags=github&category=software) 

