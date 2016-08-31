# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import re
import urllib2 
from bs4 import BeautifulSoup
import cookielib
import MySQLdb
import time
def gethtml(url):
    cookieJar = cookielib.MozillaCookieJar()#setcookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    headers={#set headers
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5584.400',
        'Accept'    :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control':'max-age=0',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'www.dianping.com',
        'Upgrade-Insecure-Requests':'1',
        'Cookie':'showNav=javascript:; navCtgScroll=0; _hc.v=69ec1d48-6214-a4a6-3e4f-8d3eb5c8f2cb.1467510663; __utma=1.1749497646.1467510663.1467510663.1467510663.1; __utmz=1.1467510663.1.1.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%A4%A7%E4%BC%97%E7%82%B9%E8%AF%84%E7%BD%91; PHOENIX_ID=0a0302bc-155d90b6be9-c8936; s_ViewType=10; JSESSIONID=7299F758AA33C769D888B5CF53E1A88C; aburl=1; cy=17; cye=xian'
    }
    data=None
    request=urllib2.Request(url,data,headers)#setrequest
    result = opener.open(request)
    html = result.read().decode('unicode_escape')
    return html

def getresultstr(result,number):#convert list to unicode string 
    resultstr=u""
    for i in range(number,len(result)-number):
        resultstr+=result[i]
    return resultstr

def getname(html):
    getname = re.compile(r'(?<=<h2 class="name">)[\s\S]*?(?=</h2>)')
    result=getname.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getfollows(html):
    soup = BeautifulSoup(html)
    resultware=soup.find_all('strong')
    getfollows=re.compile(r'\d+')
    result=getfollows.findall(str(resultware[2]))
    resultstr=getresultstr(str(result),1)
    return resultstr

def getfans(html):
    soup = BeautifulSoup(html)
    resultware=soup.find_all('strong')
    getfans=re.compile(r'\d+')
    result=getfans.findall(str(resultware[3]))
    resultstr=getresultstr(str(result),1)
    return resultstr

def getinteraction(html):
    soup = BeautifulSoup(html)
    resultware=soup.find_all('strong')
    getinteraction=re.compile(r'\d+')
    result=getinteraction.findall(str(resultware[4]))
    resultstr=getresultstr(str(result),1)
    return resultstr

def getcontribution(html):
    getcontribution=re.compile(r'(?<=<span id="J_col_exp">)\d+(?=<i class="user-aurr">)')
    result=getcontribution.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getrank(html):
    getrank=re.compile(r'(?<=<span class="col-exp">社区等级：</span>)[\s\S]*?(?=</p>)')
    result=getrank.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr


def getfirsttime(html):
    getfirsttime=re.compile(r'(?<=<span class="col-exp">注册时间：</span>)[\s\S]*?(?=</p>)')
    result=getfirsttime.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getlasttime(html):
    getlasttime=re.compile(r'(?<=<span class="col-exp">最后登录：</span>)[\s\S]*?(?=</p>)')
    result=getlasttime.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getreviews(html):
    getreviews=re.compile(r'(?<=点评\()[\s\S]*?(?=\)</a>)')
    result=getreviews.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getwishlists(html):
    getwishlists=re.compile(r'(?<=收藏\()[\s\S]*?(?=\)</a>)')
    result=getwishlists.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getcheckin(html):
    getcheckin=re.compile(r'(?<=签到\()[\s\S]*?(?=\)</a>)')
    result=getcheckin.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getphotos(html):
    getphotos=re.compile(r'(?<=图片\()[\s\S]*?(?=\)</a>)')
    result=getphotos.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getmylists(html):
    getmylists=re.compile(r'(?<=榜单\()[\s\S]*?(?=\)</a>)')
    result=getmylists.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

def getgroups(html):
    getgroups=re.compile(r'(?<=/groups" onclick="pageTracker._trackPageview\(\'dp_mypage_post\'\);" title="" class="col-link">帖子\()[\s\S]*?(?=\)</a>)')
    result=getgroups.findall(html)
    resultstr=getresultstr(str(result),1)
    return resultstr

url="https://www.dianping.com/member/2"
html=gethtml(url)

name=getname(html)
follows=getfollows(html)
fans=getfans(html)
interaction=getinteraction(html)
contribution=getcontribution(html)
rank=getrank(html)
firsttime=getfirsttime(html)
lasttime=getlasttime(html)
reviews=getreviews(html)
wishlists=getwishlists(html)
checkin=getcheckin(html)
photos=getphotos(html)
mylists=getmylists(html)
groups=getgroups(html)

print name.decode('unicode_escape')
print follows
print fans
print interaction
print contribution
print rank.decode("utf-8")
print firsttime
print lasttime
print reviews
print wishlists
print checkin
print photos
print mylists
print groups