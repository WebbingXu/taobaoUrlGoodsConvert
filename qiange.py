import urllib
import urllib.request
import re
import http.cookiejar
import urllib.parse


'''功能：我们知道在微信里面访问淘宝天猫宝贝或是店铺的链接会被为微信屏蔽，
而千鸽网站(http://www.qiange.so/Wechat_url.php)为我们提供了这样一个转换功能，
现在使用Python来实现。稍微修改程序便可实现批量的转换
代码写的有点粗糙，主要为了实现功能
'''

cj = http.cookiejar.LWPCookieJar()  
cookie_support = urllib.request.HTTPCookieProcessor(cj)  
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler) 
resp = opener.open('http://qiange.so/Wechat_url.php')

user_name = input('千鸽用户名:')
passwd = input('密码:')

login_post_para = {
	'mobile':user_name,
	'pwd':passwd,
	'type':'login'
}
login_post_data = urllib.parse.urlencode(login_post_para).encode(encoding='UTF8')
req = urllib.request.Request('http://qiange.so/ajax/users/to_Mobile_login.php', login_post_data)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; rv:46.0) Gecko/20100101 Firefox/46.0')
req.add_header('Host', 'www.qiange.so')
req.add_header('Referer', 'http://www.qiange.so/Wechat_url.php')
resp = opener.open(req)
resp_dict = eval(resp.read())
phone_num = resp_dict['mobile']
userid = resp_dict['userid']
service_name = resp_dict['service_name']
# print ('after login:\n')
# print (phone_num)
# print (userid)
# print (service_name)
# print ('************************************\n\n\n')

taobao_good_urls = input('请输入需要被转换的链接:')

post_data_judge = {
    'urls':taobao_good_urls,
    'names':''
}
data = urllib.parse.urlencode(post_data_judge).encode(encoding='UTF8')
req = urllib.request.Request('http://qiange.so/ajax/to_Judge_url.php', data)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
response = opener.open(req)
the_page = response.read()
the_page_dict = eval(the_page)
urls = the_page_dict["url"].replace('\\','');  #需要去掉斜杠\
name = the_page_dict["title"];
shop_type = the_page_dict["type"];
small_shop_type = the_page_dict["Small_shop_type"];
# print ('after call @to_Judge_url:\n')
# print ('urls = %s\n'%urls)
# print ('name = %s\n'%name)
# print ('shop_type = %s\n'%shop_type)
# print ('small_shop_type = %s\n'%small_shop_type)
# print ('************************************\n\n\n')



post_data_user_type = {
    'userid':'298841',
    'urls':urls
}
data = urllib.parse.urlencode(post_data_user_type).encode(encoding='UTF8')
req = urllib.request.Request('http://qiange.so/ajax/users/user_type.php', data)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
response = opener.open(req)
the_page_user_type = response.read()
# print ('after call @to_user_type:\n')
# print (the_page_user_type)     #正常应该是没有内容
# print ('************************************\n\n\n')


post_to_short_url = {
    'url':'http://djaa.cn/shopUrl.php?shopName=%s&'%name + 'shopUrl='+urllib.parse.quote_plus(urls)+'&userid='+userid,
    'a':'6',
    'b':'5'
}
data = urllib.parse.urlencode(post_to_short_url).encode(encoding='UTF-8')
req = urllib.request.Request('http://qiange.so/ajax/short_url/to_short_url.php', data)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
response = opener.open(req)
#print ('after call @to_short_url:\n')
the_page_short_url = response.read().decode('utf-8') #需要decode
#print (the_page_short_url)
#print ('************************************\n\n\n')

final = {'short_url':"http://yv2ryn.ren/%s"%str(the_page_short_url)}
data = urllib.parse.urlencode(final).encode(encoding='UTF8')
req = urllib.request.Request('http://qiange.so/ajax/short_url/to_weibo_url.php', data)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
response = opener.open(req)
the_page_short_url = response.read().decode('utf-8')
print ('\n\n\n转换后的链接' + the_page_short_url)
print ('现在将上面的链接复制到微信后就能直接访问而不会被屏蔽了')