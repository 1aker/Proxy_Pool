# Proxies项目的初衷 
由于在渗透等实际应用过程中常常需要ip进行代理，而网上提供的免费代理又质量不好，因此自建服务器代理自用网页用处颇益。

# 设计思路
在多处收集ip代理并自建Flask服务器进程进行ip测试，避免在其他网站查自己ip太过频繁导致自己被ban，采用异步Gevent,threading提高效率

# 性能要求
建议在linux服务器搭建，配置在1G内存一核或以上

# 使用方法
python3 proxies.py

# 更好的方法
你也可以在后台持久挖掘代理  
> sudo screen -S proxies  

> python3 proxies.py  

> ctrl + a + d  

# 同时你如果不具备apache服务，请安装
### 以Ubuntu为例
> sudo apt-get install apache2
> sudo /etc/init.d/apache2 restart
具体参照 https://www.linuxidc.com/Linux/2013-06/85827.htm
