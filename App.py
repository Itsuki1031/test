from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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
    session.clear()
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
            return render_template("login.html", msg="IDが間違っています", br="<br>")
        if cph(data[0][0], passwd):
            session["name"] = data[0][1]
            session["email"] = data[0][2]
            session["tel"] = data[0][3]
            session["admin"] = 0 if data[0][4] is None else data[0][4]
            con.close()
            return redirect("home2")
        else:
            con.close()
            return render_template("login.html", msg="パスワードが間違っています", br="<br>")
        
@app.route("/home")
def home():
    if "name" in session:
        return render_template("success.html",
                                name=html.escape(session["name"]),
                                email=html.escape(session["email"]),
                                tel=html.escape(session["tel"]))
    else:
        return redirect("login")

@app.route("/home2")
def home2():
    if "name" in session:
        if session["admin"] == 1:
            return render_template("open.html",
                                    name=html.escape(session["name"]),
                                    test2="<test2>",
                                    input="データの入力",
                                    admin = "<a href=\"admin\">ユーザ情報一覧</a>")
        else:
            return render_template("open.html",name=html.escape(session["name"]))
    else:
        return redirect("login")
    
#@app.route("/home3")
#def home3():
#    if "name" in session:
#        con = connect()
#        cur = con.cursor()
#        cur.execute("""
#                    SELECT shop_name
#                    FROM shop
#                    """)
#        data=[]
#        for row in cur:
#               data.append(row[0])
#
#        return render_template("select.html", data = data)
#    else:
#        return redirect("login")

