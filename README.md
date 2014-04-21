elite-proxy-finder
==================

Finds elite anonymity (L1) HTTP proxies using gatherproxy.com and letushide.com then tests them all concurrently. Scrapes 25 L1 proxies which were checked on by gatherproxy.com within the last 2-5 minutes and all L1 proxies checked within the last 3 days by letushide.com. Tests them all against 3 IP checking URLs including one which is https to check for that compatibility. If it finds the proxy IP address in the HTML of the page then it will display the time it took to get a response,
otherwise it will display the error that occurred.


Requirements:
------
* Tested on Kali 1.0.6
* Python 2.7
  * gevent
  * requests

Kali has gevent 0.13 in its repo and you will need gevent 1.0 to get the -s option working.
```shell
apt-get install python-dev gevent
pip install --upgrade gevent
```


Usage:
------
```shell
python elite-proxy-finder.py
```
Display the time it took each proxy to send a request and receive a reply from the 3 test URLs displaying the results as they come in, or show the error that occurred

```shell
python elite-proxy-finder.py -s 10
```
Show only the first 10 proxy results.



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
* [danmcinerney.org](danmcinerney.org)
* [![Flattr this](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=DanMcInerney&url=https://github.com/DanMcInerney/elite-proxy-finder&title=elite-proxy-finder&language=&tags=github&category=software) 

