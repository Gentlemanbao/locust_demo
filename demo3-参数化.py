# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/22 14:23
@Auth ： 章豹
@File ：demo2.py
@IDE ：PyCharm
"""
import json
from queue import Queue
import os
from util.read_data import read_csv
import requests
from locust import HttpUser, TaskSet, task, between, SequentialTaskSet
from util.log_print import get_logger

logger = get_logger()


def get_token():
    """
    登录接口
    :return:
    """
    data = {"username": "baozhang", "password": "123456", "rememberMe": True, "source": 1}
    response = requests.post("http://192.168.10.137/api/user/login", json=data)
    headers = {"Authorization": "Bearer " + response.json()["data"]["id_token"]}
    return headers


def red_csv():
    """
    读取文件并且将参数化的数据放入列队中
    :return:
    """
    q = Queue()
    data = read_csv("./test_csv.csv")
    print(data)
    for i in data:
        q.put(i)
    return q


class TestUser(SequentialTaskSet):
    """
    继承SequentialTaskSet和TaskSet的区别是，SequentialTaskSet是按照类下面的方法一次执行任务，并且不是随机的，所以
    如果有特定的任务顺序的task，可以用SequentialTaskSet
    """
    headers = get_token()
    q = red_csv()

    @task(3)
    def contract_task(self):
        """
        合同查询,并且进行参数化
        :return:
        """
        contract_id = self.q.get()  # 使用 get() 方法从队列中获取元素,注意取出来的是一个列表，但是只有一个元素
        logger.info(f"合同id-----------{contract_id[0]}，{type(contract_id)}")
        par = {"id": contract_id[0]}
        with self.client.get("/contractApi/bookkeeping/detail", headers=self.headers, params=par,
                             catch_response=True) as response:
            logger.info(f"{response.json()}")
            self.q.put(contract_id)  # 注意这个用完还行需要添加到列表，不然参数化中的数据用完之后就不会有contract_id传参数据，会导致不继续执行，意思就是这些参数化数据循环利用
            if response.status_code == 200 and str(response.json()["data"]["contractBasic"]["contractId"]) == contract_id[0]:
                response.success()
            else:
                logger.info(f"{response.json()['data']['contractBasic']['contractId']}-------{contract_id[0]}")
                response.failure("Response code wrong!")

    @task(1)
    def customer_task(self):
        """
        客户列表查询
        :return:
        """
        data = {"size": 10, "page": 0, "sort": "customerId,desc"}
        with self.client.post("/bizApi/customer/filterList", headers=self.headers, json=data,
                              catch_response=True) as response:
            logger.info(f"{response.json()}")
            if response.status_code == 200:
                response.success()
            else:
                response.failure("Response code wrong!")


# 测试配置
class WebSitUser(HttpUser):  # 定义用户，相当于一个线程组
    wait_time = between(1, 3)  # 意思是每个用户执行任务的时候随机等待1-3秒的随机时间
    tasks = [TestUser]
    min_wait = 3000
    max_wait = 6000


# if __name__ == '__main__':
#     os.system("locust -f demo3-参数化.py --host=http://192.168.10.137")