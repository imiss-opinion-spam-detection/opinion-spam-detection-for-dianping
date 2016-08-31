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


def get_result_str(result, number):  # convert list to unicode string
    resultstr = u""
    for i in range(number, len(result) - number):
        resultstr += result[i]
    return resultstr


def get_name_id(html):
    getnameid = re.compile(r'(?<=user-id\=\")\d+')
    result = getnameid.findall(html)
    resultstr = get_result_str(str(result), 1)
    return resultstr


def get_name(html):
    getname = re.compile(r'<p class="name"><a target="_blank" title="" href="/member/\d+">[\s\S]*?</a></p>')
    resultware = getname.findall(html)
    result = re.sub(r'<p class="name"><a target="_blank" title="" href="/member/\d+">|</a></p>', "", str(resultware))
    resultstr = get_result_str(result, 1)
    return resultstr


def get_contribution(html):
    soup = BeautifulSoup(html)
    resultware = soup.find_all('span', class_="user-rank-rst")
    getnumber = re.compile(r'\d+\-\d+')
    result = getnumber.findall(str(resultware))
    resultstr = get_result_str(str(result), 2)
    return resultstr


def get_review(html):
    getreviewcontent = re.compile(r'<div class="J_brief-cont">[\s\S]*?</div>')
    middleware = getreviewcontent.findall(html)
    resultware = re.sub(r'<div class="J_brief-cont">|</div>', "", str(middleware))
    result = re.sub(r'\s+|\\n', "", str(resultware))
    resultstr = get_result_str(result, 1)
    return resultstr


def get_user_info_rank(html):
    getuserinforanknumber = re.compile(r'(?<=class="item-rank-rst irr-star)\d+')
    result = getuserinforanknumber.findall(html)
    resultstr = get_result_str(str(result), 1)
    return resultstr


def get_time(html):
    gettime = re.compile(r'(?<=<span class="time">)\d{2}\-\d{2}')
    result = gettime.findall(html)
    result = str(result)
    resultstr = get_result_str(result, 2)
    return resultstr


def get_cost(html):
    getcost = re.compile(r'(?<=<span class="comm-per">)[\s\S]*?(?=</span>)')
    result = getcost.findall(html)
    resultstr = get_result_str(result, 1)
    return resultstr


def get_shop(html):
    getshop = re.compile(r'(?<=<h2 class="misc-name">)[\s\S]*?(?=</h2>)')
    result = getshop.findall(html)
    resultstr = get_result_str(str(result), 1)
    return resultstr


def get_rst1(html):  # the first classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[0]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def get_rst2(html):  # the second classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[1]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def get_rst3(html):  # the third classic review
    try:
        getshop = re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
        middleware = getshop.findall(html)
        # middleware=soup.find_all('span',class_="rst")
        result = middleware[2]
        return result
    except Exception, e:
        print Exception, ":", e
        return None


def get_html(url):
    cookieJar = cookielib.MozillaCookieJar()  # setcookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    headers = {  # set headers
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.87 Safari/537.36 QQBrowser/9.2.5584.400',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'showNav=javascript:; navCtgScroll=0; _hc.v=69ec1d48-6214-a4a6-3e4f-8d3eb5c8f2cb.1467510663; __utma=1.1749497646.1467510663.1467510663.1467510663.1; __utmz=1.1467510663.1.1.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%A4%A7%E4%BC%97%E7%82%B9%E8%AF%84%E7%BD%91; PHOENIX_ID=0a0302bc-155d90b6be9-c8936; s_ViewType=10; JSESSIONID=7299F758AA33C769D888B5CF53E1A88C; aburl=1; cy=17; cye=xian'
    }
    data = None
    request = urllib2.Request(url, data, headers)  # setrequest
    result = opener.open(request)
    html = result.read().decode('utf-8')
    return html


def get_citylist(html):
    time.sleep(10)
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


def get_category_urllist(cityurl):
    try:
        time.sleep(5)
        cityhtml = get_html(cityurl)
        getcategorylist = re.compile(r'<a data-key="\d+" href="[\s\S]*?">[\s\S]*?</a>')
        middleware = getcategorylist.findall(cityhtml)
        getcategoryhref = re.compile(r'href="[\s\S]*?"')
        resultware = getcategoryhref.findall(str(middleware))
        result = re.sub(r'href=|"|\'|\s|\[|\]', "", str(resultware))
        result = result.split(",")
        number = len(result)
        categoryurllist = []
        for i in range(0, number):
            categoryurl = "https://www.dianping.com" + str(result[i])
            categoryurllist.append(categoryurl)
        return categoryurllist
    except Exception, e:
        print Exception, "Please check"
        input("Enter to Continue")


