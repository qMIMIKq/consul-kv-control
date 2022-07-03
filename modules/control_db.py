import json
from datetime import datetime

from modules.get_data import get_data


exclude_keys = ['check/ignore']


def init_table_kvs(db, DbName):
    """Проверяем есть ли по ключу path значение в БД и добавляем, если нет"""

    data = get_data()

    for kv in data[1]:
        if kv['path'] in exclude_keys:
            continue

        if len(db.session.query(DbName).filter(DbName.path == kv['path']).all()):
            continue
        else:
            try:
                kv_data = DbName(
                    path=str(kv['path']),
                    mod_id=int(kv['mod_id']),
                    version=int(kv['value']['version']),
                    prev_value=kv['value'],
                    cur_value=kv['value'],
                    # checked=True
                )
                db.session.add(kv_data)

                db.session.commit()
            except:
                print('Не получилось')


changes_list = []


def control_kvs_updates(db, DbName):
    """Отправляем запрос и проверем mod_id, если отличился собираем изменившиеся ключи и значения"""

    data = get_data()

    for kv in data[1]:
        if kv['path'] in exclude_keys:
            continue

        prev_data = db.session.query(DbName) \
            .filter(DbName.path == kv['path']) \
            .all()[-1]

        if int(kv['mod_id']) != prev_data.mod_id:
            prev_val = prev_data.cur_value
            cur_val = kv['value']

            mod_keys = []
            changes = {}
            for key in cur_val:
                if json.dumps(cur_val[key]) != json.dumps(prev_val[key]):
                    mod_keys.append(key)

                    if type(cur_val[key]) == dict or type(cur_val[key]) == list:
                        get_changed_values(prev_val[key], cur_val[key])
                        changes[key] = [item for item in changes_list]

                        changes_list.clear()
                    else:
                        changes[key] = {
                            'prev': prev_val[key],
                            'cur': cur_val[key]
                        }

            if len(mod_keys):
                try:
                    kv_data = DbName(
                        path=str(kv['path']),
                        mod_id=int(kv['mod_id']),
                        version=int(kv['value']['version']),
                        prev_value=prev_val,
                        cur_value=cur_val,
                        mod_keys=', '.join(mod_keys),
                        changes=changes,
                        date=str(datetime.now())[0:-7]
                    )
                    db.session.add(kv_data)

                    db.session.commit()
                except:
                    print('Не получилось')


def get_changed_values(prev_obj, cur_obj, changes=None, changed_i=None):
    if not changes:
        changes = changes_list

    if type(cur_obj) == list:
        for i in range(len(cur_obj)):
            if type(prev_obj[i]) != dict and type(prev_obj[i]) != list and prev_obj[i] != cur_obj[i]:
                changes.append({
                    'index': i,
                    'prev': prev_obj[i],
                    'cur': cur_obj[i]
                })

            get_changed_values(prev_obj[i], cur_obj[i], changes, i)

    elif type(cur_obj) == dict:
        for change in changes:
            for c_key, c_value in change.items():
                print(f'{c_key}: {c_value}')

        for key, value in cur_obj.items():
            if json.dumps(value) != json.dumps(prev_obj[key]):
                if changed_i is not None:

                    changes.append({
                        'index': changed_i,
                        'prev': {
                            key: prev_obj[key]
                        },
                        'cur': {
                            key: value
                        }
                    })
                else:
                    changes.append({
                        'prev': {
                            key: prev_obj[key]
                        },
                        'cur': {
                            key: value
                        }
                    })

            get_changed_values(value, cur_obj[key], changes, changed_i)

    return 1
