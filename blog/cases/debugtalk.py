import requests
import os

host = "http://127.0.0.1:8000/"

def token(user='guolong', pwd='admin123456'):
    login_url= host + "api/v1/logintoken/"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": user,
        "password": pwd
    }
    r = requests.post(login_url, headers=headers, json=body)
    try:
        return_token = r.json()["token"]
    except:
        print('返回内容：{}'.format(r.text))
        return_token = ''
    return return_token

def hook_up():
    print("前置操作：setup!")

def hook_down():
    print("后置操作：teardown!")

def hook_log(var=''):
    print('用例执行：{}'.format(var))

def ENV(keyname):
    value = os.environ.get(keyname, '')
    return value

if __name__ == '__main__':
    print('token是：{}'.format(token()))