@app.route("/select", methods=["GET", "POST"])
def select():
    if "name" in session:
        if request.method == "GET":
            return render_template("select.html")
        elif request.method == "POST":
            shop_id = request.form.get("shop_id")
            shelf_id = request.form.get("shelf_id")
            tem_date = request.form.get("tem_date")
            item_name = request.form.get("item")
            if shop_id != None and shelf_id != None and tem_date != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time 
                            FROM temperature
                            WHERE shop_id=%(shop_id)s
                            AND shelf_id=%(shelf_id)s
                            AND tem_date=%(tem_date)s
                            """,{"shop_id":shop_id, "shelf_id":shelf_id, "tem_date":tem_date})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)
            elif shop_id != None and shelf_id:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time 
                            FROM temperature
                            WHERE shop_id=%(shop_id)s
                            AND shelf_id=%(shelf_id)s
                            """,{"shop_id":shop_id, "shelf_id":shelf_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)    
            elif shop_id != None and tem_date:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time 
                            FROM temperature
                            WHERE shop_id=%(shop_id)s
                            AND tem_date=%(tem_date)s
                            """,{"shop_id":shop_id, "tem_date":tem_date})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)    
            elif shop_id != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time 
                            FROM temperature
                            WHERE shop_id=%(shop_id)s
                            """,{"shop_id":shop_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>検索したSHOP_IDの店は存在しません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)
            elif shelf_id != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time
                            FROM temperature
                            WHERE shelf_id=%(shelf_id)s
                            """,{"shelf_id":shelf_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>検索したSHELF_IDの棚は存在しません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)
            elif tem_date != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            reference_temperature, temperature, tem_date, tem_time
                            FROM temperature
                            WHERE tem_date=%(tem_date)s
                            """,{"tem_date":tem_date})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
                if len(data)==0:
                    con.close()
                    return render_template("result.html", msg="<br><br>検索した日付は存在しません")
                else:
                    return render_template("result.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "基準温度",
                                            arti4 = "温度",
                                            arti5 = "計測日時",
                                            arti6 = "計測時間",
                                            data = data)        
            elif item_name != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, item_name
                            FROM item
                            WHERE item_name=%(item_name)s
                            """,{"item_name":item_name})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2]])
                if len(data)==0:
                    con.close()
                    return render_template("result2.html", msg="<br><br>検索した商品は存在しません")
                else:
                    return render_template("result2.html", 
                                            msg2="<br><br><b>検索していただいた商品名のSHOP_ID, SHELF_idは下記のようになっています",
                                            msg3="こちらをご確認いただき先ほどのページにて店名か棚の番号で検索してください<b><br>",
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            select = "select",
                                            data = data)
    else:
        return redirect("login")

@app.route("/select2", methods=["GET", "POST"])
def select2():
    if "name" in session:
        if request.method == "GET":
            return render_template("select2.html")
        elif request.method == "POST":
            shop_id = request.form.get("shop_id")
            shelf_id = request.form.get("shelf_id")
            item_name = request.form.get("item_name")
            sales_co = request.form.get("sales_co")
            if shop_id != None and shelf_id != None and item_name != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            AND shelf_id=%(shelf_id)s
                            AND item_name=%(item_name)s
                            """,{"shop_id":shop_id, "shelf_id":shelf_id, "item_name":item_name})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)
            elif shop_id != None and shelf_id != None and sales_co != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            AND shelf_id=%(shelf_id)s
                            AND sales_co=%(sales_co)s
                            """,{"shop_id":shop_id, "shelf_id":shelf_id, "sales_co":sales_co})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)    
            elif shop_id != None and shelf_id:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            AND shelf_id=%(shelf_id)s
                            """,{"shop_id":shop_id, "shelf_id":shelf_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)    
            elif shop_id != None and item_name:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            AND item_name=%(item_name)s
                            """,{"shop_id":shop_id, "item_name":item_name})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)
            elif shop_id != None and sales_co:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            AND sales_co=%(sales_co)s
                            """,{"shop_id":shop_id, "sales_co":sales_co})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>該当する検索結果はありません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)    
            elif shop_id != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shop_id=%(shop_id)s
                            """,{"shop_id":shop_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>検索したSHOP_IDの店は存在しません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)
            elif shelf_id != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE shelf_id=%(shelf_id)s
                            """,{"shelf_id":shelf_id})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>検索したSHELF_IDの棚は存在しません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)        
            elif item_name != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE item_name=%(item_name)s
                            """,{"item_name":item_name})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>検索した商品は存在しません")
                else:
                    return render_template("result3.html", 
                                            msg2="<b>検索していただいた商品名のSHOP_ID, SHELF_idは下記のようになっています",
                                            msg3="こちらをご確認いただき先ほどのページにて店名か棚の番号で検索してください<b><br>",
                                            msg4="<a href=\"select2\">戻る</a>",
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            data = data)
            elif sales_co != None:
                con = connect()
                cur = con.cursor()
                cur.execute("""
                            SELECT shop_id, shelf_id, 
                            item_name, sales_co, price 
                            FROM item
                            WHERE sales_co=%(sales_co)s
                            """,{"sales_co":sales_co})
                data=[]
                for row in cur:
                    data.append([row[0],row[1],row[2],row[3],row[4]])
                if len(data)==0:
                    con.close()
                    return render_template("result3.html", msg="<br><br>検索した販売会社は存在しません")
                else:
                    return render_template("result3.html", 
                                            table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                            arti = "SHOP_id",
                                            arti2 = "SHELF_id",
                                            arti3 = "商品名",
                                            arti4 = "販売会社名",
                                            arti5 = "値段",
                                            data = data)                                
    else:
        return redirect("login")    

@app.route("/home3")
def home3():
    if "name" in session:
        if session["admin"] == 1:
            return render_template("select_input.html",
                                    name = html.escape(session["name"]),
                                    mi="データの閲覧",
                                    url = "select",
                                    url2 = "select2",
                                    tem = "温度情報閲覧",
                                    item = "商品情報閲覧",
                                    admin = "<a href=\"admin\">ユーザ情報一覧</a>",
                                    br = "<br>"
                                    )
        else:
            return render_template("select_input.html",
                                    name = html.escape(session["name"]),
                                    mi="データの閲覧",
                                    url = "select",
                                    url2 = "select2",
                                    tem = "温度情報閲覧",
                                    item = "商品情報閲覧",
                                    )
    else:
        return redirect("login")

@app.route("/home4")
def home4():
    if "name" in session:
        return render_template("select_input.html",
                                name = html.escape(session["name"]),
                                mi="データの入力",
                                url = "input",
                                url2 = "input_item",
                                tem = "温度情報入力",
                                item = "商品情報入力",
                                admin = "<a href=\"admin\">ユーザ情報一覧</a>",
                                br = "<br>"
                                )
    else:
        return redirect("login")
        
@app.route("/home5")
def home5():
    if "name" in session:
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT shop_id, shop_name, shop_adress
                    FROM shop
                    """)
        data=[]
        for row in cur:
               data.append([row[0],row[1],row[2]])
        return render_template("result2.html",
                                table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                arti = "SHOP_ID",
                                arti2 = "SHOP_NAME",
                                arti3 = "SHOP_ADRESS",
                                select = "select",
                                data = data)
    else:
        return redirect("login")
    
