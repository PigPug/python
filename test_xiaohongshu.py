import requests
import os
from bs4 import BeautifulSoup
import re
import json
import pprint
import sys

# 首页地址
url = 'https://www.xiaohongshu.com/user/profile/58dfd85050c4b435fe051093'
# 笔记地址
url = 'https://www.xiaohongshu.com/discovery/item/636f7453000000001b00c33f'

download_root = os.path.join(os.getcwd(), "小红书图片下载")

url_root = 'https://www.xiaohongshu.com'

# 无水印图片基地址
url_base = 'https://ci.xiaohongshu.com/'

headers = {
    'Cookie': 'extra_exp_ids=ios_wx_launch_open_app_origin,h5_video_ui_exp3,wx_launch_open_app_duration_origin,ques_clt2;timestamp2.sig=g-ADvN3pWARSY23-Mya-aF71CgZ_olSl1thzirRBMdU; timestamp2=16684262871256414d6e7e8b77b7b9fb3e8e3efa69531acd3418dfc94bf7080; customerClientId=456896320453373; a1=1844bd93ab13u5j13cucz2n0whafj00x2shif69x900000246637;gid=yY44DfjqSfJiyY44Dfjq0MKjDyq72VyqS7SuxCjJI8Ex0388iV88Ci888J4KKqW844S4YSD2; gid.sign=Wd12hahlgEeTLe4cdoy+qMnv+dI=; xhsTracker=url=noteDetail&xhsshare=CopyLink; gid.ss=gSMQ9UOnDuZwH2oRGJG6BW6e4grs67TaYpnrW+8Wmd3JbfrnOuV5G1TU7gZ9fP6D; xhsTrackerId=9081d5bb-dd58-41f9-c106-28fece03da12',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'
}

proxyip = {
    'http': 'http://27.203.215.138:8060'
}

def download_item(url='', download_path = download_root):

    if url == '':
        print("请输入小红书博主笔记地址!")
        return 

    item_id = url.split('/')[-1]
    #download_path = download_path + '/' + item_id
    
    response = requests.get(url=url, headers=headers, timeout = 1, proxies = proxyip)

    page_source=BeautifulSoup(response.text, 'html.parser').prettify()

    with open("index.html", mode = 'w', encoding='utf-8') as file:
        file.write(page_source)

    #print(page_source)

    imageList = re.findall('"imageList":(.*?),"cover"', response.text)[0]

    #print(imageList)
    #print(type(imageList))

    json_data = json.loads(imageList)
    #pprint.pprint(json_data)
    #print(type(json_data))
    #return

    for img in json_data:
        #pprint.pprint(img['fileId'])
        fileId = img['fileId']
        image_url = url_base + fileId
        print(image_url)
        # response = requests.get(url=image_url, headers=headers)
        # print(response)

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # 'fileId': 'bw1/81b73236-4958-4152-bec2-55a7506b7d07'
        image_name = fileId.replace('/', '_')
        print(image_name)
        image_file = f'{download_path}' + '/' + f'{image_name}.jpg'
        if not os.path.exists(image_file):

            with open(image_file, 'wb') as v:
                try:
                    r = requests.get(url=image_url, headers=headers, timeout = 1, proxies = proxyip)
                    v.write(r.content)
                except Exception as e:
                    print('图片下载错误！')
        else:
            print(f"{image_name} 已下载过")

    print("笔记图片下载完成!")

def download_profile(url='', download_path = download_root):
    if url == '':
        print("请输入小红书博主首页地址!")
        return

    profile_id = url.split('/')[-1]
    #download_path = download_path + '/' + profile_id

    response = requests.get(url=url, headers=headers, timeout = 1, proxies = proxyip)

    page_source=BeautifulSoup(response.text, 'html.parser').prettify()
    with open("index.html", mode = 'w', encoding='utf-8') as file:
        file.write(page_source)
    #print(page_source)

    items = re.findall('href="(.*?)"', response.text)
    #print(items)

    for item in items:
        if "item" in item:
            item_url= url_root + item
            #print(item_url) 
            # response = requests.get(url=item_url, headers=headers, timeout = 1, proxies = proxyip)
            # print(response)
            download_item(item_url, download_path)

    print("所有图片下载完成!")


if __name__ == '__main__':
    url = sys.argv[1]
    
    if url == '':
        print("请输入下载地址!")
        quit()

    if 'profile' in url:
        download_profile(url)
    elif 'item' in url:
        download_item(url)
    else:
        print("请检查下载地址!")
