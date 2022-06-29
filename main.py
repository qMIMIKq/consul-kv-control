from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from modules.control_db import init_table_kvs, control_kvs_updates
from modules.get_filtered_db import get_filtered_db, get_db_by_id
from modules.update_control import update_control


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kv-control.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class KVControl(db.Model):
    __tablename__ = 'kvs'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=True)
    version = db.Column(db.Integer)
    mod_id = db.Column(db.Integer)
    mod_keys = db.Column(db.String, nullable=True, default='Init')
    prev_value = db.Column(db.JSON)
    cur_value = db.Column(db.JSON, nullable=True)
    changes = db.Column(db.JSON, default='Init')
    date = db.Column(db.String, default=str(datetime.now())[0:-7])
    checked = db.Column(db.Boolean, default=False)


# control_kvs_updates(db, KVControl)

@app.route('/', methods=['GET', 'POST'])
def index_view():
    data = get_filtered_db(db, KVControl)

    return render_template(
        'index.html',
        style='style/index.css',
        data=data.all(),
        t=type(data),
        date=str(datetime.now())[0:-7]
    )


@app.route('/full-kv-info/<int:kv_id>', methods=['GET', 'POST'])
def full_kv_info_view(kv_id):
    data = get_db_by_id(db, KVControl, kv_id)

    return render_template(
        'full-kv-info.html',
        style='style/index.css',
        d=data,
        # m_d=mapping_data
    )


if __name__ == '__main__':
    init_table_kvs(db, KVControl)
    update_control(control_kvs_updates, 9, db, KVControl)
    app.run(debug=True, port=3000)
