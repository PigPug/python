from time import sleep
import requests
import re
import json
import base64
import sys
import os
import time
import wget

headers ={
    'cookie' : 'MONITOR_WEB_ID=7158831357212067341; _tea_utm_cache_1300=undefined; ttcid=f4d74dcceedb498683a06599f6934adf21; ixigua-a-s=1; support_webp=true; support_avif=true; __ac_nonce=0635a5536000e08a0d04e; __ac_signature=_02B4Z6wo00f01UAWoCwAAIDBwBRabkvU7EFANqSAADNj0jnxpMCXeyc5O1x8YZDCmJoickYEhtckJGNFLwPLdd6Rchr7MRGlStTlBXaGm-UU2iVGDa7TEMt7-66sqSx4cJ2c7vfrouLME9VJ2b; tt_scid=80KnvGywa-CMEHd2BaJ0cCQR9ixCupyKPxk0rx667dfA6q.qtrCx7s0pyBn9xTyM757a; ttwid=1|oEqyFbtcBRhIcLbG-Mlb-LE8b2zCmgnuXauzfc6-C6k|1666865580|a55b9b62586ef54c486d6e1b4e974d3e0b896a39fa464d9bb6e64ce42b0ece57; msToken=AUr-4Tzy1pNMNMhM3b3v_5WtDOv8ErwAUas0JJE9JrsbSFY7-YxUQzLVT2-jztZqHvOAJNt2y7AwSxFawpwFNKPnfXnLYHA0eMJ9H92Ys9fZVTfLiqR6',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

download_path = os.path.join(os.getcwd(), "西瓜视频下载")

def download_video(video_name, video_url):
    print(f"{video_name} 开始下载...")
    video_res = requests.get(video_url, headers=headers)
    video_path = download_path
    print(f"{video_path}")
    # 如果不存在则创建视频文件夹存放视频
    if not os.path.exists(video_path):
        os.mkdir(video_path)
    with open(f"{video_path}/{video_name}.mp4", "wb") as video_file:
        video_file.write(video_res.content)
    print(f"{video_name} 下载完毕")
    return

def parse_xigua(url):

    url = url

    response=requests.get(url=url, headers=headers)

    response.encoding='utf-8'

    html_data=response.text
    #print(html_data)

    json_str=re.findall('_SSR_HYDRATED_DATA=(.*?)</script>',html_data)[0]
    #print(json_str)

    json_dict=json.loads(json_str.replace('undefined','null'))

    # 格式化打印 json dict数据
    #print(json.dumps(json_dict, sort_keys=True, indent=4, separators=(', ', ': ')))

    title=main_url=json_dict['anyVideo']['gidInformation']['packerData']['video']['title']

    #main_url=json_dict['anyVideo']['gidInformation']['packerData']['video']['videoResource']['normal']['video_list']['video_5']['main_url']
    video_list_dict=json_dict['anyVideo']['gidInformation']['packerData']['video']['videoResource']['normal']['video_list']

    # 查找清晰度最好的视频, video_5 4K, video_4 1080p, video_3 720p, video_2 480p, video_1 360p
    video_idx=5
    for i in range(6,0,-1):
        has_video=video_list_dict.__contains__('video_'+str(i))
        if has_video:
            print(str(i))
            video_idx=i
            break

    main_url=json_dict['anyVideo']['gidInformation']['packerData']['video']['videoResource']['normal']['video_list']['video_'+str(video_idx)]['main_url']
    video_url=base64.b64decode(main_url).decode()
    print(title)
    print(video_url)
    return title, video_url


##----PySimpleGUI--------------------------------------------
import PySimpleGUI as sg
import webbrowser
import pyperclip
def videoPySimpleGUI():
    layout = [
        [sg.Text('原视频地址:'), sg.Input(default_text="", size = (100, 1), key='-URL-'),  sg.Button('清除'), sg.Button('粘贴'), sg.Button('解析')],
        [sg.Text('源视频地址:'), sg.Multiline(key = "-VIDEO_URL-", size = (98, 5)), sg.Button('复制'),sg.Button('打开'),sg.Button('下载')],
        [sg.Text('视频的标题:'), sg.Input(default_text="", size = (100, 1), key='-VIDEO_TITLE-'),sg.Input(default_text="下载状态", size = (8, 1), key='-DOWNLOAD_STATUS-'),sg.Button('打开路径')]
    ]
    window = sg.Window(f'西瓜视频下载({os.getcwd()})', layout)
    while True:
        event, values = window.read()   # 窗口的读取，有两个返回值（1.事件，2.值）
        print(values)
        url = values['-URL-']
        if event == "粘贴":
            text = pyperclip.paste()
            window["-URL-"].update(text)
        if event == "清除":
            window["-URL-"].update("")
            window["-VIDEO_URL-"].update("")
            window["-VIDEO_TITLE-"].update("")
            window["-DOWNLOAD_STATUS-"].update("下载状态")
        if event =="解析" and url != "":
            video_title, video_url = parse_xigua(url)
            window["-VIDEO_TITLE-"].update(video_title)
            window["-VIDEO_URL-"].update(video_url)
        if event == "复制":
            pyperclip.copy(video_url)
        if event == "打开":
            webbrowser.open(video_url)
        if event == "下载" and video_url != "":
            download_video(video_title, video_url)
            window["-VIDEO_TITLE-"].update(video_title)
            window["-DOWNLOAD_STATUS-"].update("下载完成")
        if event == "打开路径":
            os.system("explorer.exe %s" % download_path)
        if event == None:   # 窗口关闭事件
            break


if __name__ == '__main__':
    videoPySimpleGUI()