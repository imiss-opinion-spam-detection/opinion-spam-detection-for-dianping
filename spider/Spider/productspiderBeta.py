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
import Cookie
import UserAgent


def getresultstr(result, number):  # convert list to unicode string
    resultstr = u""
    for i in range(number, len(result) - number):
        resultstr += result[i]
    return resultstr


def getnameid(html):
    getnameid = re.compile(r'(?<=user-id\=\")\d+')
    result = getnameid.findall(html)
    resultstr = getresultstr(str(result), 1)
    return resultstr


def getname(html):
    getname = re.compile(r'<p class="name"><a target="_blank" title="" href="/member/\d+">[\s\S]*?</a></p>')
    resultware = getname.findall(html)
    result = re.sub(r'<p class="name"><a target="_blank" title="" href="/member/\d+">|</a></p>', "", str(resultware))
    resultstr = getresultstr(result, 1)
    return resultstr


def getcontribution(html):
    soup = BeautifulSoup(html,"lxml")
    resultware = soup.find_all('span', class_="user-rank-rst")
    getnumber = re.compile(r'\d+\-\d+')
    result = getnumber.findall(str(resultware))
    resultstr = getresultstr(str(result), 2)
    return resultstr


def getreview(html):
    getreviewcontent = re.compile(r'<div class="J_brief-cont">[\s\S]*?</div>')
    middleware = getreviewcontent.findall(html)
    resultware = re.sub(r'<div class="J_brief-cont">|</div>', "", str(middleware))
    result = re.sub(r'\s+|\\n', "", str(resultware))
    resultstr = getresultstr(result, 1)
    return resultstr


def getuserinforank(html):
    getuserinforanknumber = re.compile(r'(?<=class="item-rank-rst irr-star)\d+')
    result = getuserinforanknumber.findall(html)
    resultstr = getresultstr(str(result), 1)
    return resultstr


def gettime(html):
    gettime = re.compile(r'(?<=<span class="time">)[\d\-]{5,8}')
    result = gettime.findall(html)
    result = str(result)
    resultstr = getresultstr(result, 2)
    return resultstr


def getcost(html):
    getcost = re.compile(r'(?<=<span class="comm-pre">)[\s\S]*?(?=</span>)')
    result = getcost.findall(html)
    resultstr = getresultstr(str(result), 1)
    return resultstr


def getshop(html,url):
    GetShopNumber = re.compile(r'(?<=shop/)[\d]*?(?=/review_all)')
    ShopNumber = GetShopNumber.findall(url)
    ShopNumberResult = getresultstr(ShopNumber,0)
    ShopNumberResult = ShopNumberResult.strip(" ")
    getshop = re.compile(r'(?<=<h2><a href="/shop/' + ShopNumberResult + '">)[\s\S]*?(?=</a></h2>)')
    result = getshop.findall(html)
    resultstr = getresultstr(result,0)
    return resultstr.strip(" ")


def getrst1(html):  # the first classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[0]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def getrst2(html):  # the second classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[1]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def getrst3(html):  # the third classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[2]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def getProxyIP():
    IPHtml = urllib2.urlopen("http://127.0.0.1:8000/?types=1")
    IPPool = IPHtml.read().decode('utf-8')
    patten = re.compile('"(.*?", \d+)]')
    IPList = patten.findall(IPPool)
    for index, item in enumerate(IPList):
        IPList[index] = item.replace("\", ", ":")
    return IPList

def gethtml(url):
    global ProxyIPList
    global UsingTimes
    global CurrentIP
    global ErrorTimes

    if UsingTimes > 100:
        UsingTimes = 0
        CurrentIP = random.choice(ProxyIPList)
    UsingTimes += 1

    # if len(ProxyIPList) == 0 :
    #    time.sleep(1)
    #   ProxyIPList = getProxyIP()
    try:
        #filename = 'cookie.txt'
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
            'Cookie': "aburl=1; "
                      "cy=1;"
                      " cye=shanghai;"
                      "c776986c-29a7-4eff-ab41-12d3b0126de7.1471956749"
                      " JSESSIONID="+random.choice(Cookie.COOIKE_LIST)+";",
            'X-Forwared-For':CurrentIP,
            'Connection': 'keep-alive',
            'Cache-Control': 'no-store',#'max-age=0',
            'Upgrade-Insecure-Requests': '1',

        }


        data = None
        request = urllib2.Request(url, data, headers)  # setrequest
        result = opener.open(request)
        html = result.read().decode('utf-8')
        #cookieJar.save(ignore_discard=True, ignore_expires=True)
        if html.find(">验证码<") != -1:
            print "vcode:",url
            CurrentIP = random.choice(ProxyIPList)
            if ErrorTimes > 10:
                ErrorTimes = 0
                ProxyIPList = getProxyIP()
                CurrentIP = random.choice(ProxyIPList)
            ErrorTimes += 1
            time.sleep(5)
            return gethtml(url)
        else :
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
        return gethtml(url)


