# -*- coding:utf-8 -*-

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings

class HttpData(object):
    def __init__(self):
        # 消除告警
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://login.huawei.com/login1/?redirect=https://netcare.huawei.com/p/netcare/new.html#/home&x_app_id=com.huawei.netcarecloud&v=V2.3.0"
        }

        self.login()
        self.getCsrfToken()



    def login(self):
        # 1. 登录获取 Cookie
        login_url = "https://login.huawei.com/login1/rest/hwidcenter/login"


        # 替换为你的用户名和密码（注意：实际中应加密或通过其他方式处理）
        data = {
            "headers": {
                "Content-Type": "application/json; charset=UTF-8"
            },
            "loginAccount": "m60079351",
            "uid": "m60079351",
            "password": "*****",
            "lang": "zh_CN",
            "cid": "",
            "targetUrl": "https%3A%2F%2Fnetcare.huawei.com%2Fp%2Fnetcare%2Fnew.html%23%2Fhome",
            "rememberAccountName": False,
            "appId": "com.huawei.netcarecloud",
            "encryptedPasswordSwitch": "off"
        }

        self.session = requests.Session()
        response = self.session.post(login_url, headers=self.headers, verify=False, data=json.dumps(data))

        if response.status_code == 200:
            print("登录成功")
            return True
        else:
            print("登录失败，状态码:", response.status_code)
            return False

    def getCsrfToken(self):
        # 2. 获取 CSRF Token
        config_url = "https://netcare.huawei.com/netcareServer/services/getSysConfig.do"
        self.headers["Referer"] = 'https://netcare.huawei.com/p/netcare/new.html'
        response = self.session.get(config_url, verify=False, headers=self.headers)

        if response.status_code == 200:
            try:
                #print(response.text)
                self.csrf_token = response.json().get('csrfToken')
                if self.csrf_token:
                    print("CSRF Token:", self.csrf_token)
                    return True
                else:
                    print("未找到 CSRF Token")
                    return False
            except Exception as e:
                print("解析 JSON 失败:", str(e))
                return False
        else:
            print("获取配置失败，状态码:", response.status_code)
            return False

    def getReCode(self, hcNo, strStatus):
        # 3. 使用 Cookie 和 CSRF Token 访问数据接口
        api_url = "https://netcare.huawei.com/adc-service/web/rest/v1/services/NetCareSDService/robustness/robustness_get_summarize_data_list"

        # 设置请求头
        self.headers["x-gde-csrf-token"] = self.csrf_token
        data = {
            "start": 0,
            "limit": 10,
            "region_code": "999999",
            "office_code": "666666",
            "country_code": "",
            "network_id": "",
            "customer_code": "",
            "product_line_code": "",
            "status":strStatus,
            "hc_code_id": hcNo,
            "hc_owner": ""
        }

        response = self.session.post(api_url, headers=self.headers, data=json.dumps(data), verify=False)

        if response.status_code == 200:
            #print("请求成功，返回数据:")
            #print(json.dumps(response.json(), ensure_ascii=False, indent=2))
            data = response.json()

            if data.get("total", 0) != 0:
                for item in data["results"]:
                    print("hcNo:", hcNo, "re_code_id:", item.get("re_code_id"))
                    return item.get("re_code_id")
            else:
                #print("total 为 0，没有数据")
                return "No"
        else:
            print("请求失败，状态码:", response.status_code)
            print("响应内容:", response.text)
            return "No"


if __name__ == "__main__":
    httpData = HttpData()
    print(httpData.getReCode('HC20250403000005'))
