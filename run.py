import requests
import json
import subprocess
# 生成数列
months = []
dates = []
formatted_dates = []
for year in range(2023, 2025):
    for month in range(1, 13):
        if (year == 2023 and month < 10) or (year == 2024 and month > 8):
            continue
        months.append(f"{year}{month:02d}")
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh,zh-CN;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "www.rthk.hk",
    "Referer": "https://www.rthk.hk/radio/radio3/programme/pete_magical_mystery_tour",
    "Sec-CH-UA": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"macOS"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "X-Requested-With": "XMLHttpRequest"
}

# 请求的 URL
for month in months:
    url = f"https://www.rthk.hk/radio/catchUpByMonth?c=radio3&p=pete_magical_mystery_tour&m={month}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
    # 检查内容编码
        if response.headers.get('Content-Encoding') == 'br':
            
            data = response.content.decode('utf-8')
            # print(decompressed_data)  # 输出解压后的二进制数据
            date_json=json.loads(data)
            dates = [item['date'] for item in date_json['content']]
            
            for date in dates:
                formatted_dates.append(f"{date[6:]}{date[3:5]}{date[:2]}")
        else:
            print(response.text)  # 直接输出文本
    else:
        print(f"请求失败，状态码x: {response.status_code}")
print(formatted_dates)
for index, date in enumerate(formatted_dates):
    m3u8_url = f"https://rthkaod2022.akamaized.net/m4a/radio/archive/radio3/pete_magical_mystery_tour/m4a/{date}.m4a/index_0_a.m3u8"
    subprocess.run(["ffmpeg", "-i", m3u8_url, 
                    "-i", m3u8_url,
                    "-c", "copy",
                    "-threads", "4",
                    "-buffer_size", "1024k",
                    f"pete_magical_mystery_tour{date}.m4a"
                ]
                    )
    print(f"Processing {date}... ({index + 1}/{len(dates)})")
