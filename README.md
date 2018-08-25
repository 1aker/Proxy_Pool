# Proxies 
由于在渗透等实际应用过程中常常需要ip进行代理，而网上提供的免费代理又质量不好，因此自建服务器代理自用网页用处颇益。

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
