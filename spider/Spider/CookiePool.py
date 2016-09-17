# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
import re
import urllib2
from bs4 import BeautifulSoup
import cookielib
import MySQLdb
import time
import random
import UserAgent

global ProxyIPList


def getProxyIP():
    IPHtml = urllib2.urlopen("http://127.0.0.1:8000/?types=1")
    IPPool = IPHtml.read().decode('utf-8')
    patten = re.compile('"(.*?", \d+)]')
    IPList = patten.findall(IPPool)
    for index, item in enumerate(IPList):
        IPList[index] = item.replace("\", ", ":")
    return IPList

def GetCookie(url):
    global ProxyIPList
    global UsingTimes
    global CurrentIP
    global ErrorTimes
    global CookieNumber
    global RunningTimes
    global Cookie

    if UsingTimes > 100:
        UsingTimes = 0
        CurrentIP = random.choice(ProxyIPList)
    UsingTimes += 1

    try:
        #filename = 'cookie' + str(CookieNumber) + ".txt"
        cookieJar = cookielib.MozillaCookieJar()  # setcookie
        #cookieJar.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        proxy = {'http': CurrentIP}
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor(cookieJar))
        headers = {  # set headers
            'Host': 'www.dianping.com',
            'User-Agent': random.choice(UserAgent.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'DNT':"1",
            'Cookie':
                "cy=1;"
                "cye=shanghai;"
                "_hc.v=c776986c-29a7-4eff-ab41-12d3b0126de7.1471956749;"
                "JSESSIONID=A8775FC6271A31BBEE3ECBBD4749BEB4,",
            'X-Forwared-For':CurrentIP,
            'Connection': 'keep-alive',
            'Cache-Control': 'no-store',#'max-age=0',
            'Upgrade-Insecure-Requests': '1',

        }
        data = None
        request = urllib2.Request(url, data, headers)  # setrequest
        result = opener.open(request)
        html = result.read().decode('utf-8')
        for i in cookieJar:
            print i
            if i.name == "JSESSIONID":
                Cookie.append("\""+i.value+"\",\n")
                break
        #cookieJar.save(ignore_discard=True, ignore_expires=True)
        CookieNumber += 1
        print str(CookieNumber-1)+"/"+str(RunningTimes)
        return html
    except Exception, e:
        print Exception, e
        print ErrorTimes, ":", CurrentIP
        print "url:", url
        CurrentIP = random.choice(ProxyIPList)
        if ErrorTimes > 10:
            ErrorTimes = 0
            ProxyIPList = getProxyIP()
            CurrentIP = random.choice(ProxyIPList)
        ErrorTimes += 1
        time.sleep(5)
        return GetCookie(url)


if __name__ == "__main__" :
    ProxyIPList = getProxyIP()
    CurrentIP = random.choice(ProxyIPList)
    UsingTimes = 0
    ErrorTimes = 0
    CookieNumber = 1
    Cookie = []

    # Get Argument from System
    if len(sys.argv) == 0 or len(sys.argv) == 1 :
        RunningTimes = string.atoi(raw_input("Please input Cookie Number: "))
    elif len(sys.argv) == 2:
        if str(sys.argv[1][0] == "-") :
            RunningTimes = string.atoi(sys.argv[1][1:])
        else :
            print "Error: Wrong Argument"
            exit()
    else :
        print "Error: Too Many Arguments"
        exit()

    # Get Cookies
    print "-------------------"
    print "Start Cookie Spider"
    print "-------------------"
    while CookieNumber <= RunningTimes:
        url = "http://www.dianping.com/"
        GetCookie(url)
        time.sleep(2)

    # Save Cookies
    Cookie = list(set(Cookie))
    Cookie.insert(0,"COOIKE_LIST = [\n")
    Cookie.append("]")
    file = open("E:/SpamDetection/Spiders/Spider/Cookie.py","w")
    file.writelines(Cookie)
    file.close()
    print "--------------------"
    print "Finished"
    print "Get",len(Cookie)-2,"Cookies"
    print "--------------------"

