import click
from flask import Flask

app = Flask(__name__)


# 一对一映射
@app.route('/')
def hello_world():
    return 'Hello World!'


# 多个url映射到同一视图函数
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello Flask</h1>'


# 动态URL
@app.route('/greet', defaults={'name', 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello %s!</h1>' % name

# 等同于
@app.route('/greet2')
@app.route('/greet2/<name>')
def greet2(name="Programmer"):
    return '<h1>Hello, %s!</h1>' % name


# 自定义Flask命令
@app.cli.command()
def hello():
    """flask hello help info."""
    click.echo('Hello, Human!')
