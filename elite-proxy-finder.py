#!/usr/bin/env python2

from gevent import monkey
monkey.patch_all()

import requests
import ast
import gevent
import sys, re, time, os, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--show', help='Show this number of results. Example: "-s 5" will show the 5 fastest proxies then stop')
    parser.add_argument('-a', '--all', help='Show all proxy results including the ones that failed 1 of the 3 tests', action='store_true')
    return parser.parse_args()

class find_http_proxy():
    ''' Will only gather L1 (elite anonymity) proxies
    which should not give out your IP or advertise
    that you are using a proxy at all '''

    def __init__(self, args):
        self.checked_proxies = []
        self.proxy_list = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36'}
        self.show_num = args.show
        self.show_all = args.all
        self.errors = []
        self.print_counter = 0

    def run(self):
        ''' Gets raw high anonymity (L1) proxy data then calls make_proxy_list()
        Currently parses data from gatherproxy.com and letushide.com '''

        try:
            letushide_list = self.letushide_req()
        except Exception:
            print '[!] Failed to get proxy list from letushide.com'

        try:
            gatherproxy_list = self.gatherproxy_req()
        except Exception:
            print '[!] Failed to get proxy list from gatherproxy.com'

        self.proxy_list.append(letushide_list)
        self.proxy_list.append(gatherproxy_list)
        # Flatten list of lists (1 master list containing 1 list of ips per proxy website)
        self.proxy_list = [ips for proxy_site in self.proxy_list for ips in proxy_site]
        self.proxy_list = list(set(self.proxy_list)) # Remove duplicates

        print '[*] %d unique high anonymity proxies found' % len(self.proxy_list)
        print '[*] Testing proxy speeds ...'
        print ''
        print '      Proxy           | CC  |       Domain         | Time/Errors'

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
        try:
            gevent.joinall(jobs)
        except KeyboardInterrupt:
            sys.exit('[-] Ctrl-C caught, exiting')

    def proxy_checker_req(self, proxy):
        ''' See how long each proxy takes to open each URL '''
        proxyip = str(proxy.split(':', 1)[0])

        # A lot of proxy checker sites give a different final octet for some reason
        proxy_split = proxyip.split('.')
        first_3_octets = '.'.join(proxy_split[:3])+'.'

        results = []
        urls = ['http://www.ipchicken.com', 'http://whatsmyip.net/', 'https://www.astrill.com/what-is-my-ip-address.php']
        for url in urls:
            try:
                check = requests.get(url,
                                    headers = self.headers,
                                    proxies = {'http':'http://'+proxy,
                                               'https':'http://'+proxy},
                                    timeout = 15)

                time = str(check.elapsed)
                html = check.text
                html_lines = html.splitlines()
                time = self.check_ip_on_page(time, html_lines, first_3_octets)
                url = self.url_shortener(url)

                results.append((time, proxy, url))

            except Exception as e:
                #raise
                time = self.error_handler(e)
                url = self.url_shortener(url)
                results.append((time, proxy, url))

        self.print_handler(results, proxyip)

    def print_handler(self, results, proxyip):
        if self.show_all:
            country_code = self.get_country_code(proxyip)
            self.printer(results, country_code)
            self.print_counter += 1
        else:
            passed_all = self.passed_all_tests(results)
            if passed_all:
                country_code = self.get_country_code(proxyip)
                self.printer(results, country_code)
                self.print_counter += 1

        if self.show_num:
            self.limiter()


    def printer(self, results, country_code):
        ''' Creates the output '''
        counter = 0
        print '-------------------------------------------------------------------'
        for r in results:
            counter += 1
            time = r[0]
            proxy = r[1]
            url = r[2]
            #country_code = r[3]

            # Only print the proxy once, on the second print job
            if counter == 2:
                print '%s | %s | %s | %s' % (proxy.ljust(21), country_code, url.ljust(20), time)
                #print '%s | %s | %s | %s' % (proxy.ljust(21), '   ', url.ljust(20), time)
            else:
                print '%s | %s | %s | %s' % (' '.ljust(21), '   ', url.ljust(20), time)

    def get_country_code(self, proxyip):
        ''' Get the 3 letter country code of the proxy using geoiptool.com
        Would use the geoip library, but it requires a local DB and what
        is the point of that hassle other than marginal speed improvement '''
        cc_line_found = False
        cc = 'N/A'

        r = requests.get('http://www.geoiptool.com/en/?IP=%s' % proxyip)
        html = r.text
        html_lines = html.splitlines()
        for l in html_lines:
            if cc_line_found == True:
                cc = l.split('(', 1)[1].split(')', 1)[0]
                break
            if 'country code:' in l.lower():
                cc_line_found = True

        #if cc == 'N/A':
        #    print proxyip, html
        return cc

    def check_ip_on_page(self, time, html_lines, first_3_octets):
        ''' Check for the IP on the page, for a captcha, and for 'access denied' mesg '''
        ip_found = False

        for l in html_lines:
            if first_3_octets in l:
                ip_found = True
            if 'captcha' in l.lower():
                time = time + ' - Captcha detected'
            if 'access denied' in l.lower():
                time = time + ' - Access denied'
                break

        if ip_found == False:
            time = 'Err: Page loaded but proxy failed'
        return time

    def error_handler(self, e):
        if 'Cannot connect' in str(e):
            time = 'Err: Cannot connect to proxy'
        elif 'timed out' in str(e).lower():
            time = 'Err: Timed out'
        elif 'retries exceeded' in str(e):
            time = 'Err: Max retries exceeded'
        elif 'Connection reset by peer' in str(e):
            time = 'Err: Connection reset by peer'
        elif 'readline() takes exactly 1 argument (2 given)' in str(e):
            time = 'Err: SSL error'
        else:
            time = 'Err: '+str(e)
        return time

    def url_shortener(self, url):
        if 'ipchicken' in url:
            url = 'http://ipchicken.com'
        elif 'whatsmyip' in url:
            url = 'http://whatsmyip.net'
        elif 'astrill' in url:
            url = 'https://astrill.com'
        return url

    def passed_all_tests(self, results):
        for r in results:
            time = r[0]
            if 'Err:' in time:
                return False
        return True

    def limiter(self):
        ''' Kill the script if user supplied limit of successful proxy attempts (-s argument) is reached '''
        if self.print_counter >= int(self.show_num):
            sys.exit()

P = find_http_proxy(parse_args())
P.run()
