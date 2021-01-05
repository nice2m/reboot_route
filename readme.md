# 问题：
自用路由器开机太久，传输卡顿，内外网延迟高；


# 解决：
在windows下，使用PyInstaller 生成重启路由可执行程序，借助windows计划任务，每周自动重启一次路由器；


[windows计划任务参考](https://jingyan.baidu.com/article/154b463130041128ca8f41c7.html)


### libs & tools
[ requests 网络请求](https://github.com/psf/requests)
、
[ re 正则表达式操作](https://docs.python.org/zh-cn/3/library/re.html#module-re)、
[configparser ini 配置文件读取](https://docs.python.org/zh-cn/3/library/configparser.html#module-configparser)、
[PyInstaller python打包分发工具](https://github.com/pyinstaller/pyinstaller)


ps：万能的百度
