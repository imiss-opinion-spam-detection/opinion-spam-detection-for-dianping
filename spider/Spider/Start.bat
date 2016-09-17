@echo off
echo "Start IPProxy"
start "IPProxy" "python2" "E:\SpamDetection\IPProxys-master\IPProxys.py"
pause
echo "Start CookiePool"
call "python2" "E:\SpamDetection\Spiders\Spider\CookiePool.py"
echo "Start Spider"
start "Spider" "python2" "E:\SpamDetection\Spiders\Spider\productspiderBeta.py"
pause
echo "Open Mysql"
mysql -u root -p
pause
