import json

import requests
import datetime,re



def get_kd(dh):
    params = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "17token":"6AFA3318BFD3451E0B30D95677C2F430",
        }
    data =  [
    {
        'number': f'{dh}',
    }
]
    request = requests.post(url=f"https://api.17track.net/track/v2/register",headers=params,json=data)
    response = requests.request("POST", "https://api.17track.net/track/v2/gettracklist", headers=params)
    print(response.json())




print(get_kd())