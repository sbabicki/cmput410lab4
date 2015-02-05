from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello():
    return '<h1>Hello Flask!</h1>'

@app.route('/second')
@app.route('/second/<name>')
def hello2(name = 'FLASK'):
    return '<h1>Hello %s (second test)!</h1>' %name

if __name__ == '__main__':
    app.debug = True
    app.run()