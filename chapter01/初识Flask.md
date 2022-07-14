# 第一章 初识Flask

## 1. Flask有哪些主要的依赖？
1. Werkzeug(http://werkzeug.pocoo.org/)：WSGI（Web Server Gateway Interface）工具集，WSGI是Python中用来规定Web服务器如何与PythonWeb程序进行沟通的标准；
2. Jinja2(http://jinja.pocoo.org/)模板引擎.

---

## 2. 本章使用的Python包：
1. Flask
2. pip
3. Pipenv：基于pip的python包管理器，是pip、Pipfile和Virtualenv的结合体；
4. Virtualenv
5. Pipfile(https://github.com/pypa/pipfile): 用来替代难于管理的requirements.txt文件, 管理依赖
6. python-dotenv(https://github.com/theskumar/python-dotenv)：提供配置和管理环境变量的工具
7. watchdog(https://pythonhosted.org/watchdog/): 用于监测文件变动，可用于Flask文件调试时的reload

---

## 3. 如何搭建开发环境？
1. 安装Pipenv： `pip install pipenv`
2. 创建虚拟环境：
   1. 在打算创建虚拟环境的目录下执行`pipenv install`创建虚拟环境。创建的python解释器会放在`C:\Users\<User-name>\.virtualenvs\`目录下， 如果你想在项目目录内创建虚拟环境文件夹，可以设置环境变量`PIPENV_VENV_IN_PROJECT`，这时名为.venv的虚拟环境文件夹将在项目根目录被创建。
     当前目录下会出现两个文件Pipfile和Pipfile.lock用于管理python依赖：
      * `Pipfile`：用来记录项目的依赖包列表；
      * `Pipfile.lock`：用来记录固定版本的详细依赖包列表。
   1. 激活虚拟环境：`pipenv shell`，激活后linux系统会在命令行前显示环境名称，但是windows系统不显示。
   2. 退出虚拟环境：`exit`。
   3. 直接使用当前环境运行Python文件：`pipenv run python hello.py`
   4. 查看当前环境的依赖：`pipenv graph`或`pip list`。
   5. 查看当前虚拟环境路径：`pipenv --venv`.
3. 安装Flask：
   在目标目录下执行`pipenv install flask`，安装Flask到当前虚拟环境中（可以不用激活环境）。

   Flask会同时安装5个依赖包：
   * Jinja2：模板渲染引擎；
   * MarkupSafe：HTML字符转义（escape）工具；
   * Werkzeug：WSGI工具集，处理请求与响应、内置WSGI开发服务器、调试器和重载器；
   * click：命令行工具；
   * itsdangerous：提供各种加密签名功能。
  
---

## 4. Web应用中，客户端和服务器上的Flask程序的交互步骤有哪些？

1. 用户在浏览器输入URL访问某个资源；
2. Flask接收用户请求并分析请求的URl；
3. 为这个URL找到对应的处理函数；
4. 执行函数并生成响应，返回给浏览器；
5. 浏览器接收并解析响应，将信息显示在页面中。

---

## 5. 最简单的Flask应用包括那些部分？
1. 服务类示例`app=Flask(__name__)`: Flask类是Flask的核心类，提供很多与程序相关的属性和方法。
   
   其构造函数的第一个参数是模块或包的名称，这里使用特殊变量`__name__`，即当前文件的名称。
2. URL路由规则`app.route(URL规则)`: 该装饰器接收URl规则（不是URL），注册路由，进行URL和函数之间的映射。
   
   URL规则为字符串，**必须以斜杠开始**。输入的URL为相对URL，不包括域名。
3. 视图函数 `def index()`: 处理对应URL的请求并返结果.

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
```
---

## 6. URL规则有哪几种设置方法？

1. 一对一绑定：一个URL规则对应一个视图函数；
2. 多对一绑定：多个不同的URl对应同一个视图函数；
3. 动态URL：URL中含有变量参数，使用`<变量名>`的形式表示。Flask会将变量传入视图函数，要在视图函数中添加变量接收。
   可以使用 defaults参数设置URL变量的默认值，该参数接收字典为输入。
```python
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
```

---

## 7. 如何启动Flask应用？
Flask内置了一个简单的开发服务器（有Werkzeug提供），足够在开发和测试阶段使用。但不满足生产环境需要。

Flask通过Click内置了一个命令行交互界面CLI（command line interface）系统。安装Flask后，会自动添加一个flask命令脚本，我们可以通过flask命令执行内置命令、扩展提供的命令或是我们自己定义的命令。

激活虚拟环境后，**进入程序文件所在目录**，使用`flask run` 命令用来启动内置的开发服务器。
如未激活环境则可以使用`pipenv run flask run`命令。

启动后默认监听(http://127.0.0.1:5000)地址。，并开启多线程支持。

---

## 8. Flask自动探测程序实例的规则是什么？
使用Flask run 命令启动程序是，我们需要提供程序示例所在的模块地址，如果在程序事例的目录下，可以直接自动探测程序示例。

Flask的自动探测规则为：
1. 从当前目录寻找`app.py`和`wsgi.py`模块，并从中寻找名为`app`或`application`的程序示例；
2. 从环境变量`FLASK_APP`对应的值寻找名为`app`或`application`的程序示例；
   
   **NOTE:**
   如果你的程序名称不是app.py，则需要设置`FLASK_APP`变量，如hello.py需要设置为`export FLASK_APP=hello`(linux)或`set FLASK_APP=hello`(windows)。
3. 如果安装了python-dotenv，那么在使用flask run或其他命令时会使用它自动从`.flaskenv`文件和`.env`文件中加载环境变量。
   
   当安装了python-dotenv时(`pipenv install python-dotenv`)，Flask在加载环境变量的优先级是：

   > 手动设置的环境变量>.env中设置的环境变量>.flaskenv设置的环境变量。

---

## 9. 如何使用python-dotenv为Flask配置环境变量？
因为系统环境变量在每次新开终端或重启后就会清除，多以建议使用python-dotenv进行配置。

在项目的根目录下新建两个文件：
* `.flaskenv`：用来存储和Flask相关的公开的环境变量，如FLAKS_APP等；
* `.env`：用来存储包含敏感信息的环境变量，如用户名、密码等。(**注意不要提交到公共仓库中，写入.gitignore中**)

文件中使用键值对形式存储变量，# 开头的行为注释：
```
FLASK_APP=hello
# 这是注释
FOO="BAR"
```

程序中使用时，可使用os模块的`os.getenv(varname, default)`方法获取环境变量值。

---

## 10. Flask run 命令常用的启动选项有哪些？
* --host=0.0.0.0, 监听所有外部请求。 内网穿透工具：[ngrok](https://ngrok.com/ ), [Localtunnel](https://localtunnel.github.io/www/ )
* --port=8080, 改变监听端口
* --with-threads/--ithout-threads, 是否打开多线程
* 等

各种参数还可以通过环境变量来设置：`FLASK_RUN_HOST`和`FLASK_RUN_PORT`，环境变量的通用格式为`FALSK_<COMMAND>_<OPTION>`.

---

## 11. 如何设置运行时环境？
Flask根据运行时环境的不同，其扩展及其他程序会有相应的行为和设置。
Flask通过`FLASK_ENV`环境变量来设置环境，默认为生产环境`production`, 可以在`.flaskenv`文件中将其设置为开发环境`development`。

然后启动程序，则会看到如下输出：
```
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 199-196-057
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
---

## 12. 开发环境的特点是什么？
Flask在开发环境下会默认开启调试器 debugger 和重载器 reloader。

可以单独通过`FALSK_DEBUG=0/1`环境变量来关闭调试模式。

**注意**：生产环境中绝对不能开启调试模式。

* 调试器：在网页上显示错误追踪信息，以及进行在线调试等，调试时需要使用启动时显示的PIN码。
* 重载器：当代码修改后，重载器监测到文件变动，然后重新启动服务器，使修改及时生效。
  
  Werkzeug默认提供的stat重载器性能一般，我们需要安装使用 `watchdog` 库来监测文件变动：`pipenv install watchdog --dev`, 因为这个包只在开发时才会用到，所以我们在安装命令后添加了一个`--dev`选项，这用来把这个包声明为开发依赖。在Pipfile文件中，这个包会被添加到dev-packages部分。

  **注意**：如果项目中使用了单独的CSS或JavaScript文件时，那么浏览器可能会缓存这些文件，从而导致对文件做出的修改不能立刻生效。在浏览器中，我们可以按下`Crtl+F5`或`Shift+F5`执行硬重载（hard reload），即忽略缓存并重载（刷新）页面。

---

## 13. Flask中的上下文指什么？

上下文（context）是为了程序正常运行，被临时保存下来的相关状态和数据。可分为**程序上下文**和**请求上下文**。

使用`flask shell`可以进入python交互模式并激活程序上下文，此时，会自动导入当前程序实例中的app示例。

---

## 14. Flask扩展是什么？

扩展（extension）是使用Flask提供的API接口编写的python库，可以为Flask程序提供各种功能，主要用来集成其他库。

其使用初始化过程大致为：实例化扩展类，实例化时要传入我们创建的程序事例app作为参数。扩展会在传入过程中注册一些处理函数，并加载一些配置。

---

## 15. Flask的配置项有哪几类？

1. Flask提供的配置(https://flask.palletsprojects.com/en/2.0.x/config/)；
2. 扩展提供的配置, 查看扩展相关文档；
3. 程序自己特定的配置。

---

## 16. 如何设置和读取配置变量的值？

配置变量的名称必须是全大写的形式，小写的变量将不会被读取。

配置变量通过Flask对象的`app.config`属性作为统一接口来获取和设置。Config类继承自字典类，可以像操作字典一样操作配置。

此外还可以将配置写入python文件、JSON文件或Python类中，然后导入配置。

1. 设置：
   ```python
   app.config['ADMIN_NAME'] = 'Peter'

   app.config.update(
      TESTING=True,
      SECRET_KEY='_5#yF4Q8z\n\xec]/'
   )
   ```
2. 读取：
   ```python
   value = app.config['ADMIN_NAME']
   ```
---

## 17. Flask中的端点是什么？

在Flask中，端点（endpoint）用来标记一个视图函数以及对应的URL规则。端点的默认值为视图函数的名称。在使用`app.route()`装饰器时可以使用`endpoint`参数自定义端点。

如果程序中想要获取某个URL，可以使用`url_for()`方法进行获取。其第一个参数就是端点值。如果URL规则中含有动态参数，则也要传入相应的参数。

```python
@app.route('/')
def index():
    return 'Hello Flask!'

url_for('index')  # = '/'

@app.route('/hello/<name>')
def greet(name):
    return 'Hello %s!' % name

url_for('greet', name='Jack')  # = '/hello/Jack'
```
url_for() 方法生成的URL是相对URL，如果想获得绝对URL则需要 `_external=True` 参数。

---

## 18. 如何自定义Flask命令？

创建任意一个方法，并为其添加`app.cli.command()`装饰器，就可以注册一个Flask命令。默认函数的名称即为注册的命令，也可以通过装饰器的参数来指定。

```python
@app.cli.command()
def hello():
    """flask hello help info."""
    click.echo('Hello, Human!')
```
通过`flask hello`可以触发该方法，方法的注释文档会变为其帮助信息`flask hello --help`。

有关自定义命令的更多帮助，可参考(https://click.palletsprojects.com/en/6.x/).

---

## 19. 模板和静态文件应如何设置？
* 模板（template）：包含程序页面的HTML文件，一般保存在`template`文件夹中。
* 静态文件（static file）：需要放在HTML文件中加载的CSS和JavaScript文件，以及图片、字体文件等资源文件。一般保存在`static`文件夹中。
* `template` 和 `static` 文件夹需要和程序示例的模块处于同一目录下:
```
hello/
    - templates/
    - static/
    - app.py
```

* 建议在开发环境下使用本地资源，这样可以提高加载速度。下载到static目录下，统一管理，出于方便的考虑也可以使用扩展内置的本地资源。
* 在过渡到生产环境时，自己手动管理所有本地资源或自己设置CDN，避免使用扩展内置的资源。
  
  因为：

  ·鉴于国内的网络状况，扩展默认使用的国外CDN可能会无法访问，或访问过慢。
  
  ·不同扩展内置的加载方法可能会加载重复的依赖资源，比如jQuery。

  ·在生产环境下，将静态文件集中在一起更方便管理。

  ·扩展内置的资源可能会出现版本过旧的情况。

---

## 20. CDN是什么？

CDN指分布式服务器系统。服务商把你需要的资源存储在分布于不同地理位置的多个服务器，它会根据用户的地理位置来就近分配服务器提供服务（服务器越近，资源传送就越快）。使用CDN服务可以加快网页资源的加载速度，从而优化用户体验。对于开源的CSS和JavaScript库，CDN提供商通常会免费提供服务。

---

## 21. MVC架构有哪几部分构成？
MVC（Model-View-Controller, 模型-视图-控制器）架构可以分为三部分：
* 数据处理Model
* 用户界面View
* 交互逻辑Controller

严格来说，Flask并不是MVC架构的框架，因为他没有内置数据模型的支持。如果想要使用Flask来编写一个MVC架构的程序，那么视图函数可以作为控制器（Controller），视图（View）则使用Jinja2渲染的HTML模板，而模型（Model）可以使用其他库来实现，如使用SQLAlchemy来创建数据库模型。