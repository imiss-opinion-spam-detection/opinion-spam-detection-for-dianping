# #-*- coding: UTF-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# import requests
# import json
# import re
# import urllib2
# import urllib
# from bs4 import BeautifulSoup
# import cookielib
# # import MySQLdb
# import time
# import random
#
# global ProxyIPList
#
#
#
# def getresultstr(result,number):#convert list to unicode string
#     resultstr=u""
#     for i in range(number,len(result)-number):
#         resultstr+=result[i]
#     return resultstr
#
# def getnameid(html):
#     getnameid=re.compile(r'(?<=user-id\=\")\d+')
#     result=getnameid.findall(html)
#     resultstr=getresultstr(str(result),1)
#     return resultstr
#
# def getname(html):
#     getname=re.compile(r'<p class="name"><a target="_blank" title="" href="/member/\d+">[\s\S]*?</a></p>')
#     resultware=getname.findall(html)
#     result=re.sub(r'<p class="name"><a target="_blank" title="" href="/member/\d+">|</a></p>',"",str(resultware))
#     resultstr=getresultstr(result,1)
#     return resultstr
#
#
# def getcontribution(html):
#     soup = BeautifulSoup(html)
#     resultware=soup.find_all('span',class_="user-rank-rst")
#     getnumber=re.compile(r'\d+\-\d+')
#     result=getnumber.findall(str(resultware))
#     resultstr=getresultstr(str(result),2)
#     return resultstr
#
#
# def getreview(html):
#     getreviewcontent=re.compile(r'<div class="J_brief-cont">[\s\S]*?</div>')
#     middleware=getreviewcontent.findall(html)
#     resultware=re.sub(r'<div class="J_brief-cont">|</div>',"",str(middleware))
#     result=re.sub(r'\s+|\\n',"",str(resultware))
#     resultstr=getresultstr(result,1)
#     return resultstr
#
#
# def getuserinforank(html):
#     getuserinforanknumber=re.compile(r'(?<=class="item-rank-rst irr-star)\d+')
#     result=getuserinforanknumber.findall(html)
#     resultstr=getresultstr(str(result),1)
#     return resultstr
#
#
#
# def gettime(html):
#     gettime=re.compile(r'(?<=<span class="time">)[\d\-]+?(?=</span>)')
#     result=gettime.findall(html)
#     result=str(result)
#     resultstr=getresultstr(result,2)
#     return resultstr
#
#
#
# def getcost(html):
#     getcost = re.compile(r'(?<=<span class="comm-pre">)[\s\S]*?(?=</span>)')
#     result = getcost.findall(html)
#     resultstr = getresultstr(str(result), 1)
#     return resultstr
#
#
# def getshop(html):
#     getshop=re.compile(r'(?<=<h2 class="misc-name">)[\s\S]*?(?=</h2>)')
#     result=getshop.findall(html)
#     resultstr=getresultstr(str(result),1)
#     return resultstr
#
#
# def getrst1(html):#the first classic review
#     try:
#         getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
#         middleware=getshop.findall(html)
#     #middleware=soup.find_all('span',class_="rst")
#         result=middleware[0]
#         return result
#     except Exception,e:
#         print Exception,":",e
#         return None
#
#
# def getrst2(html):#the second classic review
#     try:
#         getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
#         middleware=getshop.findall(html)
#         #middleware=soup.find_all('span',class_="rst")
#         result=middleware[1]
#         return result
#     except Exception,e:
#         print Exception,":",e
#         return None
#
# def getrst3(html):#the third classic review
#     try:
#         getshop=re.compile(r'(?<=<span class="rst">)[\s\S]*?(?=<em class="col-exp">)')
#         middleware=getshop.findall(html)
#         #middleware=soup.find_all('span',class_="rst")
#         result=middleware[2]
#         return result
#     except Exception,e:
#         print Exception,":",e
#         return None
#
#
# USER_AGENTS = [
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; media Center PC 5.0; .NET CLR 3.0.04506)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; media Center PC 6.0)",
#     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; media Center PC 6.0; .NET4.0C; .NET4.0E)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; media Center PC 6.0; .NET4.0C; .NET4.0E)",
#     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#     "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
#     "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
# ]
#
#
# def getProxyIP():
#     IPHtml = urllib2.urlopen("http://127.0.0.1:8000/?types=1")
#     IPPool = IPHtml.read().decode('utf-8')
#     patten = re.compile('"(.*?", \d+)]')
#     IPList = patten.findall(IPPool)
#     for index, item in enumerate(IPList):
#         IPList[index] = item.replace("\", ", ":")
#     return IPList
#
#
# ProxyIPList = getProxyIP()
# CurrentIP = random.choice(ProxyIPList)
# UsingTimes = 0
# ErrorTimes = 0
#
# def gethtml (url):
#     global ProxyIPList
#     global UsingTimes
#     global CurrentIP
#     global ErrorTimes
#
#     if UsingTimes >100:
#         UsingTimes  = 0
#         CurrentIP = random.choice(ProxyIPList)
#     UsingTimes +=1
#
#     #if len(ProxyIPList) == 0 :
#     #    time.sleep(1)
#      #   ProxyIPList = getProxyIP()
#     try:
#         cookieJar = cookielib.MozillaCookieJar()#setcookie
#         proxy = {'http':CurrentIP }
#         proxy_support = urllib2.ProxyHandler(proxy)
#         opener = urllib2.build_opener(proxy_support,urllib2.HTTPCookieProcessor(cookieJar))
#         headers={#set headers
#             'User-Agent':random.choice(USER_AGENTS),
#             'Accept'    :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Cache-Control':'max-age=0',
#             'Accept-Language':'zh-CN,zh;q=0.8',
#             'Connection':'keep-alive',
#             'Host':'www.dianping.com',
#              'Upgrade-Insecure-Requests':'1',
#             'Cookie':'showNav=javascript:; navCtgScroll=0; _hc.v=69ec1d48-6214-a4a6-3e4f-8d3eb5c8f2cb.1467510663; __utma=1.1749497646.1467510663.1467510663.1467510663.1; __utmz=1.1467510663.1.1.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%A4%A7%E4%BC%97%E7%82%B9%E8%AF%84%E7%BD%91; PHOENIX_ID=0a0302bc-155d90b6be9-c8936; s_ViewType=10; JSESSIONID=7299F758AA33C769D888B5CF53E1A88C; aburl=1; cy=17; cye=xian'
#          }
#         data=None
#         request=urllib2.Request(url,data,headers)#setrequest
#         result = opener.open(request)
#         html = result.read().decode('utf-8')
#         return html
#     except Exception,e:
#         print Exception,e
#         ProxyIPList = getProxyIP()
#         if ErrorTimes > 10:
#             ErrorTimes = 0
#             ProxyIPList = getProxyIP()
#             CurrentIP = random.choice(ProxyIPList)
#         ErrorTimes +=1
#         time.sleep(20)
#         return gethtml(url)
#
#
# def getcitylist(html):
#     time.sleep(1)
#     getcitywareurl=re.compile(r'<a href="/[\s\S]*?</a>')
#     cityurlware=getcitywareurl.findall(html)
#     getcityurl=re.compile(r'href="/[\s\S]*?"')
#     cityurl=getcityurl.findall(str(cityurlware))
#     result=re.sub(r'href=|"|\s|\'',"",str(cityurl))
#     result=result.split(',')
#     number=len(result)
#     cityurllist=[]
#     for i in range(3,number-1):
#         urlcity="https://www.dianping.com"+str(result[i])
#         cityurllist.append(urlcity)
#     return cityurllist
#
# def getcategoryurllist(cityurl):
#     time.sleep(0.5)
#     cityhtml=gethtml(cityurl)
#     getcategorylist=re.compile(r'<a data-key="\d+" href="[\s\S]*?">[\s\S]*?</a>')
#     middleware=getcategorylist.findall(cityhtml)
#     getcategoryhref=re.compile(r'href="[\s\S]*?"')
#     resultware=getcategoryhref.findall(str(middleware))
#     result=re.sub(r'href=|"|\'|\s|\[|\]',"",str(resultware))
#     result=result.split(",")
#     number=len(result)
#     categoryurllist=[]
#     for i in range(0,number):
#         categoryurl="https://www.dianping.com"+str(result[i])
#         categoryurllist.append(categoryurl)
#     print categoryurllist
#     return categoryurllist
#
# def getareaurllist(categoryurl):
#     time.sleep(0.5)
#     categoryhtml=gethtml(categoryurl)
#     getareaurlware=re.compile(r'href="/search/category/\d+/\d+/g\d+r\d+')
#     resultware=getareaurlware.findall(categoryhtml)
#
#     result=re.sub(r'href=|\"|\'|\[|\]|\s|u|#nav-tab\|0\|1',"",str(resultware))
#     result=result.split(",")
#     number=len(result)
#     areaurllist=[]
#     for i in range(0,number):
#         areaurl="https://www.dianping.com"+str(result[i])
#         areaurllist.append(areaurl)
#     return areaurllist
#
# def getshopurllist(shopeachlisturl):
#     shopurlhtml=gethtml(shopeachlisturl)
#     getshopurl=re.compile(r'<a target="_blank" href="/shop/\d+"')
#     resultware=getshopurl.findall(shopurlhtml)
#     result=re.sub(r'<a target="_blank" href=|\"|\'|\[|\]|\s|u',"",str(resultware))
#     result=result.split(",")
#     number=len(result)
#     shopurllist=[]
#     for i in range(0,number):
#         shopurl="https://www.dianping.com"+str(result[i])
#         shopurllist.append(shopurl)
#     return shopurllist
#
# def getpagenumber(url):
#      html=gethtml(url)
#      getpagenumber=re.compile(r'title\="\d+">\d+</a>')
#      pagenumberware=getpagenumber.findall(html)
#      if pagenumberware==[]:
#           return 1
#      getpageinnernumber=re.compile(r'\d+')
#      pagenumber=getpageinnernumber.findall(str(pagenumberware[-1]))
#      pagenumber=int(pagenumber[1])
#      return pagenumber
#
#
# '''
# rooturl="https://www.dianping.com/citylist/citylist?citypage=1"
# roothtml=gethtml(rooturl)
# cityurllist=getcitylist(roothtml)
# for cityurl in cityurllist:
# '''
# cityurl = "https://www.dianping.com/shanghai"
# categoryurllist=getcategoryurllist(cityurl)
# for categoryurl in categoryurllist:
#     areaurllist=getareaurllist(categoryurl)
#     for areaurl in areaurllist:
#         shoplistpagenumber=getpagenumber(areaurl)#togetpagenumber
#         for y in range(1,shoplistpagenumber+1):
#             shopeachlisturl=areaurl+"p"+str(y)
#             shopurllist=getshopurllist(shopeachlisturl)
#             for shopurl in shopurllist:
#                 url=shopurl+"/review_all?pageno=1"#togetpagenumber
#                 print url
#                 pagenumber=getpagenumber(url)
#                 print url
#                 for x in range(1,pagenumber+1):
#                     url=shopurl+"/review_all?pageno="+str(x)
#                     try:
#                         html=gethtml(url)
#                     except Exception,e:
#                         print Exception,":",e
#                     getcontent=re.compile(r'<li id="rev_\d+" data-id="\d+">[\s\S]*?<div class="mode-tc respond Hide">')
#                     result=getcontent.findall(html)
#                     contentnumber=len(result)
#                     for i in  range(0,contentnumber):
#                         nameid=getnameid(result[i])
#                         name=getname(result[i])
#                         contribution=getcontribution(result[i])
#                         userinforank=getuserinforank(result[i])
#                         review=getreview(result[i])
#                         timet= gettime(result[i])
#                         shop=getshop(result[i])
#                         cost=""#getcost(result[i])
#                         rst1=getrst1(result[i])
#                         rst2=getrst2(result[i])
#                         rst3=getrst3(result[i])
#                         try:
#
#                             #print nameid
#                             #print name.decode('unicode_escape')
#                             #print contribution
#                             #print userinforank.decode('unicode_escape')
#                             #print review.decode('unicode_escape')
#                             print timet
#                             print shop.decode('unicode_escape')
#                             # print cost.decode('unicode_escape')
#                             # print rst1
#                             #print rst2
#                             #print rst3
#                         except:
#                             pass
#
#                         db = MySQLdb.connect(user='root', passwd='root', db='dianping', host='localhost',charset='utf8')
#                         cursor=db.cursor()
#                         sql = 'INSERT INTO `dianpingcontent`(`nameid`,`name`,`contribution`,`userinforank`,`review`,`time`,`shop`,`cost`,`rst1`,`rst2`,`rst3`)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
#                         val = (
#                                 nameid[2:-1],
#                                 name.decode('unicode_escape')[2:-1],
#                                 contribution,
#                                 userinforank.decode('unicode_escape')[2:-1],
#                                 review.decode('unicode_escape')[2:-1],
#                                 timet[1:],
#                                 shop.decode('unicode_escape')[2:-1],
#                                 cost,
#                                 rst1,
#                                 rst2,
#                                 rst3
#                                )
#                         try:
#                             cursor.execute(sql%val)
#                             db.commit()
#                         except:
#                             db.rollback()
#                         db.close()
#
#                 time.sleep(20)
#             time.sleep(3)
#         time.sleep(6)
#     time.sleep(12)
# time.sleep(15)