# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/22 14:23
@Auth ： 章豹
@File ：demo2.py
@IDE ：PyCharm
"""
import json
import os

import requests
from locust import HttpUser, TaskSet, task, between


def get_token():
    """
    登录接口
    :return:
    """
    data = {"username": "baozhang", "password": "123456", "rememberMe": True, "source": 1}  # http://192.168.10.137
    response = requests.post("http://192.168.10.137/api/user/login", json=data)
    headers = {"Authorization": "Bearer " + response.json()["data"]["id_token"]}
    return headers


class TestUser(TaskSet):
    headers = get_token()

    @task(1)
    def contract_task(self):
        """
        合同查询
        :return:
        """
        response = self.client.get("/contractApi/bookkeeping/detail?id=12055", headers=self.headers)
        print(response.json())
        if response.status_code == 200:
            print("查询请求成功！")
        else:
            print("查询请求失败！")

    @task(3)
    def customer_task(self):
        """
        客户列表查询
        :return:
        """
        data = {"size": 10, "page": 0, "sort": "customerId,desc"}
        response = self.client.post("/bizApi/customer/filterList", headers=self.headers, json=data)
        print(response.json())
        if response.status_code == 200:
            print("查询请求成功！")
        else:
            print("查询请求失败！")


# 测试配置
class WebSitUser(HttpUser):  # 定义用户，相当于一个线程组
    wait_time = between(1, 3)
    tasks = [TestUser]
    min_wait = 3000
    max_wait = 6000


# if __name__ == '__main__':
#     os.system("locust -f demo2.py --host=http://192.168.10.137")