@app.route("/home6")
def home6():
    if "name" in session:
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT shop_id, shelf_id, 
                    reference_temperature, temperature, tem_date, tem_time
                    FROM temperature
                    """)
        data=[]
        for row in cur:
               data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
        return render_template("result.html", 
                                table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                arti = "SHOP_id",
                                arti2 = "SHELF_id",
                                arti3 = "基準温度",
                                arti4 = "温度",
                                arti5 = "計測日時",
                                arti6 = "計測時間",
                                data = data)
    else:
        return redirect("login")

@app.route("/home7")
def home7():
    if "name" in session:
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT shop_id, shelf_id, 
                    item_name, sales_co, price 
                    FROM item
                    """)
        data=[]
        for row in cur:
               data.append([row[0],row[1],row[2],row[3],row[4]])
        return render_template("result3.html", 
                                table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                arti = "SHOP_id",
                                arti2 = "SHELF_id",
                                arti3 = "商品名",
                                arti4 = "販売会社名",
                                arti5 = "値段",
                                data = data)
    else:
        return redirect("login")

@app.route("/home8")
def home8():
    if "name" in session:
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT shop_id, shop_name, shop_adress
                    FROM shop
                    """)
        data=[]
        for row in cur:
               data.append([row[0],row[1],row[2]])
        return render_template("result2.html",
                                table = "<table border=\"1\" align=\"center\" class=\"design10\">",
                                arti = "SHOP_ID",
                                arti2 = "SHOP_NAME",
                                arti3 = "SHOP_ADRESS",
                                select = "select2",
                                data = data)
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
                    """,{"email":email, "hashpass":hashpass, "tel":tel, "name":name}
                    )
        con.commit()
        con.close()
        return render_template("info.html", email=email, passwd=passwd, name=name, tel=tel)

@app.route("/input", methods=["GET", "POST"])
def input():
    if "name" in session:
        if request.method == "GET":
            return render_template("input.html",
                                    name=html.escape(session["name"]),
                                    admin = "<a href=\"admin\">ユーザ情報一覧</a>",
                                    br = "<br>")
        elif request.method == "POST":
            shop_id = request.form["shop_id"]
            shelf_id = request.form["shelf_id"]
            reference_temperature = request.form["reference_temperature"]
            temperature = request.form["temperature"]
            tem_date = request.form["tem_date"]
            tem_time = request.form["tem_time"]
            con = connect()
            cur =con.cursor()
            cur.execute("""
                        INSERT INTO user.temperature
                        (shelf_id,shop_id,reference_temperature,temperature,tem_date,tem_time)
                        VALUES (%(shelf_id)s,%(shop_id)s,%(reference_temperature)s,%(temperature)s,%(tem_date)s,%(tem_time)s)
                        """,{"shelf_id":shelf_id,"shop_id":shop_id, "reference_temperature":reference_temperature, "temperature":temperature, "tem_date":tem_date, "tem_time":tem_time}
                        )
            con.commit()
            con.close()
            return render_template("shelf_info.html", shelf_id=shelf_id, shop_id=shop_id, reference_temperature=reference_temperature, temperature=temperature, tem_date=tem_date, tem_time=tem_time)
    else:
        return redirect("login")
    
