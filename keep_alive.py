from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def run():
    app.run(host='0.0.0.0', port=10000, debug=False)


def keep_alive():
    t = Thread(target=run)
    t.start()
