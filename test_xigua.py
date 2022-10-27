import requests
import re
import json
import base64
import sys

def download_xigua(url):

    url = url

    headers ={
        'cookie' : 'MONITOR_WEB_ID=7158831357212067341; _tea_utm_cache_1300=undefined; ttcid=f4d74dcceedb498683a06599f6934adf21; ixigua-a-s=1; support_webp=true; support_avif=true; __ac_nonce=0635a5536000e08a0d04e; __ac_signature=_02B4Z6wo00f01UAWoCwAAIDBwBRabkvU7EFANqSAADNj0jnxpMCXeyc5O1x8YZDCmJoickYEhtckJGNFLwPLdd6Rchr7MRGlStTlBXaGm-UU2iVGDa7TEMt7-66sqSx4cJ2c7vfrouLME9VJ2b; tt_scid=80KnvGywa-CMEHd2BaJ0cCQR9ixCupyKPxk0rx667dfA6q.qtrCx7s0pyBn9xTyM757a; ttwid=1|oEqyFbtcBRhIcLbG-Mlb-LE8b2zCmgnuXauzfc6-C6k|1666865580|a55b9b62586ef54c486d6e1b4e974d3e0b896a39fa464d9bb6e64ce42b0ece57; msToken=AUr-4Tzy1pNMNMhM3b3v_5WtDOv8ErwAUas0JJE9JrsbSFY7-YxUQzLVT2-jztZqHvOAJNt2y7AwSxFawpwFNKPnfXnLYHA0eMJ9H92Ys9fZVTfLiqR6',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

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

if __name__ == '__main__':
    url = sys.argv[1]   # 接收位置参数
    download_xigua(url)