import urllib.parse
import urllib.request
import http.cookiejar
import re

# 适用于 天翼网关产品型号 ZXHN F450 21ZTT40001
# 偶发路由长时间开机，内网延迟高问题，一键重启路由


# 常量定义
# 路由器用户名
routeUserName = 'useradmin'
# 路由登录密码
routePwd = 'mwtxn'

#路由器ip
host = 'http://192.168.1.1'
loginPath_step1 = '/cgi-bin/luci'
rebootPath = '/cgi-bin/luci/admin/reboot'

#声明一个CookieJar保存调试cookie
cookie = http.cookiejar.CookieJar()
#利用urllib.request库的HTTPCookieProcessor对象
handler = urllib.request.HTTPCookieProcessor(cookie)
#通过CookieHandler创建opener
opener = urllib.request.build_opener(handler)


#step0_ 获取初始token
urlStr_step0 = host
response = opener.open(urlStr_step0)
print(response.read().decode('utf8'))


#step1_ 开始登录
dict_step1 ={}
dict_step1['psd'] = routePwd
dict_step1['username'] = routeUserName
dictData_step1 = bytes(urllib.parse.urlencode(dict_step1),encoding='utf8')
print(dict_step1)
urlStr_step1 = host + loginPath_step1
print(urlStr_step1)
response2 = opener.open(urlStr_step1,data=dictData_step1)
#解析token所在html
tokenOriginHtmlString = response2.read().decode('utf8')
print(tokenOriginHtmlString)
#匹配查找登录token
pattern_tokenMatch = re.compile(r'{ token: .* }')
result = pattern_tokenMatch.search(tokenOriginHtmlString)
tokenStartIndex = 10
tokenLength = 32
resultDes = result.group()[tokenStartIndex : (tokenStartIndex + tokenLength)]
print('result.goup() is:')
print(result.group())
print('resultDes')
print(resultDes)


#step2_开始重启路由
dict_step3 ={}
dict_step3['token'] = resultDes
dictData_step3 = bytes(urllib.parse.urlencode(dict_step3),encoding='utf8')

urlStr_step3 = host + rebootPath
response3 = opener.open(urlStr_step3,data=dictData_step3)
print(response3.read().decode('utf8'))


#调试打印cookie信息
print('print cookies:\n')
for item in cookie:
    print('Name = %s' % item.name)
    print('Value = %s' % item.value)


