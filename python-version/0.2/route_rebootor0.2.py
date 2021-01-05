import os
import re
import requests
import configparser

# 用途：一键重启路由器
# 适用于 天翼网关产品型号 ZXHN F450 21ZTT40001
# 偶发路由长时间开机，内网延迟高问题

#步骤一、   分析
# 模拟接口的形式，无破解或漏洞
# 使用chrome 浏览器开发者工具，得到了接口访问顺序，和cookies 存取
# !!! 比较有意思的是进路由域名首次请求页面，有一个hidden属性的form 表单提交初始token 的操作，sao操作

#步骤二、   coding
# python 实现步骤：
# 步骤1 首先GET请求路由地址，获取到初始token
# 步骤2 携带初始token ,路由密码，用户名，POST请求 /cgi-bin/luci登录
# 步骤3 截取用户token ,请求路由重启接口 /cgi-bin/luci/admin/reboot

# 步骤三、  exe 程序生成
# pyinstaller --onefile --nowindowed --icon="C:\Users\Administrator\Desktop\side_project\路由重启\resource\20201217080538460_easyicon_net_128.ico" C:\Users\Administrator\Desktop\side_project\路由重启\python-version\0_2\route_rebootor0.2.py
# ref:https://www.cnblogs.com/robinunix/p/8426832.html

class RouteRbootor:
    """
    重启路由器模块
    """

    ini_read_info = []
    #路由器地址，路由器用户名，密码
    route_host = ''
    route_username = ''
    route_pwd = ''
    
    login_path_step1 = '/cgi-bin/luci'
    reboot_path = '/cgi-bin/luci/admin/reboot'
    debug_show = 0

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
        #0.读取配置文件，变量赋值
        self.ini_config()
        #1.
        self.get_init_token()

        #格式化展示
        print('======================================================')
        print('======================================================')

        print('Start reboot route...')
        #2.
        login_response = self.login(self.route_username,self.route_pwd)

        gapMeterialStrting = login_response.text
        token = self.search_token(gapMeterialStrting)

        #3.
        reboot_response = self.reboot(token)

        state = "succeed" if ((reboot_response.status_code == 200) and (login_response.status_code == 200)) else "failed"
        if self.debug_show == 1:
            print(login_response.url)
            print(login_response.status_code)

            print(reboot_response.url)
            print(reboot_response.status_code)
        
        print(state)
        print('reboot end')
        print('======================================================')
        print('======================================================')
        pass

    def get_init_token(self):
        """
        # 步骤1 首先GET请求路由地址，获取到初始token;
        """
        url = self.route_host
        rt = self.http_request(url,True,None)
        self.debug_show_cookies(rt)
        pass

    def login(self,username,pwd):
        """
        步骤2 携带初始token 登录路由器
        """
        url = self.route_host + self.login_path_step1
        rt = self.http_request(url,False,{'username':username,'psd':pwd})
        self.debug_show_cookies(rt)

        return rt
    
    def reboot(self, token):
        """
        步骤3 截取用户token ,请求路由重启接口 /cgi-bin/luci/admin/reboot
        """
        url = self.route_host + self.reboot_path
        r = self.http_request(url,False,{'token':token})

        return r

    # util
    def ini_config(self):
        """
        初始化配置
        """
        self.ini_read_info = self.read_ini_configs()
        self.route_host = self.ini_read_info[0]
        self.route_username = self.ini_read_info[1]
        self.route_pwd = self.ini_read_info[2]

        self.debug_show =  self.ini_read_info[3]
        pass

    def read_ini_configs(self):
        #"""读取路由配置，读取调试配置"""
        cf = configparser.ConfigParser()
        root_path = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(root_path, 'config.ini')
        cf.read(config_path, encoding='utf-8')

        route_host = cf.get("route_info", "route_host")
        route_username = cf.get("route_info", "route_username")
        route_pwd = cf.get("route_info", "route_pwd")

        debug_show = cf.get("debug_config", "debug_config_show")
        return [route_host, route_username, route_pwd, debug_show]

    def search_token(self,content):
        pattern_tokenMatch = re.compile(r'{ token: .* }')
        result = pattern_tokenMatch.search(content)
        #通过接口页面 搜索到的内容形如 { token:'01234567890123456789012345678912' }

        tokenStartIndex = 10
        tokenLength = 32
        resultDes = result.group()[tokenStartIndex: (tokenStartIndex + tokenLength)]
        return resultDes

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
            if self.debug_show == 1:
                print(showRt)
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
        if self.debug_show == 1:
            print(showRt)
        return r

    # debug helpers
    def debug_show_cookies(self,response):
        """
        展示当前URL cookie
        """
        print('cookies:')
        print(response.cookies)
        pass


def main():
    rebootor = RouteRbootor()
    rebootor.start()

if __name__ == '__main__':
    main()


