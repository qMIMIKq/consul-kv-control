import requests, json, base64


def get_data():
    data = requests.get(
        'http://127.0.0.1:8500/v1/kv?recurse'
    ).json()

    dec_data = list(map(lambda kv: {
        'path': kv['Key'],
        'mod_id': kv['ModifyIndex'],
        'value': json.loads(base64.b64decode(kv['Value']).decode('utf-8'))
    }, data))

    return data, dec_data
