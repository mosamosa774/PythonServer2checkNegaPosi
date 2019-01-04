from flask import Flask, request, send_from_directory, Response  # Flaskパッケージを要インポート
import os.path
import checkNP as np
import json

noun, verb = np.init()

app = Flask(__name__, static_url_path='/dist/')  # Flaskクラスのインスタンス生成


def root_dir():  # pragma: no cover
    print(os.path.dirname(__file__))
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        print(root_dir()+'/dist')
        src = os.path.join(root_dir()+'/dist', filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/api', methods=['POST'])  # URL指定。URLにリクエストが来ると関数内が実行される。
def api():
    data = request.data.decode('utf-8')
    d = json.loads(data)
    return np.analyze(noun, verb, d['contents'], int(d['flag']), int(d['flag2']))


@app.route('/oneline', methods=['POST'])  # URL指定。URLにリクエストが来ると関数内が実行される。
def oneline():
    data = request.data.decode('utf-8')
    return data.replace('\n', '\\n')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('dist\\js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('dist\\css', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('dist\\img', path)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
