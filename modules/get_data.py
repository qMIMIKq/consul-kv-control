import json
import consul


c = consul.Consul()


def get_data():
    index, data = c.kv.get('', recurse=True)

    dec_data = filter(lambda kv: kv['Key'] != 'exclude-keys', data)
    dec_data = list(map(lambda kv: {
        'path': kv['Key'],
        'mod_id': kv['ModifyIndex'],
        'value': json.loads(kv['Value'].decode('utf-8'))
    }, dec_data))

    return data, dec_data


def get_exclude_keys():
    index, data = c.kv.get('exclude-keys')

    return data['Value'].decode('utf-8').split(' ')