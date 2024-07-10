from flask import Flask
import webbrowser
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
