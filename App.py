from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html', title="ログイン画面",  message="温度管理アプリを始める前にパスワードを入れてください")

@app.route('/login')
def loginurl():
    return render_template('login.html')

@app.route('/index1', methods=['GET'])
def index1():
    return render_template('index1.html', message="")

@app.route('/index1', methods=['POST'])
def form2():
    field1 = request.form['field1']
    return render_template('index1.html', message="温度 : %s 度" %field1)

@app.route('/show', methods=['POST'])
def show():
    return_json = {
        "message": f"{request.form['username']}"
    }
    return jsonify(values=json.dumps(return_json))

if __name__ == '__main__':
	app.debug = True
	app.run(host='localhost') 

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

import MySQLdb

con = MySQLdb.connect(
    host = "localhost",
    user = "root",
    passwd = "1031hosei",
    db = "user"
)
cur = con.cursor()

cur.execute("""
            CREATE TABLE user.list
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            name VARCHAR(30),
            password VARCHAR(30),
            adress VARCHAR(100),
            PRIMARY KEY(id))
            """)

con.commit()

con.close()