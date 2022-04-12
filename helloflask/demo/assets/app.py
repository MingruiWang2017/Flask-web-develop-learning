import os

from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev key')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

assets = Environment(app)
ckeditor = CKEditor(app)

css_pack = Bundle('css/bootstrap.min.css',
                  'css/bootstrap.css',
                  'css/dropzone.min.css',
                  'css/jquery.Jcrop.min.css',
                  'css/style.css',
                  filters='cssmin', output='gen/packed.css')

js_pack = Bundle('js/jquery.min.js',
                 'js/popper.min.js',
                 'js/bootstrap.min.js',
                 'js/bootstrap.js',
                 'js/moment-with-locales.min.js',
                 'js/dropzone.min.js',
                 'js/jquery.Jcrop.min.js',
                 filters='jsmin', output='gen/packed.js')

assets.register('js_all', js_pack)
assets.register('css_all', css_pack)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/foo')
def unoptimized():
    """未经优化的页面"""
    return render_template('unoptimized.html')


@app.route('/bar')
def optimized():
    """经过优化的页面"""
    return render_template('optimized.html')

# run `flask assets build` before `flask run`
