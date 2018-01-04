#-*- coding:utf-8 -*-

import sys
import re
import requests
from scrapy.selector import Selector
import MySQLdb
import pymysql.cursors

##数据库链接信息
# config = {
#     'host': '127.0.0.1',
#     'port': '3306',
#     'user': 'root',
#     'password': '',
#     'db': 'proxy_ip',
#     'charset': 'utf8',
#     'cursorclass': pymysql.cursors.DictCursor
# }
reload(sys)
sys.setdefaultencoding('utf8')

## 创建链接
conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='proxy_ip', charset='utf8')
cursor = conn.cursor()


def crawl_ips():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"}

    for i in range(2572):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]  # ip
            port = all_texts[1]
            proxy_type = all_texts[5]
            ip_list.append((ip, port, proxy_type, speed))
        print(ip_list)

        for info in ip_list:
            ip = info[0]
            port = info[1]
            speed = info[3]
            proxy_type = info[2]
            if proxy_type.replace("\n", " ") == "":
                proxy_type = 'HTTP'

            # 执行sql语句，插入记录
            cursor.execute(
                "INSERT  ip (ip, port, speed, proxy_type) VALUES ('{0}','{1}',{2},'{3}')".format(ip, port, speed, proxy_type)
            )
            #cursor.close()
            conn.commit()
            #conn.close()


class GetIp(object):
    def delete_ip(self, ip):
        #从数据库删除无效的ip
        delete_sql = "delete from ip where ip='{0}'".format(ip)
       # print(delete_sql)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)

        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >=200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        #从数据库中随机获取一个可用ip
        random_sql = "SELECT ip,port FROM ip ORDER BY RAND() LIMIT 1"
        cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            #if ip_info == "":
               # crawl_ips()
            #print ip_info
            ip = ip_info[0]
            port = ip_info[1]
            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


#print(crawl_ips())
#if __name__ == "__main__":

#getIP = GetIp()
#print(getIP.get_random_ip())
# def test():
#  #   list = ["\r\n                                                                                                                            ", "自媒体机构", "\r\n                                                                                                                            ", "自媒体", "\r\n                                                                                                                            ", "心灵鸡汤", "\r\n                                                                                                                            ", "情感", "\r\n                                                                                                                            ", "美发", "\r\n                                                                                                                            ", "美体", "\r\n                                                                                                                            ", "穿搭", "\r\n                                                                                                                            ", "美妆", "\r\n                                                                                                                            ", "购物", "\r\n                                                                                                                        ", "\r\n                                                                                                                                                                        "]
#     url = "background:url(http://wx.qlogo.cn/mmhead/Q3auHgzwzM69LTbDm6MVzczu0yvF9fPLJ9w92kowPuo0T6JMiavTCDQ/0) -0px -0px no-repeat;background-size:80px 80px; width: 80px;height:80px;"
#     img = re.findall(r'[^()]+', url)[1]
#
#     print(img)
#
#
#
#     # aa = []
#     # for index in list:
#     #     #print(list[index])
#     #     #print(a)
#     #     if index.replace("\r\n", " ").strip() != "":
#     #         aa.append(index)
#    # print(wci)
#
# test()
