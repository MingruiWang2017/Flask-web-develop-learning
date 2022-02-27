import os
from flask import Flask, render_template, flash, redirect, url_for, Markup, request
from markupsafe import escape

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')

# 开启jinja2空白控制
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# 模拟用户数据
user = {
    'username': 'Jack Chen',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


# 注册模板上下文处理器，用于渲染时提供全局变量
@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)


# 注册模板全局函数
@app.template_global()
def bar():
    return 'I an bar.'


# 注册过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# 注册测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False


@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html', user=user, movies=movies)


# 使用消息闪现
@app.route('/flash')
def just_flash():
    message = request.args.get('message', "I am flash, who is looking for me?")
    flash(escape(message))
    return redirect(url_for('index'))


# 自定义错误页面404和500
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
