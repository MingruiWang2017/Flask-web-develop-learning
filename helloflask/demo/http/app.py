import os
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urljoin, urlparse

from markupsafe import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, request, redirect, make_response, url_for, abort, session, jsonify

app = Flask(__name__)
# 通过环境变量加载session使用的密钥
app.secret_key = os.getenv('SECRET_KEY', 'secret sting')


# 从查询参数和cookie中获取用户名
@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')  # 获取查询参数name的值
    if not name:
        name = request.cookies.get('name', 'Human')

    response = '<h1>Hello, %s!</h1>' % escape(name)  # 使用escape转义用户输入，防止XSS攻击

    # 根据用户的不同登录状态返回不同响应
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

# 重定向
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# 使用URL转换器
@app.route('/goback/<int:year>')  # 使用转换器将year转换为int类型
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2022 - year)


@app.route('/colors/<any(blue, black, white, red, green):color>')  # 使用any转换器，接收的参数只能是指定的几个值
def colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# 通过预定义的列表传输数据
colors = ['blue', 'white', 'red']

@app.route('/colors/<any(%s):color>' % str(colors)[1:-1])
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'

# 返回错误响应
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'

# 404
@app.route('/404')
def not_found():
    abort(404)  # 使用abort主动返回错误


###### 使用不同文档格式返回内容##########
# 1. HTML
@app.route('/note', defaults={'content_type': 'text'})
@app.route('/note/<content_type>')
def note(content_type: str):
    content_type = content_type.lower()

    if content_type == 'text':  # 纯文本格式
        body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
        response = make_response(body)
        response.mimetype = 'text/plain'

    elif content_type == 'html':  # HTML格式
        body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
        response = make_response(body)
        response.mimetype = 'text/html'

    elif content_type == 'xml':  # xml格式
        body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
        response = make_response(body)
        response.mimetype = 'application/xml'

    elif content_type == 'json':  # json格式
        body = {"note": {
            "to": "Peter",
            "from": "Jane",
            "heading": "Remider",
            "body": "Don't forget the party!"
        }
        }
        response = jsonify(body)
        # equal to:
        # response = make_response(json.dumps(body))
        # response.mimetype = "application/json"

    else:
        abort(400)
    return response


# 设置name cookie项
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# 模拟用户登录
@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))

# 判断用户是否登录，能否访问管理员视图
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


# 退出登录
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# AJAX, 使用异步请求加载长文章
@app.route('/ajax')
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(2)

    return '''
<h1>A very long post</h1>
<div class='body'>%s</div>
<button id='load'>Load More</button>
<script src='https://code.jquery.com/jquery-3.3.1.min.js'></script>
<script type='text/javascript'>
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(2)


# 重定向到上一个页面
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)  # 在url后面添加next参数，参数值为当前页面url


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)

@app.route('/do-something')
def do_something():
    return redirect_back()


# 判断跳转的url是否安全
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


# 从request的参数中获取next或referrer，跳转回上一页面，如果为空则返回首页
def redirect_back(default='hello', **kwargs):
    for target in request.referrer, request.args.get('next'):
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