@app.route("/input_item", methods=["GET", "POST"])
def input_item():
    if "name" in session:
        if request.method == "GET":
            return render_template("input_item.html",
                                    name=html.escape(session["name"]),
                                    admin = "<a href=\"admin\">ユーザ情報一覧</a>",
                                    br = "<br>")
        elif request.method == "POST":
            shop_id = request.form["shop_id"]
            shelf_id = request.form["shelf_id"]
            item_name = request.form["item_name"]
            sales_co = request.form["sales_co"]
            price = request.form["price"]
            con = connect()
            cur =con.cursor()
            cur.execute("""
                        INSERT INTO user.item
                        (shelf_id,shop_id,item_name,sales_co,price)
                        VALUES (%(shelf_id)s,%(shop_id)s,%(item_name)s,%(sales_co)s,%(price)s)
                        """,{"shelf_id":shelf_id,"shop_id":shop_id, "item_name":item_name, "sales_co":sales_co, "price":price}
                        )
            con.commit()
            con.close()
            return render_template("item_info.html", shelf_id=shelf_id, shop_id=shop_id, item_name=item_name, sales_co=sales_co, price=price)
    else:
        return redirect("login")

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
            res = res + "<a href=\"home2\">戻る</a>\n"
            for row in cur:
                res = res + "<table border=\"1\" align=\"center\">\n"
                res = res + "\t<tr><td align=\"right\">名前</td><td>" + html.escape(row[0]) + "</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">メールアドレス</td><td>" + html.escape(row[1]) + "</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">電話番号</td><td>" + html.escape(row[2]) + "</td></tr>\n"
                res = res + "</table>"
                res = res + "<br>"
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

@app.route('/open')
def open():
    return render_template('open.html')

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

#con = MySQLdb.connect(
#    host = "localhost",
#    user = "root",
#    passwd = "1031hosei",
#    db = "user"
#)

con = connect()

cur = con.cursor()

#cur.execute("""
#            CREATE TABLE user.data
#            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
#            email VARCHAR(100),
#            passwd VARCHAR(200),
#            name VARCHAR(30),
#            tel VARCHAR(30),
#            PRIMARY KEY(id))
#            """)

#cur.execute("""
#            CREATE TABLE user.shop
#            (shop_id MEDIUMINT NOT NULL AUTO_INCREMENT,
#            id MEDIUMINT NOT NULL,
#            shop_name VARCHAR(30),
#            shop_adress VARCHAR(200),
#            PRIMARY KEY(shop_id),
#            FOREIGN KEY(id) REFERENCES user.data(id))
#            """)

#cur.execute("""
#            DROP TABLE user.temperature
#            """)

#cur.execute("""
#            INSERT INTO user.shelf
#            (shelf_id)
#            VALUES(9)           
#            """)

#cur.execute("""
#            CREATE TABLE user.temperature
#            (temperature_id MEDIUMINT NOT NULL AUTO_INCREMENT,
#            shop_id MEDIUMINT NOT NULL,
#            shelf_id INTEGER NOT NULL,
#            reference_temperature INTEGER,
#            temperature INTEGER,
#            temperature_at DATETIME,
#            PRIMARY KEY(temperature_id),
#            FOREIGN KEY(shelf_id) REFERENCES user.shelf(shelf_id),
#            FOREIGN KEY(shop_id) REFERENCES user.shop(shop_id))
#            """)

#cur.execute("""
#            ALTER TABLE user.temperature auto_increment = 1;
#            """)

con.commit()

con.close()