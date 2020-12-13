import requests
import re

# 用途：一键重启路由器
# 适用于 天翼网关产品型号 ZXHN F450 21ZTT40001
# 偶发路由长时间开机，内网延迟高问题

# 模拟接口的形式，无破解或漏洞
# 使用chrome 浏览器开发者工具，得到了接口访问顺序，和cookies 存取
# !!! 比较有意思的是进路由域名首次请求页面，有一个hidden属性的form 表单提交初始token 的操作，sao操作

# python 实现步骤：
# 步骤1 首先GET请求路由地址，获取到初始token
# 步骤2 携带初始token ,路由密码，用户名，POST请求 /cgi-bin/luci登录
# 步骤3 截取用户token ,请求路由重启接口 /cgi-bin/luci/admin/reboot

# 常量定义

class RouteRbootor:
    """
    重启路由器模块
    """

    #路由器地址，路由器用户名，密码
    route_host = 'http://192.168.1.1'
    route_username = 'useradmin'
    route_pwd = '******'
    
    login_path_step1 = '/cgi-bin/luci'
    reboot_path = '/cgi-bin/luci/admin/reboot'

    http_session = requests.Session()
    http_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def start(self):
        self.get_init_token()

        login_response = self.login(self.route_username,self.route_pwd)
        gapMeterialStrting = login_response.text
        assert(login_response.status_code == 200)

        token = self.search_token(gapMeterialStrting)
        print('token')
        print(token)

        reboot_response = self.reboot(token)
        assert(reboot_response.status_code == 200)
        pass

    
    def get_init_token(self):
        """
        # 步骤1 首先GET请求路由地址，获取到初始token;
        """
        url = self.route_host
        rt = self.http_request(url,True,None)
        self.showCookies(rt)
        print('get_init_token:')
        print(rt.cookies)
        pass

    def login(self,username,pwd):
        """
        步骤2 携带初始token 登录路由器
        """
        url = self.route_host + self.login_path_step1
        rt = self.http_request(url,False,{'username':username,'psd':pwd})
        self.showCookies(rt)

        return rt
    
    def reboot(self, token):
        """
        步骤3 截取用户token ,请求路由重启接口 /cgi-bin/luci/admin/reboot
        """
        url = self.route_host + self.reboot_path
        r = self.http_request(url,False,{'token':token})

        return r

    def search_token(self,content):
        pattern_tokenMatch = re.compile(r'{ token: .* }')
        result = pattern_tokenMatch.search(content)
        #通过接口页面 搜索到的内容形如 { token:'01234567890123456789012345678912' }

        tokenStartIndex = 10
        tokenLength = 32
        resultDes = result.group()[tokenStartIndex: (tokenStartIndex + tokenLength)]
        return resultDes

    # util
    def http_request(self, url,isGET,param):
        """
        发起http POST & GET请求
        """
        if isGET:
            self.http_session.headers = self.http_headers
            r = self.http_session.get(url)
            r.encoding = 'utf8'

            #print(r.cookies['token'])
            showRt = '''
            path:{0}
            content:{1}
            '''.format(url, r.text)
            return r

        self.http_session.headers = self.http_headers
        r = self.http_session.post(url,data=param)
        r.encoding = 'utf8'
        # print('sysauth')
        # print(r.cookies['sysauth'])
        showRt = '''
        path:{0}
        content:{1}
        '''.format(url,r.text)
        print(showRt)
        return r
    # debug helpers
    
    def showCookies(self,response):
        """
        展示当前URL cookie
        """
        print('cj:')
        print(response.cookies)
        # for item in cj.keys:
        #     print('cj:')
        #     print(cj)
        #     print(item)
        return response.cookies


def main():
    rebootor = RouteRbootor()
    rebootor.start()

if __name__ == '__main__':
    main()



