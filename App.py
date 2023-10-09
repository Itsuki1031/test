from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html', title="あなたは誰でしょうか",  message="ユーザー名をお願いします")

@app.route('/', methods=['POST'])
def  form():
	field = request.form['field']
	return render_template('index.html', title="名前を承りました",  message="こんにちは、%s さん！" %field)

@app.route('/sub', methods=['GET'])
def sub():
	return render_template('sub.html', title="ログイン画面",  message="温度管理アプリを始める前にパスワードを入れてください")

@app.route('/sub', methods=['POST'])
def  form2():
	field = request.form['field']
	return render_template('sub.html', title="ログイン画面",  message="アプリへようこそ")

@app.route('/sub')
def suburl():
    return render_template('sub.html')

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