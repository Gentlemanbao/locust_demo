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

from locust import HttpUser, task, between, events, SequentialTaskSet

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
class MyUser(SequentialTaskSet):
    #    wait_time = between(5, 15)

    @task
    def my_task(self):
        # all_semaphore.wait()
        self.client.get(
            "https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=b07fe31e001b8d11&wd=locust%E6%95%99%E7%A8%8B&rsv_spt=1&rsv_iqid=0x911851f90003e6e5&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_dl=tb&oq=locust%25E6%2595%2599%25E7%25A8%258B&rsv_btype=t&rsv_t=d1e1e%2B%2BBmzyWJgF7EFoRy94wnIZGr1EpoFdGZrVvElFh%2B2J%2F5xO1uEQk%2B4TkpLBd4cTx&rsv_pq=b07fe31e001b8d11&bs=locust%E6%95%99%E7%A8%8B&rsv_sid=40416_40445_40080_60158&_ss=1&clist=&hsug=&f4s=1&csor=8&_cr1=36293")

    @task
    def my1_task(self):
        # all_semaphore.wait()
        self.client.get("https://www.baidu.com/s?wd=locust%E5%88%86%E5%B8%83%E5%BC%8F%E8%BF%90%E8%A1%8C&pn=10&oq=locust%E5%88%86%E5%B8%83%E5%BC%8F%E8%BF%90%E8%A1%8C&tn=baiduhome_pg&ie=utf-8&rsv_idx=2&rsv_pq=e964452e00007678&rsv_t=c65eZbjPDSxQPSk8rZOC%2F6Sco62JP%2F1NcJtWX53z59cLcZEvbVQKNvG97j1NpOouJyez")


class WebSitUser(HttpUser):  # 定义用户，相当于一个线程组
    wait_time = between(1, 3)  # 意思是每个用户执行任务的时候随机等待1-3秒的随机时间
    tasks = [MyUser]
    min_wait = 3000
    max_wait = 6000

# if __name__ == '__main__':
#     os.system("locust -f demo_test.py --host=https://www.baidu.com --headless -u 20 -r 2 -t 30s --html=./report/report.html")

    # "locust -f demo_分布式.py --master --host=https://www.baidu.com --headless -u 20 -r 2 -t 60s --html=/root/apache-tomcat-9.0.88/webapps/test/report.html" 现在主机上执行这个命令
    # " locust -f .\demo_分布式.py --worker --master-host=121.40.158.77" 然后在从机地方执行这个脚本