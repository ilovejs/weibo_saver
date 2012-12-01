**Note:**

第一次使用的时候需要提供用户名和密码，只有登录了才能获取微博内容。第一次使用以后，只要cookie有效，就可以使用cookie直接登录。

本程序不能处理验证码，所以如果你正常登录的时候需要输入验证码，那么程序就不能使用这个帐号了。

原则上可以抓取任何人的所有微博,只要提供你想抓取的用户的uid。(不知道什么是 weibo uid？Google it！)

程序有判断时间线和上次抓取的结果，只会抓取上次抓取后的新增部分，不会每次扫描所有微博。

结果按照时间顺序排序，因此忽略置顶。

欢迎关注 [@聂风_](http://weibo.com/napoleonu) [http://weibo.com/napoleonu](http://weibo.com/napoleonu)

**Usage:**

    ~/weibo_saver (master) $ python save_post.py --help
    Usage: save_post.py [options] arg 
     e.g.: save_post.py -i 1259955755 # when cookie file is usable 
     e.g.: save_post.py -u username -p password -i 1259955755
    
    Options:
      -h, --help            show this help message and exit
      -u USERNAME, --username=USERNAME
                            if cookie file is unusable you must provide username and password.
      -p PASSWORD, --password=PASSWORD
                            if cookie file is unusable you must provide username and password.
      -i UID, --uid=UID     the id of the user you want save.

**Result:**

    ~/weibo_saver (master) $ more weibo_post.txt 
    xpYZltWsR       2011-09-26 17:26        嗷 
    y7cgV3Svj       2012-02-26 03:03        Peter Zaitsev在Linkedin上加我，虽然我是菜鸟。。 
    ytvxeFT5m       2012-07-21 20:33        分享图片 #WeicoLomo# 
    z3d9i1bYI       2012-11-01 20:41        我做了一个通过比对两个mysqldump文件的差异生成表变更语句的小工具，欢迎试用 http://t.cn/zlddhOW 。merge_schema : Compare and merge MySQL schemas. 
    z3KnKiJoW       2012-11-05 09:17        转发微博 [@韩志国 : 【 三权分立是最不坏制度 】 权力应该用来制衡权力：没有一种无娄罗的权力，也没有一种无臣仆的尊荣。无限权力会奴化一切，也会毁掉他的占有者。权力制衡已成中国第一难题，中国社会出现的混论无序，根源于没有制衡的权力。权力机关没有制衡，社会不能约束权力；司法成为权力奴仆，社会就很难有公义。]
    z5cdGfZ4B       2012-11-14 21:59        //@grassbell: 推荐一种Oracle的备份方式。如果你有NAS设备，在上面直接搭建一个standby，一天恢复一次，open readonly 后利用NAS的snapshot做一次快照。根据NAS空间，保留比如30天的快照。这样我们可以通过snapshot打开任意30天以内的standby，一方面可以验证备份，一方面可以追溯历史数据。 [@沃趣科技 :【远离故障的十大原则之4】备份并验证备份有效性。是人总会出错，是机器总可能会有突然崩溃的那一天。怎么办－我们需要准备备份。备份的学问很大。按照不同的纬度可以分为：冷备份和热备份；实时备份和非实时备份；物理备份和逻辑备份。]
    z5ctealKc       2012-11-14 22:37        大四上学期无聊做的那些Chrome插件，今天过去瞄了眼，没想到有些还有4，5千人在用，额。 http://t.cn/zjZXxaj 虽然快3年没更新了[江南style] 
    z5fVfeuGD       2012-11-15 07:25        秀的别人好羡慕 [@二宝真好记 : 如果不秀点双11流量带来的“成绩”， 不表一下辛苦，不搞个庆祝，那就在这家公司白混了。谁来关注这些浮华数字背后的问题？为何我们依然缺乏安全感？秀场文化真的要一颗永流传吗？]
    z5fXvhirk       2012-11-15 07:30        这个ms-sql是微软那个吗[思考] //@水永成_王涛: 赞！这次双11，mysql,ms—sql,oceanbase,hbase,oracle都顶住了！ [@_后羿 : 祝贺我们DBA组成功hold住双11，成功驾驭了史上最高强度的数据库技术保障！MySQL、Oceanbase、RDS、Hbase 都平稳渡过了史上最高流量！ 双11有我们更精彩！ @hellodba @tb天羽 @AlibabaDBA]
    z5g0ZAMGq       2012-11-15 07:39        siri真好[心] 