def getcitylist(html):
    time.sleep(1)
    getcitywareurl = re.compile(r'<a href="/[\s\S]*?</a>')
    cityurlware = getcitywareurl.findall(html)
    getcityurl = re.compile(r'href="/[\s\S]*?"')
    cityurl = getcityurl.findall(str(cityurlware))
    result = re.sub(r'href=|"|\s|\'', "", str(cityurl))
    result = result.split(',')
    number = len(result)
    cityurllist = []
    for i in range(3, number - 1):
        urlcity = "https://www.dianping.com" + str(result[i])
        cityurllist.append(urlcity)
    return cityurllist


def getcategoryurllist(cityurl):
    time.sleep(0.5)
    cityhtml = gethtml(cityurl)
    getcategorylist = re.compile(r'<a data-key="\d+" href="[\s\S]*?">[\s\S]*?</a>')
    middleware = getcategorylist.findall(cityhtml)
    for index,value in enumerate(middleware):
        if value.find("其他") != -1:
            number = index
            break
    middleware = middleware[:number+1]
    getcategoryhref = re.compile(r'href="[\s\S]*?"')
    resultware = getcategoryhref.findall(str(middleware))
    result = re.sub(r'href=|"|\'|\s|\[|\]', "", str(resultware))
    result = result.split(",")
    categoryurllist = []
    for i in result:
        categoryurl = "https://www.dianping.com" + str(i)
        categoryurllist.append(categoryurl)
    return categoryurllist
    # Checked

def getareaurllist(categoryurl):
    time.sleep(0.5)
    categoryhtml = gethtml(categoryurl)
    getareaurlblock = re.compile(r'(?<=<div id="region-nav" class="nc-items">)[\S\s]*?(?=</div>)')
    resultblock = getareaurlblock.findall(categoryhtml)

    getareaurlware = re.compile(r'href="/search/category/\d+/\d+/g\d+[rc]\d+')
    resultware = getareaurlware.findall(str(resultblock))
    result = re.sub(r'href=|\"|\'|\[|\]|\s|u|#nav-tab\|0\|1', "", str(resultware))
    result = result.split(",")
    areaurllist = []
    for i in result:
        areaurl = "https://www.dianping.com" + str(i)
        areaurllist.append(areaurl)
    return areaurllist
    # Checked


def getshopurllist(shopeachlisturl):
    shopurlhtml = gethtml(shopeachlisturl)
    getshopurl = re.compile(r'<a target="_blank" href="/shop/\d+(?=/review")')
    resultware = getshopurl.findall(shopurlhtml)
    result = re.sub(r'<a target="_blank" href=|\"|\'|\[|\]|\s|u', "", str(resultware))
    result = result.split(",")
    shopurllist = []
    for i in result:
        shopurl = "https://www.dianping.com" + str(i)
        shopurllist.append(shopurl)
    return shopurllist
    # Checked


def getpagenumber(url):
    html = gethtml(url)
    getpagenumber = re.compile(r'title\="\d+">\d+</a>')
    pagenumberware = getpagenumber.findall(html)
    if pagenumberware == []:
        return 1
    getpageinnernumber = re.compile(r'\d+')
    pagenumber = getpageinnernumber.findall(str(pagenumberware[-1]))
    pagenumber = int(pagenumber[1])
    return pagenumber


# Read the Record
File = open("E:/SpamDetection/Spiders/Spider/SpiderPosition.txt","r")
SpiderPosition = File.readlines()
File.close()
ScanRecord = string.atoi(SpiderPosition[0].strip("\n"))
CategoryRecord = string.atoi(SpiderPosition[1].strip("\n"))
AreaRecord = string.atoi(SpiderPosition[2].strip("\n"))
ShopRecord = string.atoi(SpiderPosition[3].strip("\n"))
PageRecord = string.atoi(SpiderPosition[4].strip("\n"))

# Get the Proxy IP
ProxyIPList = getProxyIP()
CurrentIP = random.choice(ProxyIPList)
UsingTimes = 0
ErrorTimes = 0

