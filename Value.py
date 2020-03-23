import requests
import json
import time 
import pandas as pd

def latest_qieman():
   url = r'https://qieman.com/pmdj/v2/idx-eval/latest' # 且慢
   json_data = request_url(url)
   current_date_temp = list(str(json_data['date']))
   current_date_temp.insert(10,'.')
   current_date = float(''.join(current_date_temp))
   
   json_body = pd.read_json(json.load(json_data['idxEvalList']))
   
   print(json_body)
   items = parse_result(json_data)
   return current_date, items

def request_url(url):
    try:
        header = {
            'Connection': 'keep-alive',
            'Host': 'qieman.com',
            'Referer': 'https://qieman.com/idx-eval',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'x-aid': 'A.8B12C9D01E42PY0TR4VKQ6M1V70RNZZ0M',
            'x-request-id': 'albus.6F8821079F3CE04B2772',
            'x-sign': '1584934951170D4046B0EEEED4EE9C36625C8F9C21081'
        }

        response = requests.get(url, headers = header)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None

def parse_result(json_data):    
    for item in json_data['idxEvalList']:
        yield {
            'indexName':item['indexName'],
            'indexCode':item['indexCode'],
            'pe':item['pe'],
            'peHigh':item['peHigh'],
            'peLow':item['peLow'],            
            'pePercentile':item['pePercentile'],
            'pb':item['pb'],
            'pbLow':item['pbLow'],
            'pbHigh':item['pbHigh'],
            'pbPercentile':item['pbPercentile'],
            'roe':item['roe'],
            'scoreBy':item['scoreBy'],
            'source':item['source'],
            'group':item['group']
        }


if __name__ == "__main__":
    current_date, items = latest_qieman()
    timestamp = time.strftime("%Y-%m-%d",time.localtime(current_date))
    with open('qieman_' + timestamp + '.txt','a',encoding='UTF-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + '/n')
        f.close()

