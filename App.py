from flask import Flask, render_template, request, jsonify, session, redirect
import json
import datetime
import calendar
import MySQLdb
import html
import secrets
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta

dt_now = datetime.datetime.now()
weekday = datetime.date.today().weekday()
weekday_name = calendar.day_name[weekday]

def connect():
    con = MySQLdb.connect(
        host = "localhost",
        user = "root",
        passwd = "1031hosei",
        db = "user"
    )
    return con

def ChangeMonth(month):
    date = datetime.date(dt_now.year, month, dt_now.day)
    return date.strftime("%B")

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                      SELECT passwd,name,email,tel,admin
                      FROM data
                      WHERE email=%(email)s
                      """,{"email":email})
        data=[]
        for row in cur:
            data.append([row[0],row[1],row[2],row[3],row[4]])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="IDが間違っています")
        if cph(data[0][0], passwd):
            session["name"] = data[0][1]
            session["email"] = data[0][2]
            session["tel"] = data[0][3]
            session["admin"] = 0 if data[0][4] is None else data[0][4]
            con.close()
            return redirect("home")
        else:
            con.close()
            return render_template("login.html", msg="パスワードが間違っています")
        
@app.route("/home")
def home():
    if "name" in session:
        if session["admin"] == 1:
            return render_template("success.html",
                                    name=html.escape(session["name"]),
                                    email=html.escape(session["email"]),
                                    tel=html.escape(session["tel"]),
                                    admin="<a href=\"admin\">ユーザ情報一覧</a>")
        else:
            return render_template("success.html",
                                    name=html.escape(session["name"]),
                                    email=html.escape(session["email"]),
                                    tel=html.escape(session["tel"]))
    else:
        return redirect("login")

@app.route("/make", methods=["GET", "POST"])
def make():
    if request.method == "GET": 
        return render_template("make.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        name = request.form["name"]
        tel = request.form["tel"]
        hashpass = gph(passwd)
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM data WHERE email=%(email)s
                    """,{"email":email})
        data=[]
        for row in cur:
            data.append(row)
        if len(data)!=0:
            return render_template("make.html", msg="既に存在するメールアドレスです")
        con.commit()
        con.close()
        con = connect()
        cur =con.cursor()
        cur.execute("""
                    INSERT INTO user.data
                    (email,passwd,tel,name)
                    VALUES (%(email)s,%(hashpass)s,%(tel)s,%(name)s)
                    """,{"email":email, "hashpass":hashpass, "tel":tel, "name":name})
        con.commit()
        con.close()
        return render_template("info.html", email=email, passwd=passwd, name=name, tel=tel)
    
@app.route("/admin")
def admin():
    if "admin" in session:
        if session["admin"] == 1:
            con = connect()
            cur = con.cursor()
            cur.execute("""
                        SELECT name,email,tel
                        FROM data
                        """)
            res=""
            for row in cur:
                res = res + "<table border=\"1\" align=\"center\">\n"
                res = res + "\t<tr><td align=\"right\">名前</td><td>" + html.escape(row[0]) + "</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">メールアドレス</td><td>" + html.escape(row[1]) + "</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">電話番号</td><td>" + html.escape(row[2]) + "</td></tr>\n"
                res = res + "</table>"
            con.close()
            return res
        else:
            return redirect("home")
    else:
        return redirect("login")

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

@app.route('/api/time')
def jikan():
    jikan = {
        '1.year':dt_now.year,
        '2.month':dt_now.month,
        '3.month_name':ChangeMonth(dt_now.month),
        '4.day':dt_now.day,
        '5.weekday':weekday_name,
        '6.hour':dt_now.hour,
        '7.minute':dt_now.minute,
        '8.second':dt_now.second,
        '9.now':dt_now.isoformat()
    }
    return jsonify(jikan)

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

con = MySQLdb.connect(
    host = "localhost",
    user = "root",
    passwd = "1031hosei",
    db = "user"
)
cur = con.cursor()

cur.execute("""
            CREATE TABLE user.data
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            email VARCHAR(100),
            passwd VARCHAR(200),
            name VARCHAR(30),
            tel VARCHAR(30),
            PRIMARY KEY(id))
            """)

con.commit()

con.close()