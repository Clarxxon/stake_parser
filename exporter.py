import json
import requests
import time

from prometheus_client import start_http_server, Info
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

cerberus_link = "https://api.cerberus.zone:1317/staking/validators" \
                "/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy"
ki_link = "https://api-mainnet.blockchain.ki/staking/validators/kivaloper19seaxuh9wp3zum42w6flrjsr5raptxhy3l8qvw"


i = Info('coingecko_metric', 'Mintscan info', ['chain'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'}

validators = [
    {'name': 'cerberus-2',
     'url': "https://api.cerberus.zone:1317/staking/validators/cerberusvaloper1xjgspyv73d3k3ewygu0v2gcwwplwxkxg03reqy"
     },
    {'name': 'ki',
     'url': "https://api-mainnet.blockchain.ki/staking/validators/kivaloper19seaxuh9wp3zum42w6flrjsr5raptxhy3l8qvw"
     },
    {'name': 'ixo',
     'url': "https://impacthub.ixo.world/rest/staking/validators/ixovaloper12g6xke0lu758u8dtan8efsdhe2xxwxwh4lrjax"
     },
]


def process_request(t, link, net_name):
    parsed_json = requests.get(link).json()
    coin_cost = float(cg.get_price(
        ids=net_name, vs_currencies='usd').get(net_name).get('usd'))
    bounded_tokens = {'net_name': net_name, 'staked tokens': str(float(parsed_json.get('result').get('tokens')) / 1000000),
                      'turnover': str(float(parsed_json.get('result').get('tokens')) / 1000000 * coin_cost)}

    return bounded_tokens
    # time.sleep(t)


def job():
    for validator in validators:
        try:
            bound_tokens = process_request(
                10, validator['url'], validator['name'])
            print(bound_tokens)

            i.labels(chain=validator['name']).info({
                f"staked tokens": bound_tokens['staked tokens'],
                f"turnover": bound_tokens['turnover'],
            })
        except Exception:
            i.labels(chain=validator['name']).info({
                f"staked tokens": -1,
                f"turnover": -1
            })


if __name__ == '__main__':
    t = 10
    start_http_server(9879)
    #cerberus_bounded_tokens = Info('my_inprogress_requests', 'cerberus')
    #ki_bounded_tokens = Info('my_inprogress_requests', 'ki')
    while True:
        job()
        #process_request(t, ki_link, 'ki')
        time.sleep(10)
