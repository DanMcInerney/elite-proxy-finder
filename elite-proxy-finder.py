#!/usr/bin/env python2

from gevent import monkey
monkey.patch_all()

import requests
import ast
import gevent
import sys, re, time, os, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show', help='Show this number of results. Example: -s 5 will show the 5 fastest proxies then stop')
    return parser.parse_args()
	
class find_http_proxy():
    ''' Will only gather L1 (elite anonymity) proxies
    which should not give out your IP or advertise
    that you are using a proxy at all '''
    
    def __init__(self, args):
        self.checked_proxies = []
        self.proxy_list = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'}
        self.show = args.show
        self.proxy_counter = 0
            
    def run(self):
        ''' Gets raw high anonymity (L1) proxy data then calls make_proxy_list() 
        Currently parses data from gatherproxy.com and letushide.com '''
        letushide_list = self.letushide_req()
        gatherproxy_list = self.gatherproxy_req()
        
        self.proxy_list.append(letushide_list)
        self.proxy_list.append(gatherproxy_list)
        # Flatten list of lists (1 master list containing 1 list of ips per proxy website)
        self.proxy_list = [ips for proxy_site in self.proxy_list for ips in proxy_site]
        
        print '[*] %d high anonymity proxies found' % len(self.proxy_list)
        print '[*] Testing proxy speed against https://www.yahoo.com ...'
        print ''
        print '     Time elapsed         Proxy'
        
        self.proxy_checker()
            
    def letushide_req(self):
        ''' Make the request to the proxy site and create a master list from that site '''
        letushide_ips = []
        for i in xrange(1,20): # can search maximum of 20 pages
            try:
                url = 'http://letushide.com/filter/http,hap,all/%s/list_of_free_HTTP_High_Anonymity_proxy_servers' % str(i)
                r = requests.get(url, headers=self.headers)
                html = r.text
                ips = self.parse_letushide(html)
            
                # Check html for a link to the next page
                if '/filter/http,hap,all/%s/list_of_free_HTTP_High_Anonymity_proxy_servers' % str(i+1) in html:
                    pass
                else:
                    letushide_ips.append(ips)
                    break
                letushide_ips.append(ips)
            except:
                print '[!] Failed get reply from %s' % url
                break

        # Flatten list of lists (1 list containing 1 list of ips for each page)
        letushide_list = [item for sublist in letushide_ips for item in sublist]
        return letushide_list
            
    def parse_letushide(self, html):
        ''' Parse out list of IP:port strings from the html '''
        # \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}  -  matches IP addresses
        # </a></td><td>  -  is in between the IP and the port
        # .*?<  -  match all text (.) for as many characters as possible (*) but don't be greedy (?) and stop at the next greater than (<)
        raw_ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}</a></td><td>.*?<', html)
        ips = []
        for ip in raw_ips:
            ip = ip.replace('</a></td><td>', ':')
            ip = ip.strip('<')
            ips.append(ip)
        return ips

    def gatherproxy_req(self):
        r = requests.get('http://gatherproxy.com/proxylist/anonymity/?t=Elite', headers = self.headers)
        lines = r.text.splitlines()
        gatherproxy_list = self.parse_gp(lines)
        return gatherproxy_list
            
    def parse_gp(self, lines):
        ''' Parse the raw scraped data '''
        gatherproxy_list = []
        for l in lines:
            if 'proxy_ip' in l.lower():
                l = l.replace('gp.insertPrx(', '')
                l = l.replace(');', '')
                l = l.replace('null', 'None')
                l = l.strip()
                l = ast.literal_eval(l)
                            
                proxy = '%s:%s' % (l["PROXY_IP"], l["PROXY_PORT"])
                gatherproxy_list.append(proxy)
                #ctry = l["PROXY_COUNTRY"]
        return gatherproxy_list
            
    def proxy_checker(self):
        ''' Concurrency stuff here '''
        jobs = [gevent.spawn(self.proxy_checker_req, proxy) for proxy in self.proxy_list]
        gevent.joinall(jobs)

    def proxy_checker_req(self, proxy):
        ''' See how long each proxy takes to open https://www.yahoo.com '''
        try:
            check = requests.get('https://www.yahoo.com',
                                headers = self.headers,
                                proxies = {'http':'http://'+proxy},
                                timeout=10)
            time = str(check.elapsed)
        except:
            time = 'Error'

        print '    %s | %s' % (time.ljust(14), proxy)
        self.limiter()
    
    def limiter(self):
        ''' Kill the script if user supplied limit (-s argument) is reached '''
        if self.show:
            self.proxy_counter += 1
            if self.proxy_counter == int(self.show):
                gevent.shutdown
                sys.exit()

P = find_http_proxy(parse_args())
P.run()
