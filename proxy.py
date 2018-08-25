# usr/bin/env python
# -*- coding :utf-8 -*-
# author:lakeR
# 我们将在这里使用大量socket,为了与sqlmap的socket中间件更加适应
import requests
import socket
import gevent
import time
import re
import os
import queue
import random
from gevent import monkey;
monkey.patch_socket()
queue = queue.Queue()  # 推到queue调度器

already = []
web_filename = '/www/wwwroot/1aker.cn/open/socket.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3315.4 Safari/537.36'}



rex_xici = re.compile(r'<td>(\d+\..*?)</td>.*?<td>(\d+)</td>', re.S)
rex_66ip = re.compile(r'<tr><td>((?:\d+\.){3}\d+)</td><td>(\d+)</td><td>')
rex_kuai = re.compile(r'<td data-title="IP">((?:\d+\.){3}\d+)</td>.*?<td data-title="PORT">(\d+)</td>', re.S)
rex_89ip = re.compile(r'((?:\d+\.){3}\d+).*?</td>.*?<td>.*?(\d+).*?</td>', re.S)
# 以上是代理ip爬取的正则表达式
rex_ip = re.compile(r'((?:\d+\.){3}\d+)')

def file_write(lis):
    erasure()
    result = []
    for i in lis:
        if i not in result:
            result.append(i)
    lis = result
    del result
    f = open(web_filename, 'a+', encoding='utf-8')
    for i in lis:
        print('[*]Socket writing:', i[0])
        f.write(str(i) + '<br>')
    f.close()

def erasure():
    if os.name != 'nt':
        f = open(web_filename, 'w')
        f.truncate()
        f.close()



def socket_test(temp):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.settimeout(7)  # 不排除竞争现象，但我们使用协程或许可行
    socket_symbol = False
    try:

        proxy_socket.connect((str(temp[0]), int(temp[1])))  # 获取连接可行性
        #print('socket可连接',temp)
        proxy_socket.send('GET / HTTP/1.1\r\nHost: 120.79.91.29:13888\r\n\r\n'.encode())
        data = proxy_socket.recv(2048).decode()
        proxy_socket.close()
        #print('得到数据',data.encode())
        #ip = rex_ip.findall(data)[0]
        if re.findall(r'Python/3\.5\.2', data) != []:# 防止匿名网络错杀
            already.append(temp)
            return True
        else:
            return False
        #  print('socket核验成功', ip)
    except Exception as e:
        #print(e)
        return False


def self_test():
    temp = queue.get()
    proxies_test = {"http": "http://%s:%s" % (temp[0], temp[1])}
    proxies = proxies_test
    socket_symbol = socket_test(temp)



def spawn(spawn_list):
    result = []
    for i in spawn_list:  # 对spawn_list去重，转移给
        if i not in result:
            result.append(i)
    spawn_list = result
    for i in spawn_list:
        queue.put(i)
    size = queue.qsize()
    gevent_list = []
    for i in range(size):
        try:
            g = gevent.spawn(self_test, )
            gevent_list.append(g)
        except KeyboardInterrupt:
            return True
    gevent.joinall(gevent_list)
    if os.name != 'nt':
        file_write(already)


def proxies_crawl():
    try:  # 这是我们第二次代理
        proxies = random.choice(already)
        proxies = {'http': 'http://%s:%s' % (proxies[0], proxies[1])}  # 构造proxies
        already.extend(crawl(proxies))
    except Exception as e:
        proxies = random.choice(already)
        proxies = {'http': 'http://%s:%s' % (proxies[0], proxies[1])}  # 构造proxies
        already.extend(crawl(proxies))
        print('[?] 我们忽略了一个异常：', e)
    time.sleep(1 * 60)
    spawn(already)


def crawl(proxies=None):
    proxy_list = []
    try:
        for i in range(1, 3):  # 数据搜集
            url = 'http://www.xicidaili.com/wt/%s' % str(i)
            res = requests.get(url=url, headers=headers, proxies=proxies, timeout=3)
            proxy_list.extend(rex_xici.findall(res.text))  # 对于xici的 列表读取
    except:
        pass
    #  number_of_xici = len(proxy_list)
    # print('[+] 共检索到%d个IP' % number_of_xici, '-->来自西刺')
    # temp = len(proxy_list)
    try:
        for i in range(1, 10):  # 数据搜集
            url = 'http://www.66ip.cn/%s.html' % str(i)
            res = requests.get(url=url, headers=headers, proxies=None, timeout=3)
            proxy_list.extend(rex_66ip.findall(res.text))  # 对于66ip的 列表读取
    except:
        pass
    #  number_of_66ip = (len(proxy_list) - temp)
    #  print('[+] 共检索到%d个IP' % number_of_66ip, '-->来自66ip')
    #  temp = len(proxy_list)
    try:
        for i in range(1, 7):  # 数据搜集
            url = 'https://www.kuaidaili.com/free/inha/%s/' % str(i)
            res = requests.get(url=url, headers=headers, proxies=None, timeout=3)
            # print(res.text)
            proxy_list.extend(rex_kuai.findall(res.text))  # 对于快代理 的列表读取
            # print(rex_kuai.findall(res.text))
            time.sleep(1)
    except:
        pass
    #  number_of_kuai = (len(proxy_list) - temp)
    #  print('[+] 共检索到%d个IP' % number_of_kuai, '-->来自快代理')
    #  temp = len(proxy_list)
    try:
        for i in range(1, 8):  # 数据搜集
            url = 'http://www.89ip.cn/index_%s.html' % str(i)
            res = requests.get(url=url, headers=headers, proxies=None)
            proxy_list.extend(rex_89ip.findall(res.text))  # 对于89ip的 列表读取
    except:
        pass
    #  print('[+] 共检索到%d个IP' % (len(proxy_list) - temp), '-->89ip')
    print('[+] 共检索到%d个IP' % len(proxy_list))
    return proxy_list




def main():
    while True:
        global already
        # 参数初始化部分
        if len(already) > 150:
            already = []
        proxy_list = []
        #proxy_list = crawl(proxies=None)  # 爬取,此时未采用代理 , 获取啊

        # 三句代码实现重用
        res = requests.get('https://1aker.cn/open/proxies.html').text.strip('\r\n').split('<br>')
        for i in res:
            try:
                already.append(eval(i))
            except:
                pass

        for i in already:
            proxy_list.append(i)
        spawn(proxy_list)  # spawn已经有了自动去重, 并且会清空文件
        # 第一次写入完成
        proxies_crawl()  # 这函数里仍然会有睡眠42秒, 会自动spawn
        proxies_crawl()
        proxies_crawl()

if __name__ == '__main__':
    import subprocess

    if os.name != 'nt':
        subprocess.Popen('python3 flask_proxies.py', shell=True)
    erasure()  # 初始清空
    main()