def get_filtered_db(db, DbName, filter_by='default'):
    if filter_by == 'default':
        data = db.session \
            .query(DbName) \
            .filter(DbName.checked != 1) \
            .order_by(DbName.date.desc())

        return data


def get_db_by_id(db, DbName, db_id):
    data = db.session.query(DbName).get(db_id)

    return data

    # filter(KVControl.path == 'check/settings/alarm')
    # filter(str_date == KVControl.date)
