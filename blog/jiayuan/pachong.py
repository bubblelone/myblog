import requests
import json
import time
import re


def fetchURL(url):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'unicode_escape'
        print(r.url)
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parserHtml(html):
    '''
    功能：根据参数 html 给定的内存型 HTML 文件，尝试解析其结构，获取所需内容
    参数：
            html：类似文件的内存 HTML 文本对象
    '''
    s = json.loads(html, strict=False)

    usrinfo = []

    for key in s['userInfo']:
        blist = []

        realUid = key['realUid']
        nickname = key['nickname']
        sex = key['sex']
        age = key['age']
        work_location = key['work_location']
        height = key['height']
        education = key['education']

        matchCondition = key['matchCondition']
        marriage = key['marriage']
        income = key['income']
        shortnote = key['shortnote']
        image = key['image']


        blist.append(realUid)
        blist.append(nickname)
        blist.append(sex)
        blist.append(age)
        blist.append(work_location)
        blist.append(height)
        blist.append(education)
        blist.append(matchCondition)
        blist.append(marriage)
        blist.append(income)
        blist.append(shortnote)
        blist.append(image)

        randListTag = key['randListTag']
        print(randListTag)
        reg = '\d{2}公斤'
        temp = re.search(reg, randListTag, flags=0)
        if temp is None:
            print('temp is None')
        elif temp == '':
            print('temp is 空string')
        else:
            weightString = temp.group()
            weight = int(weightString[:2])
            if weight >= 60:

                blist.append(weight)

                usrinfo.append(blist)
        print(nickname, age, work_location)

    writePage(usrinfo)
    print('---' * 20)


def writePage(urating):
    '''
        Function : To write the content of html into a local file
        html : The response content
        filename : the local filename to be used stored the response
    '''

    import pandas as pd
    dataframe = pd.DataFrame(urating)
    dataframe.to_csv('Jiayuan_UserInfo.csv', mode='a', index=False, sep=',', header=False)


if __name__ == '__main__':
    for page in range(26, 700):
        url = 'http://search.jiayuan.com/v2/search_v2.php?key=&sex=f&stc=1:4403,2:20.30,23:1&sn=default&sv=1&p=%s&f=select' % str(
            page)
        html = fetchURL(url)
        parserHtml(html)


        # 为了降低被封ip的风险，每爬100页便歇5秒。
        if page % 2 == 1:
            time.sleep(3)