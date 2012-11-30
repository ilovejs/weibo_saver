#coding=utf8
import os
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import time
from BeautifulSoup import BeautifulSoup

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

def get_servertime():
    servertime_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
    data = urllib2.urlopen(servertime_url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print 'Get severtime error!'
        return None

def get_pwd(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

def login(username,pwd,cookie_file):
    if os.path.exists(cookie_file):
        try:
            cookie_jar  = cookielib.LWPCookieJar(cookie_file)
            cookie_load = cookie_jar.load(ignore_discard=True, ignore_expires=True)
            loaded = 1
        except cookielib.LoadError:
            loaded = 0
            print 'error loading cookies'

        if loaded:
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener         = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            return 1
        else:
            return do_login(username,pwd,cookie_file)
    else:
        return do_login(username,pwd,cookie_file)

def do_login(username,pwd,cookie_file):
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'wsse',
        'sp': '',
        'encoding': 'UTF-8',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    cookie_jar2     = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2         = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
    try:
        servertime, nonce = get_servertime()
    except:
        return
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username)
    login_data['sp'] = get_pwd(pwd, servertime, nonce)
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req_login  = urllib2.Request(
        url = login_url,
        data = login_data,
        headers = http_headers
    )
    result = urllib2.urlopen(req_login)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        login_url = p.search(text).group(1)
        urllib2.urlopen(login_url)
        print "Login success!"
        cookie_jar2.save(cookie_file,ignore_discard=True, ignore_expires=True)
        return 1
    except:
        print 'Login error!'
        return 0

def saver(uid):
    page = 1
    finished = False
    while not finished:
        urls={}
        urls[0]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=50&page=%d&uid=%d' % (page,uid)
        urls[1]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=0' % (page,uid,page)
        urls[2]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=1' % (page,uid,page)
        page = page + 1
        for p in urls:
            d = urllib2.urlopen(urls[p]).read()
            n = json.loads(d)
            soup = BeautifulSoup(n['data'])
            #print soup.prettify()
            #murl = (base62_encode(int(mid[::-1][14:21][::-1]))+base62_encode(int(mid[::-1][7:14][::-1]))+base62_encode(int(mid[::-1][0:7][::-1])))
            #mid = (str(base62_decode(str(murl[::-1][8:12][::-1])))+str(base62_decode(str(murl[::-1][4:8][::-1])))+str(base62_decode(str(murl[::-1][0:4][::-1]))))
            posts = soup.findAll(attrs={'action-type' : "feed_list_item"})
            if len(posts)>0:
                for post in posts:
                    mid  = post.get('mid')
                    if mid:
                        wb_from = post.find("a",{'class' : "S_link2 WB_time"})
                        murl    = re.sub("/.*/","",str(wb_from.get('href')))
                        ptime   = str(wb_from.get('title'))
                        content = re.sub("<[^>]*>", "", str(post.find(attrs={'node-type' : "feed_list_content"})))
                        print "%s\t%s\t%s" % (str(murl),str(ptime),str(content))
            else:
                finished = True

            time.sleep(0.5)

def main():
    username     = "18717746277"
    pwd          = "2&huffman"
    cookie_file  = "cookie_file.dat"

    login_status = login(username,pwd,cookie_file)

    # @聂风_ 1259955755
    uid = 1259955755
    if login_status:
        saver(uid)


if __name__  ==  '__main__':
    main()
