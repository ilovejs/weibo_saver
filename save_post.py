#!/usr/bin/env python
#coding=utf8

try:
    import os
    import sys
    import urllib
    import urllib2
    import cookielib
    import base64
    import re
    import hashlib
    import json
    import time
    from BeautifulSoup import BeautifulSoup
    from optparse import OptionParser
except ImportError:
        print >> sys.stderr, """\

There was a problem importing one of the Python modules required to run yum.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_value, sys.version)
        sys.exit(1)

__prog__= "weibo_saver"
__site__= "http://chaous.com"
__weibo__= "@聂风_"
__version__="0.1-beta"

def config_option():
    usage =  "usage: %prog [options] arg \n"
    usage += " e.g.: %prog -i 1259955755 # when cookie file is usable \n"
    usage += " e.g.: %prog -u username -p password -i 1259955755"
    parser = OptionParser(usage)
    parser.add_option("-u","--username",dest="username",help="if cookie file is unusable you must provide username and password.")
    parser.add_option("-p","--password",dest="password",help="if cookie file is unusable you must provide username and password.")
    parser.add_option("-i","--uid",dest="uid",help="the id of the user you want save.")

    (options, args) = parser.parse_args()

    if not options.username or not options.password:
        options.username = "wrong_user"
        options.password = "wrong_pass"

    if not options.uid:
        parser.error("You must input -i parameters");

    global opt_main
    opt_main = {}
    opt_main["username"] = options.username
    opt_main["password"] = options.password
    opt_main["uid"] = options.uid

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

def mid_to_murl(mid):
    murl = (base62_encode(int(mid[::-1][14:21][::-1]))+base62_encode(int(mid[::-1][7:14][::-1]))+base62_encode(int(mid[::-1][0:7][::-1])))
    return murl

def murl_to_mid(murl):
    mid = (str(base62_decode(str(murl[::-1][8:12][::-1])))+str(base62_decode(str(murl[::-1][4:8][::-1])))+str(base62_decode(str(murl[::-1][0:4][::-1]))))
    return mid

def get_servertime():
    servertime_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&client=ssologin.js(v1.3.18)'
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
            print 'Loading cookies error'

        if loaded:
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener         = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print 'Loading cookies success'
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

def last_murl(output_file):
    with open(output_file, 'r') as f:
        f.seek (0, 2) # Seek @ EOF
        fsize = f.tell() # Get Size
        f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
        lines = f.readlines() # Read to end
    line = lines[-1:] # Get last line
    murl = '0'
    if len(line) > 0:
        murl = re.sub("\t.*", "", line[0])
        murl = re.sub("\n", "", murl)

    return murl

def clean_content(content):
    content = re.sub("<img src=[^>]* alt=\"", "", content)
    content = re.sub("\" type=\"face\" />", "", content)
    content = re.sub("<[^>]*>", "", content)
    content = re.sub("&quot;", "\"", content)
    content = re.sub("&apos;", "\'", content)
    content = re.sub("&amp;", "&", content)
    content = re.sub("&lt;", "<", content)
    content = re.sub("&gt;", ">", content)

    return content

def saver(uid,output_file):
    if os.path.exists(output_file):
        last_mid = int(murl_to_mid(last_murl(output_file)))
    else:
        last_mid = 0
    page     = 1
    uid      = int(uid)
    weibo    = {}
    finished = False
    saved_count = 0 # for top
    while not finished:
        urls={}
        urls[0]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=50&page=%d&uid=%d' % (page,uid)
        urls[1]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=0' % (page,uid,page)
        urls[2]='http://weibo.com/aj/mblog/mbloglist?_wv=5&count=15&page=%d&uid=%d&pre_page=%d&pagebar=1' % (page,uid,page)
        print "now page : %d" % page
        page = page + 1
        for p in urls:
            try:
                d = urllib2.urlopen(urls[p]).read()
                n = json.loads(d)
            except:
                print "Get data error,remove your cookie data and try again"
                finished = True
                break
            soup = BeautifulSoup(n['data'])
            #print soup.prettify()
            posts = soup.findAll(attrs={'action-type' : "feed_list_item"})
            if len(posts)>0:
                for post in posts:
                    mid  = int(post.get('mid'))
                    if mid:
                        forward = post.get('isforward')
                        if forward:
                            origin_nick     = clean_content(str(post.find(attrs={'node-type' : "feed_list_originNick"})))
                            forward_content = "[%s : %s]" % (origin_nick,clean_content(str(post.find(attrs={'node-type' : "feed_list_reason"}))))
                        else:
                            forward_content = ""
                        wb_from = post.find("a",{'class' : "S_link2 WB_time"})
                        murl    = str(re.sub("/.*/","",str(wb_from.get('href'))))
                        ptime   = str(wb_from.get('title'))
                        content = clean_content(str(post.find(attrs={'node-type' : "feed_list_content"})))

                        if mid > last_mid:
                            weibo[mid] = "%s\t%s\t%s %s\n" % (murl,ptime,content,forward_content)
                        elif saved_count > 2:
                            finished = True
                        else:
                            saved_count = saved_count + 1

            else:
                finished = True

            time.sleep(0.5)

        #finished = True

    f = open(output_file,'a+')
    for i in sorted(weibo.items(), key=lambda e:e[0], reverse=False):
        f.write(i[1])

    f.close()


def main():
    config_option()
    username     = opt_main["username"]
    pwd          = opt_main["password"]
    uid          = opt_main["uid"]
    cookie_file  = "cookie_file.dat"
    output_file  = "weibo_post_%s.txt" % (uid)

    login_status = login(username,pwd,cookie_file)

    # @聂风_ 1259955755
    if login_status:
        saver(uid,output_file)


if __name__  ==  '__main__':
    main()
