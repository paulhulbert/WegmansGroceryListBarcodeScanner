import requests
import json


def get_item_by_upc(upc):
    url = f"https://shop.wegmans.com/api/v2/store_products?allow_autocorrect=true&limit=60&offset=0&search_provider=buffet&search_term={upc}&secondary_results=false&sort=rank"

    payload = {}
    headers = {
        'cookie': open('cookie.txt', 'r').read()
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    item = json.loads(response.text)['items'][0]
    print(item)
    if response.status_code != 200:
        pushbullet_message("Wegmans", f"Failed to get item with UPC: {upc}")
    return item


def add_item_by_upc(upc):
    item = get_item_by_upc(upc)
    url = "https://shop.wegmans.com/api/v2/user_lists/default"
    headers = {
        'cookie': open('cookie.txt', 'r').read()
    }

    payload_json = json.loads('{"discount_total":"0.0","href":"/user_lists/default","id":"31368411","ids":{"grocery":"194098"},"item_count":1,"items":[{"id":"' + str(item['id']) + '","quantity":1,"order_by_weight":false,"product_config":null,"item_type":"store_product"}],"modified":"2021-06-01T20:05:09.569597+00:00","name":"default","offer_progress":[],"offer_total":"0","points":{"awarded":0},"pre_discount_product_total":"22.26","product_total":"22.26"}')
    payload_json['items'][0]['store_product'] = item
    response = requests.request("PUT", url, headers=headers, json=payload_json)
    print(response.text)
    if response.status_code != 200:
        pushbullet_message("Wegmans", f"Failed to add item to list: {item['name']}")
    else:
        pushbullet_message("Wegmans", f"Added item to list: {item['name']}")


def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    TOKEN = open('pushbullet.txt', 'r').read()
    resp = requests.post('https://api.pushbullet.com/v2/pushes',
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error', resp.status_code)
    else:
        print('Message sent')


if __name__ == '__main__':
    add_item_by_upc("644124696437")