def get_area_url_list(categoryurl):
    time.sleep(5)
    categoryhtml = get_html(categoryurl)
    getareaurlware = re.compile(r'href="/search/category/\d+/\d+/g\d+r\d+')
    resultware = getareaurlware.findall(categoryhtml)

    result = re.sub(r'href=|\"|\'|\[|\]|\s|u|#nav-tab\|0\|1', "", str(resultware))
    result = result.split(",")
    number = len(result)
    areaurllist = []
    for i in range(0, number):
        areaurl = "https://www.dianping.com" + str(result[i])
        areaurllist.append(areaurl)
    return areaurllist


def get_shop_url_list(shopeachlisturl):
    shopurlhtml = get_html(shopeachlisturl)
    getshopurl = re.compile(r'<a target="_blank" href="/shop/\d+"')
    resultware = getshopurl.findall(shopurlhtml)
    result = re.sub(r'<a target="_blank" href=|\"|\'|\[|\]|\s|u', "", str(resultware))
    result = result.split(",")
    number = len(result)
    shopurllist = []
    for i in range(0, number):
        shopurl = "https://www.dianping.com" + str(result[i])
        shopurllist.append(shopurl)
    return shopurllist


def get_page_number(url):
    html = get_html(url)
    getpagenumber = re.compile(r'title\="\d+">\d+</a>')
    pagenumberware = getpagenumber.findall(html)
    if pagenumberware == []:
        return 1
    getpageinnernumber = re.compile(r'\d+')
    pagenumber = getpageinnernumber.findall(str(pagenumberware[-1]))
    pagenumber = int(pagenumber[1])
    return pagenumber


'''
rooturl="https://www.dianping.com/citylist/citylist?citypage=1"
roothtml=gethtml(rooturl)
cityurllist=getcitylist(roothtml)
for cityurl in cityurllist:
'''
review_count = 0
# print "Please input the city's name"
city_name = 'xian'
city_url = "https://www.dianping.com/" + city_name
category_url_list = get_category_urllist(city_url)
for category_url in category_url_list:
    area_url_list = get_area_url_list(category_url)
    for area_url in area_url_list:
        shop_list_page_number = get_page_number(area_url)  # togetpagenumber
        for y in range(1, shop_list_page_number + 1):
            shop_each_list_url = area_url + "p" + str(y)
            shop_url_list = get_shop_url_list(shop_each_list_url)
            for shop_url in shop_url_list:
                url = shop_url + "/review_all?pageno=1"  # togetpagenumber
                print url
                pagenumber = get_page_number(url)
                for x in range(1, pagenumber + 1):
                    url = shop_url + "/review_all?pageno=" + str(x)
                    try:
                        html = get_html(url)

                        getcontent = re.compile(
                            r'<li id="rev_\d+" data-id="\d+">[\s\S]*?<div class="mode-tc respond Hide">')
                        result = getcontent.findall(html)
                        contentnumber = len(result)
                        for i in range(0, contentnumber):
                            nameid = get_name_id(result[i])
                            name = get_name(result[i])
                            contribution = get_contribution(result[i])
                            userinforank = get_user_info_rank(result[i])
                            review = get_review(result[i])
                            timet = get_time(result[i])
                            shop = get_shop(result[i])
                            cost = get_cost(result[i])
                            rst1 = get_rst1(result[i])
                            rst2 = get_rst2(result[i])
                            rst3 = get_rst3(result[i])
                            review_count = review_count+1
                            print "Now we have", review_count, "reviews"
                            print "nameid",nameid
                            print "name",name.decode('unicode_escape')
                            print "contribution",contribution
                            print "userinforank", userinforank.decode('unicode_escape')
                            print "review",review.decode('unicode_escape')
                            print "time",timet
                            print "shop",shop.decode('unicode_escape')
                            print "cost",cost.decode('unicode_escape')
                            print "rst",rst1,rst2,rst3
                            # print rst2
                            # print rst3
                        '''
                        db=MySQLdb.connect(user='root',db='dianping',host='localhost' ,charset = 'utf8')
                        cursor=db.cursor()
                        sql = 'INSERT INTO `dianpingcontent`(`nameid`,`name`,`contribution`,`userinforank`,`review`,`time`,`shop`,`cost`,`rst1`,`rst2`,`rst3`)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                        val = (nameid,name,contribution,userinforank,review,time,shop,cost,rst1,rst2,rst3)
                        try:
                            cursor.execute(sql%val)
                            db.commit()
                        except:
                            db.rollback()
                        db.close()
                        '''
                    except Exception, e:
                        print Exception, ":", e
                        input("Error. Please check and then click Enter")
                time.sleep(20)
            time.sleep(10)
        time.sleep(20)
    time.sleep(40)
print "Finish"
