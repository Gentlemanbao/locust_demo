# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/25 14:53
@Auth ： 章豹
@File ：demo_test.py
@IDE ：PyCharm
"""
from sqlalchemy.sql import events

# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/25 14:53
@Auth ： 章豹
@File ：demo_test.py
@IDE ：PyCharm
"""
import os

from locust import HttpUser, task, between, events

from gevent._semaphore import Semaphore


# 创建计数器
all_semaphore = Semaphore()
# 如果计数器为0则阻塞线程
all_semaphore.acquire()


# 创建钩子函数
def on_math_complete(**kwargs):
    all_semaphore.release()


# 挂在到locust钩子函数（所有的Locust示例产生完成时触发）
events.spawning_complete.add_listener(on_math_complete)
num=0
class MyUser(HttpUser):
    #    wait_time = between(5, 15)

    @task
    def my_task(self):
        # all_semaphore.wait()
        self.client.get(
            "https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=b07fe31e001b8d11&wd=locust%E6%95%99%E7%A8%8B&rsv_spt=1&rsv_iqid=0x911851f90003e6e5&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&oq=locust%25E6%2595%2599%25E7%25A8%258B&rsv_btype=t&rsv_t=d1e1e%2B%2BBmzyWJgF7EFoRy94wnIZGr1EpoFdGZrVvElFh%2B2J%2F5xO1uEQk%2B4TkpLBd4cTx&rsv_pq=b07fe31e001b8d11&bs=locust%E6%95%99%E7%A8%8B&rsv_sid=40416_40445_40080_60158&_ss=1&clist=&hsug=&f4s=1&csor=8&_cr1=36293")

    @task
    def my1_task(self):
        # all_semaphore.wait()
        self.client.get("https://blog.csdn.net/Main123464644/article/details/136524975")

    @task
    def my1_task(self):
        # all_semaphore.wait()
        self.client.get("https://grafana.com/grafana/dashboards/1860-node-exporter-full/")

# if __name__ == '__main__':
# os.system("locust -f demo_test.py --host=http://localhost --headless -u 20 -r 2 -t 30s --html=./report/report.html")
# os.system("locust -f demo_test.py --host=https://www.baidu.com")