'''
# Traverse the city
rooturl="https://www.dianping.com/citylist/citylist?citypage=1"
roothtml=gethtml(rooturl)
cityurllist=getcitylist(roothtml)
for cityurl in cityurllist:
'''
cityurl = "https://www.dianping.com/shanghai"
categoryurllist = getcategoryurllist(cityurl)[CategoryRecord:]
for category_index,categoryurl in enumerate(categoryurllist):
    print "categoryurl:", categoryurl
    areaurllist = getareaurllist(categoryurl)[AreaRecord:]

    for area_index,areaurl in enumerate(areaurllist):
        print "areaurl:", areaurl

        if ScanRecord == 0:
            shoplistpagenumber = getpagenumber(areaurl)  # togetpagenumber
            shopurllist = []
            print "Scan Shops"
            for y in range(1, shoplistpagenumber + 1):
                print str(y) + "/" + str(shoplistpagenumber)
                shopeachlisturl = areaurl + "o10p" + str(y)
                shopurllist += getshopurllist(shopeachlisturl)
                time.sleep(1)

            if len(list(set(shopurllist))) == len(shopurllist):
                File = open("E:/SpamDetection/Spiders/Spider/ShopList.txt","w")
                for i in shopurllist:
                    File.write(i+"\n")
                File.close()
                ScanRecord = 1
                print "Scan Finished"
                print
            else :
                print "Scan Error: Scan Incomplete"
                exit()
        else :
            File = open("E:/SpamDetection/Spiders/Spider/ShopList.txt","r")
            shopurllist = File.readlines()
            for index,value in enumerate(shopurllist):
                shopurllist[index] = value.strip("\n")
            File.close()

        shopurllist = shopurllist[ShopRecord:]

        print "Start Spider"
        for shop_index,shopurl in enumerate(shopurllist):
            url = shopurl + "/review_all?pageno=1"  # togetpagenumber
            pagenumber = getpagenumber(url)
            print
            print "Length:"
            print "CategoryNumber:",CategoryRecord , " + " , len(categoryurllist)
            print "AreaNumber:",AreaRecord, " + " , len(areaurllist)
            print "ShopNumber:",ShopRecord," + ",len(shopurllist)
            print "PageNumber:",PageRecord,"-",pagenumber
            print

            for x in range(1+PageRecord, pagenumber + 1):
                #print "PageNumber",x
                url = shopurl + "/review_all?pageno=" + str(x)
                result = []
                while not result:     # Check Whether result is empty
                    html = gethtml(url)
                    shop = getshop(html, url)
                    getcontent = re.compile(r'<li id="rev_\d+" data-id="\d+">[\s\S]*?<div class="mode-tc respond Hide">')
                    result = getcontent.findall(html)
                    if not result:
                        Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "\n"
                        File = open("Error.log","a")
                        File.write(Time)
                        File.write(url+"\n")
                        File.write(html+"\n\n")
                        File.close()
                        print "Error:Result is Empty"
                        print url
                        print
                for i in result:
                    nameid = getnameid(i)
                    name = getname(i)
                    contribution = getcontribution(i)
                    userinforank = getuserinforank(i)
                    review = getreview(i)
                    timet = gettime(i)
                    cost = ""  # getcost(i)
                    rst1 = getrst1(i)
                    rst2 = getrst2(i)
                    rst3 = getrst3(i)
                    try:
                        #a=0
                        #print
                        #print "ReviewNumber",i
                        print "NameID",nameid[2:-1]
                       # print name.decode('unicode_escape')
                        #print contribution
                        #print userinforank.decode('unicode_escape')
                        #print review.decode('unicode_escape')
                        print "Time",timet[1:]
                        print "Shop",shop
                        #print cost.decode('unicode_escape')
                        #print rst1
                        #print rst2
                        #print rst3
                    except:
                        pass

                    db = MySQLdb.connect(user='root', passwd='root', db='dianping', host='localhost',
                                         charset='utf8')
                    cursor = db.cursor()
                    sql = 'INSERT INTO `dianpingcontent`(`nameid`,`name`,`contribution`,`userinforank`,`review`,`time`,`shop`,`cost`,`rst1`,`rst2`,`rst3`)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                    val = (
                        nameid[2:-1],
                        name.decode('unicode_escape')[2:-1],
                        contribution,
                        userinforank.decode('unicode_escape')[2:-1],
                        review.decode('unicode_escape')[2:-1],
                        timet[1:],
                        shop,
                        cost,
                        rst1,
                        rst2,
                        rst3
                    )
                    try:
                        cursor.execute(sql % val)
                        db.commit()
                    except:
                        db.rollback()
                    db.close()

                print
                print "-------------------"
                print "Inner Loop Finished"
                print "-------------------"
                print url
                print "ScanRecord",ScanRecord
                print "CategoryIndex",category_index + CategoryRecord
                print "AreaIndex",area_index + AreaRecord
                print "ShopIndex",shop_index + ShopRecord
                print "PageNumber",x - 1 + 1
                print
                time.sleep(3)

            print "Init PageRecord"
            PageRecord = 0
            time.sleep(3)

        print "Init ShopRecord"
        ShopRecord = 0
        ScanRecord = 0
        time.sleep(3)

    print "Init AreaRecord"
    AreaRecord = 0
    time.sleep(3)

print "Init CategoryRecord"
CategoryRecord = 0

