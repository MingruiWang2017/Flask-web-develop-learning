# logging 模块入门与进阶教程：https://docs.python.org/zh-cn/3/howto/logging.html

# 13.1. logging模块入门教程：

> 日志时对软件执行时所发生的事件的一种追踪方式，开发者对他们的代码添加日志调用，借此来指示某事件的发生。一个事件通过一些包含变量数据的相关信息来进行描述。每个时间可以指定不同的等级（level）或严重性（severity）。

日志的严重性（等级）如下，按顺序递增：
|      级别       | 何时使用                                                         |
| :-------------: | :--------------------------------------------------------------- |
|      DEBUG      | 细节信息，仅当诊断问题时适用                                     |
|      INFO       | 确认程序按预期执行                                               |
| WARNING（默认） | 表明有已经或即将发生的意外（如，磁盘空间不足）。程序仍按预期执行 |
|      ERROR      | 由于严重的问题，程序的某些功能已经不能正常执行                   |
|    CRITICAL     | 严重的错误，表明程序已不能继续执行                               |

默认的等级是`WARNING`，这意味着程序只会记录warning及其以上等级（error、critical）的日志信息，而不会记录debug和info。当然，等级是可以设置修改的。

---

## 1. 什么时候应该使用日志？使用何种日志记录方法？
  
  对于简单的日志使用来说日志功能提供了一系列便利的函数。它们是 `debug()，info()，warning()，error() 和 critical()`。
  
  想要决定何时使用日志，请看下表，其中显示了对于每个通用任务集合来说最好的工具。

  | 想要执行的任务                                                 | 此任务最好的工具                                                                                                                                                     |
  | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 对于命令行或程序的应用，结果显示在控制台                       | print()直接打印                                                                                                                                                      |
  | 在对程序的普通操作发生时提交事件报告(比如：状态监控和错误调查) | logging.info() 函数(当有诊断目的需要详细输出信息时使用 logging.debug() 函数)                                                                                         |
  | 提出一个警告信息基于一个特殊的运行时事件                       | warnings.warn() : 如果事件是可以避免的，那么客户端应用应该进行修改来消除告警；<br>logging.warning() 如果客户端应用对这种情况无法通过修改来避免，但是事件需要引起关注 |
  | 对一个特殊的运行时事件报告错误                                 | raise抛出异常                                                                                                                                                        |
  | 报告错误而不引发异常(如在长时间运行中的服务端进程的错误处理)   | logging.error(), logging.exception() 或 logging.critical() 分别适用于特定的错误及应用领域                                                                            |

---
 
## 2. logging模块的基本用法：如何输出到控制台和文件？
  
  * 直接输出到控制台，logging默认的行为就是将日志输出到 stdout和stderr：
    ```python
    import logging
    logging.warning('Watch out!')  # will print a message to the console
    logging.info('I told you so')  # will not print anything
    ```
  * 记录到日志：
    通过[logging.basicConfig()](https://docs.python.org/zh-cn/3/library/logging.html#logging.basicConfig)指定日志记录位置和相关参数。
    ```python
    import logging
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    ```
    python3.9版本增加了encoding参数，用来指定日志文件的编码格式。

---

## 3. 如何在日志中记录变量数据？
  
  要记录变量数据，可以使用格式化字符串作为时间描述信息，并附加传入变量数据做参数：
  ```python
  logging.warning('%s before you %s', 'Look', 'leap!')
  # WARNING:root:Look before you leap!
  ```

---

## 4. 如何更改显示消息的格式？
  
  ```python
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
  logging.debug('This message should appear on the console')
  logging.info('So should this')
  logging.warning('And this, too')
  # DEBUG:This message should appear on the console
  # INFO:So should this
  # WARNING:And this, too
  ```
---

## 5. 如何在日志中显示日期/时间？
  
  要显示日期和时间，可以在格式化字符串中使用`%(asctime)s`
  ```python
  import logging
  logging.basicConfig(format='%(asctime)s %(message)s')
  logging.warning('is when this event was logged.')
  # 2010-12-12 11:41:42,612 is when this event was logged.
  ```
  也可以自定义日期格式：
  ```python
  logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
  logging.warning('is when this event was logged.')
  # 12/12/2010 11:46:36 AM is when this event was logged.
  ```

  更多关于打印日志的格式问题，可以参考[Formater](https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter)的相关参数，他可以灵活地定义日志记录的格式。其中有关logging自带的某些属性可参考[LogRecord属性](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes)
  <details>
  <table class="docutils align-default">
  <colgroup>
  <col style="width: 18%">
  <col style="width: 28%">
  <col style="width: 53%">
  </colgroup>
  <thead>
  <tr class="row-odd"><th class="head"><p>属性名称</p></th>
  <th class="head"><p>格式</p></th>
  <th class="head"><p>描述</p></th>
  </tr>
  </thead>
  <tbody>
  <tr class="row-even"><td><p>args</p></td>
  <td><p>此属性不需要用户进行格式化。</p></td>
  <td><p>合并到 <code class="docutils literal notranslate"><span class="pre">msg</span></code> 以产生 <code class="docutils literal notranslate"><span class="pre">message</span></code> 的包含参数的元组，或是其中的值将被用于合并的字典（当只有一个参数且其类型为字典时）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>asctime</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(asctime)s</span></code></p></td>
  <td><p>表示 <a class="reference internal" href="#logging.LogRecord" title="logging.LogRecord"><code class="xref py py-class docutils literal notranslate"><span class="pre">LogRecord</span></code></a> 何时被创建的供人查看时间值。 默认形式为 '2003-07-08 16:49:45,896' （逗号之后的数字为时间的毫秒部分）。</p></td>
  </tr>
  <tr class="row-even"><td><p>created</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(created)f</span></code></p></td>
  <td><p><a class="reference internal" href="#logging.LogRecord" title="logging.LogRecord"><code class="xref py py-class docutils literal notranslate"><span class="pre">LogRecord</span></code></a> 被创建的时间（即 <a class="reference internal" href="time.html#time.time" title="time.time"><code class="xref py py-func docutils literal notranslate"><span class="pre">time.time()</span></code></a> 的返回值）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>exc_info</p></td>
  <td><p>此属性不需要用户进行格式化。</p></td>
  <td><p>异常元组（例如 <code class="docutils literal notranslate"><span class="pre">sys.exc_info</span></code>）或者如未发生异常则为 <code class="docutils literal notranslate"><span class="pre">None</span></code>。</p></td>
  </tr>
  <tr class="row-even"><td><p>文件名</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(filename)s</span></code></p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">pathname</span></code> 的文件名部分。</p></td>
  </tr>
  <tr class="row-odd"><td><p>funcName</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(funcName)s</span></code></p></td>
  <td><p>函数名包括调用日志记录.</p></td>
  </tr>
  <tr class="row-even"><td><p>levelname</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(levelname)s</span></code></p></td>
  <td><p>消息文本记录级别（<code class="docutils literal notranslate"><span class="pre">'DEBUG'</span></code>，<code class="docutils literal notranslate"><span class="pre">'INFO'</span></code>，<code class="docutils literal notranslate"><span class="pre">'WARNING'</span></code>，<code class="docutils literal notranslate"><span class="pre">'ERROR'</span></code>，<code class="docutils literal notranslate"><span class="pre">'CRITICAL'</span></code>）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>levelno</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(levelno)s</span></code></p></td>
  <td><p>消息数字的记录级别 (<code class="xref py py-const docutils literal notranslate"><span class="pre">DEBUG</span></code>, <code class="xref py py-const docutils literal notranslate"><span class="pre">INFO</span></code>, <code class="xref py py-const docutils literal notranslate"><span class="pre">WARNING</span></code>, <code class="xref py py-const docutils literal notranslate"><span class="pre">ERROR</span></code>, <code class="xref py py-const docutils literal notranslate"><span class="pre">CRITICAL</span></code>).</p></td>
  </tr>
  <tr class="row-even"><td><p>lineno</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(lineno)d</span></code></p></td>
  <td><p>发出日志记录调用所在的源行号（如果可用）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>message</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(message)s</span></code></p></td>
  <td><p>记入日志的消息，即 <code class="docutils literal notranslate"><span class="pre">msg</span> <span class="pre">%</span> <span class="pre">args</span></code> 的结果。 这是在发起调用 <a class="reference internal" href="#logging.Formatter.format" title="logging.Formatter.format"><code class="xref py py-meth docutils literal notranslate"><span class="pre">Formatter.format()</span></code></a> 时设置的。</p></td>
  </tr>
  <tr class="row-even"><td><p>module -- 模块</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(module)s</span></code></p></td>
  <td><p>模块 (<code class="docutils literal notranslate"><span class="pre">filename</span></code> 的名称部分)。</p></td>
  </tr>
  <tr class="row-odd"><td><p>msecs</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(msecs)d</span></code></p></td>
  <td><p><a class="reference internal" href="#logging.LogRecord" title="logging.LogRecord"><code class="xref py py-class docutils literal notranslate"><span class="pre">LogRecord</span></code></a> 被创建的时间的毫秒部分。</p></td>
  </tr>
  <tr class="row-even"><td><p>msg</p></td>
  <td><p>此属性不需要用户进行格式化。</p></td>
  <td><p>在原始日志记录调用中传入的格式字符串。 与 <code class="docutils literal notranslate"><span class="pre">args</span></code> 合并以产生 <code class="docutils literal notranslate"><span class="pre">message</span></code>，或是一个任意对象 (参见 <a class="reference internal" href="../howto/logging.html#arbitrary-object-messages"><span class="std std-ref">使用任意对象作为消息</span></a>)。</p></td>
  </tr>
  <tr class="row-odd"><td><p>名称</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(name)s</span></code></p></td>
  <td><p>用于记录调用的日志记录器名称。</p></td>
  </tr>
  <tr class="row-even"><td><p>pathname</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(pathname)s</span></code></p></td>
  <td><p>发出日志记录调用的源文件的完整路径名（如果可用）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>process</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(process)d</span></code></p></td>
  <td><p>进程ID（如果可用）</p></td>
  </tr>
  <tr class="row-even"><td><p>processName</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(processName)s</span></code></p></td>
  <td><p>进程名（如果可用）</p></td>
  </tr>
  <tr class="row-odd"><td><p>relativeCreated</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(relativeCreated)d</span></code></p></td>
  <td><p>以毫秒数表示的 LogRecord 被创建的时间，即相对于 logging 模块被加载时间的差值。</p></td>
  </tr>
  <tr class="row-even"><td><p>stack_info</p></td>
  <td><p>此属性不需要用户进行格式化。</p></td>
  <td><p>当前线程中从堆栈底部起向上直到包括日志记录调用并引发创建当前记录堆栈帧创建的堆栈帧信息（如果可用）。</p></td>
  </tr>
  <tr class="row-odd"><td><p>thread</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(thread)d</span></code></p></td>
  <td><p>线程ID（如果可用）</p></td>
  </tr>
  <tr class="row-even"><td><p>threadName</p></td>
  <td><p><code class="docutils literal notranslate"><span class="pre">%(threadName)s</span></code></p></td>
  <td><p>线程名（如果可用）</p></td>
  </tr>
  </tbody>
  </table>
  </details>

---

# 13.2. logging模块进阶教程：

## 1. logging模块的主要组件有哪些？
  
  * 记录器[logger](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger)：为应用程序提供直接使用的日志接口
  * 处理器[handler](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler)：将日志记录（LogRecord，由记录器创建）发送到适当的目标（控制台、文件、邮件等接收对象）
  * 过滤器[filter](https://docs.python.org/zh-cn/3/library/logging.html#logging.Filter)：提供更细粒度的功能，用于确定要输出的日志记录。
  * 格式化器[formatter](https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter)：指定要输出日志记录的样式

---

## 2. 除了以上4个组件还有哪些重要概念？
  * [LogRecord](https://docs.python.org/zh-cn/3/library/logging.html#logging.LogRecord): 日志事件信息以LogRecord对象的格式在logger、handler、filter和formatter之间传递。即LogRecord对象代表一条日志本身的信息。

  * 记录器的层次结构：开发者可以通过调用logger类实例来执行日志记录。每个logger实例都有一个名称，名称可以通过点号(.)作为分隔符构成层级结构，如名为 'scan' 的记录器是记录器 'scan.text' ，'scan.html' 和 'scan.pdf' 的父级。 记录器名称可以是你想要的任何名称，并指示记录消息源自的应用程序区域。
  一个好的命名习惯是在每个使用日志记录器的模块中使用模块级记录器：`logger = logging.getLogger(__name__)`。这样记录器名称跟随包或模块的层级结构，可以直观地从日志记录器名称找到事件发生点。

  * 根记录器：记录器层次结构的根称为`根记录器`。 这是函数 debug() 、 info() 、 warning() 、 error() 和 critical() 使用的记录器，它们就是调用了根记录器的同名方法。 函数和方法具有相同的签名。 根记录器的名称在输出中打印为 'root' 。

  * 目标：消息记录想要保存的不同地方称为目标。 软件包中的支持包含，用于将日志消息写入文件、 HTTP GET/POST 位置、通过 SMTP 发送电子邮件、通用套接字、队列或特定于操作系统的日志记录机制（如 syslog 或 Windows NT 事件日志）。 `目标由 handler 类提供`。 如果你有任何内置处理器类未满足的特殊要求，则可以创建自己的日志目标类。`默认情况下，没有为任何日志消息设置目标。` 你可以使用 basicConfig() 指定目标（例如控制台或文件），如教程示例中所示。 如果你调用函数 debug() 、 info() 、 warning() 、 error() 和 critical() ，它们将检查是否有设置目标；如果没有设置，将在委托给根记录器进行实际的消息输出之前设置目标为控制台（ sys.stderr ）并设置显示消息的默认格式。

---

## 2. 日志的记录流程：
  
  记录器和处理器中的日志事件信息流程如下所示：
  ![](./images/logging_flow.png)
  1. 记录器允许该等级的日志调用吗？不允许则结束；
  2. 创建LogRecord对象；
  3. 记录器有附加的过滤器拒绝该LogRecord吗？有则结束；
  4. 将LogRecord对象传递给当前记录器附加的处理器；
     1. 处理器允许该等级的LogRecord吗？不允许则结束；
     2. 处理器附加的过滤器拒绝该记录吗？拒绝则结束；
     3. 不拒绝则执行emit()方法，格式化并发送请求到目标；
  5. 当前记录器的propagate属性(控制子记录器是否将消息传播带与其父记录器关联的处理器)设置为true吗？False则结束；
  6. 当前记录器有父记录器吗？没有则结束;
  7. 有父记录器则将父记录器设为当前的记录器？？？

---

## 3. 记录器的功能是什么？
  
  Logger对象有三重任务：
  * 为程序提供记录日志的几种方法；
  * 根据严重性（默认过滤工具）或过滤器对象确定要处理的日志消息；
  * 将相关的日志消息传递给相关的日志处理器。
  
---

## 4. Logger对象的主要方法有哪些？

  Logger对象主要使用的方法有两类：配置和创建消息：
  * 配置：
    * Logger.setLevel() 指定记录器将处理的最低严重性日志消息，其中 debug 是最低内置严重性级别， critical 是最高内置严重性级别。 例如，如果严重性级别为 INFO ，则记录器将仅处理 INFO 、 WARNING 、 ERROR 和 CRITICAL 消息，并将忽略 DEBUG 消息。
    * Logger.addHandler() 和 Logger.removeHandler() 从记录器对象中添加和删除处理器对象。
    * Logger.addFilter() 和 Logger.removeFilter() 可以添加或移除记录器对象中的过滤器。 
  
  * 创建消息：
    * Logger.debug() 、 Logger.info() 、 Logger.warning() 、 Logger.error() 和 Logger.critical() 都创建日志记录，包含消息和与其各自方法名称对应的级别。该消息实际上是一个格式化字符串，它可能包含标题字符串替换语法 %s 、 %d 、 %f 等等。其余参数是与消息中的替换字段对应的对象列表。关于 **kwargs ，日志记录方法只关注 exc_info 的关键字，并用它来确定是否记录异常信息。
    * Logger.exception() 创建与 Logger.error() 相似的日志信息。 不同之处是， Logger.exception() 同时还记录当前的堆栈追踪。仅从异常处理程序调用此方法。
    * Logger.log() 将日志级别level作为显式参数。对于记录消息而言，这比使用上面列出的日志级别便利方法更加冗长，但这是使用自定义日志级别的方法。

---

## 5. 如何在程序中湖区记录器对象？
  
  调用logging.getLogger() 方法，传入logger名称，就会返回对具有指定名称的记录器实例的引用（如果已提供），或者如果没有则返回 root 根记录器。

---

## 6. 记录器有哪些特性？

  * 记录器具有**有效等级**的概念。如果未在记录器上显式设置级别（setLevel()），则使用其父记录器的级别作为其有效级别。如果父记录器没有明确的级别设置，则检查父记录器的父级。依此类推，搜索所有上级元素，直到找到明确设置的级别。根记录器始终具有显式级别集（默认情况下为 WARNING ）。在决定是否处理事件时，记录器的有效级别用于确定事件是否传递给记录器相关的处理器。

  * 传播特性：子记录器会将消息传播到与其父级记录器关联的处理器。因此，不必为应用程序使用的所有记录器定义和配置处理器。一般为顶级记录器配置处理器，再根据需要创建子记录器就足够了。（但是，你可以通过将记录器的 `propagate 属性`设置为 False 来关闭传播。）

---

## 7. 处理器的主要功能是什么？
  
  Handler对象负责将适当的日志消息（基于消息的等级）发送给处理器指定的目标。Logger对象可以使用addHandler()方法为自己添加0个或多个处理器。
  
  如，应用可能希望将所有日志消息输出到日志文件，将错误或更高级别的日志发送到标准输出，以及将关键消息通过邮件发送通知管理员。这就需要为logger添加3个不同的处理器，每个处理器负责将特定等级的消息发送到不同的目标。

---

## 8. logging提供了哪些内置的有用处理器？

  logging库中提供了很多[预定义的处理器类型](https://docs.python.org/zh-cn/3/howto/logging.html#useful-handlers)，方便我们使用：

  <details>
  <ol class="arabic simple">
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.StreamHandler" title="logging.StreamHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">StreamHandler</span></code></a> 实例发送消息到流（类似文件对象）。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.FileHandler" title="logging.FileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">FileHandler</span></code></a> 实例将消息发送到硬盘文件。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.BaseRotatingHandler" title="logging.handlers.BaseRotatingHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">BaseRotatingHandler</span></code></a> 是轮换日志文件的处理器的基类。它并不应该直接实例化。而应该使用 <a class="reference internal" href="../library/logging.handlers.html#logging.handlers.RotatingFileHandler" title="logging.handlers.RotatingFileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">RotatingFileHandler</span></code></a> 或 <a class="reference internal" href="../library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler" title="logging.handlers.TimedRotatingFileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">TimedRotatingFileHandler</span></code></a> 代替它。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.RotatingFileHandler" title="logging.handlers.RotatingFileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">RotatingFileHandler</span></code></a> 实例将消息发送到硬盘文件，支持最大日志文件大小和日志文件轮换。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler" title="logging.handlers.TimedRotatingFileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">TimedRotatingFileHandler</span></code></a> 实例将消息发送到硬盘文件，以特定的时间间隔轮换日志文件。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.SocketHandler" title="logging.handlers.SocketHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">SocketHandler</span></code></a> 实例将消息发送到 TCP/IP 套接字。从 3.4 开始，也支持 Unix 域套接字。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.DatagramHandler" title="logging.handlers.DatagramHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">DatagramHandler</span></code></a> 实例将消息发送到 UDP 套接字。从 3.4 开始，也支持 Unix 域套接字。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.SMTPHandler" title="logging.handlers.SMTPHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">SMTPHandler</span></code></a> 实例将消息发送到指定的电子邮件地址。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.SysLogHandler" title="logging.handlers.SysLogHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">SysLogHandler</span></code></a> 实例将消息发送到 Unix syslog 守护程序，可能在远程计算机上。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.NTEventLogHandler" title="logging.handlers.NTEventLogHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">NTEventLogHandler</span></code></a> 实例将消息发送到 Windows NT/2000/XP 事件日志。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.MemoryHandler" title="logging.handlers.MemoryHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryHandler</span></code></a> 实例将消息发送到内存中的缓冲区，只要满足特定条件，缓冲区就会刷新。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.HTTPHandler" title="logging.handlers.HTTPHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">HTTPHandler</span></code></a> 实例使用 <code class="docutils literal notranslate"><span class="pre">GET</span></code> 或 <code class="docutils literal notranslate"><span class="pre">POST</span></code> 方法将消息发送到 HTTP 服务器。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.WatchedFileHandler" title="logging.handlers.WatchedFileHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">WatchedFileHandler</span></code></a> 实例会监视他们要写入日志的文件。如果文件发生更改，则会关闭该文件并使用文件名重新打开。此处理器仅在类 Unix 系统上有用； Windows 不支持依赖的基础机制。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.handlers.QueueHandler" title="logging.handlers.QueueHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">QueueHandler</span></code></a> 实例将消息发送到队列，例如在 <a class="reference internal" href="../library/queue.html#module-queue" title="queue: A synchronized queue class."><code class="xref py py-mod docutils literal notranslate"><span class="pre">queue</span></code></a> 或 <a class="reference internal" href="../library/multiprocessing.html#module-multiprocessing" title="multiprocessing: Process-based parallelism."><code class="xref py py-mod docutils literal notranslate"><span class="pre">multiprocessing</span></code></a> 模块中实现的队列。</p></li>
<li><p><a class="reference internal" href="../library/logging.handlers.html#logging.NullHandler" title="logging.NullHandler"><code class="xref py py-class docutils literal notranslate"><span class="pre">NullHandler</span></code></a> 实例对错误消息不执行任何操作。它们由想要使用日志记录的库开发人员使用，但是想要避免如果库用户没有配置日志记录，则显示 'No handlers could be found for logger XXX' 消息的情况。更多有关信息，请参阅 <a class="reference internal" href="#library-config"><span class="std std-ref">配置库的日志记录</span></a> 。</p></li>
</ol>
  </details>

其中，NullHandler、 StreamHandler 和 FileHandler 类在核心日志包中（logging）定义。其他处理器定义在 logging.handlers 中。（还有另一个子模块 logging.config ，用于配置功能）

---

## 9. 处理器的主要方法有哪些？

  handler中很少有方法给开发者使用，使用内置的处理器仅有以下几种方法可以调用：

  * setLevel() 方法，就像在记录器对象中一样，指定将被分派到适当目标的最低严重性。为什么有两个 setLevel() 方法？记录器中设置的级别确定将传递给其处理器的消息的严重性。每个处理器中设置的级别确定该处理器将发送哪些消息。
  * setFormatter() 选择一个该处理器使用的 Formatter 对象。
  * addFilter() 和 removeFilter() 分别在处理器上配置和取消配置过滤器对象。

  应用程序代码不应直接实例化并使用 Handler 的实例。 相反， Handler 类是一个基类，它定义了所有处理器应该具有的接口，并建立了子类可以使用（或覆盖）的一些默认行为。`使用时一般直接实例化其子类使用，如StreamHandler、FileHandler等`。

---

## 10. 格式化器的主要功能是什么，如何创建格式化器？

  formatter主要用来配置日志消息的最终顺序、结构和内容。
  
  Formatter的构造函数有三个可选参数：消息格式字符串、日期格式字符串和样式指示符。
  `logging.Formatter.__init__(fmt=None, datefmt=None, style='%')`

  * 如果没有消息格式字符串，则默认使用原始消息。
  
  * 如果没有日期格式字符串，则默认日期格式为：`%Y-%m-%d %H:%M:%S`。最后加上毫秒数。 
  
  * style 是 ％，'{' 或 '$' 之一。 如果未指定，则将使用 '％'。
    * 如果 style 是 '％'，则消息格式字符串使用`%(<dictionary key>)s`样式字符串替换；可能的键值在 [LogRecord 属性](https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes) 中。 
    * 如果样式为 '{'，则假定消息格式字符串与 [str.format()](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format) （使用关键字参数）兼容;
    * 如果样式为 '$' ，则消息格式字符串应符合 [string.Template.substitute()](https://docs.python.org/zh-cn/3/library/string.html#string.Template.substitute) 。

以下消息格式字符串将以人类可读的格式记录时间、消息的严重性以及消息的内容，按此顺序:

`%(asctime)s - %(levelname)s - %(message)s`

格式器通过用户可配置的函数将记录的创建时间转换为元组。 默认情况下，使用 time.localtime() ；要为特定格式器实例更改此项，请将实例的 converter 属性设置为与 time.localtime() 或 time.gmtime() 具有相同签名的函数。 

要为所有格式化器更改它，例如，如果你希望所有记录时间都以 GMT 显示，请在格式器类中设置 converter 属性（对于 GMT 显示，设置为 time.gmtime ）。

---

## 11. 如何[配置logging模块](https://docs.python.org/zh-cn/3/library/logging.config.html#logging-config-api)？

有三种方法可以配置logging：

1. 使用上面介绍的Logger对象、Handler对象和Formatter对象中的配置方法在代码中进行配置：
   
   ```python
   import logging
   
   # create logger
   logger = logging.getLogger('simple_example')
   logger.setLevel(logging.DEBUG)
   
   # create console handler and set level to debug
   ch = logging.StreamHandler()
   ch.setLevel(logging.DEBUG)
   
   # create formatter
   formatter = logging.Formatter('%(asctime)s - %   (name)s - %(levelname)s - %(message)s')
   
   # add formatter to ch
   ch.setFormatter(formatter)
   
   # add ch to logger
   logger.addHandler(ch)
   
   # 'application' code
   logger.debug('debug message')
   logger.info('info message')
   logger.warning('warn message')
   logger.error('error message')
   logger.critical('critical message')
   ```

   运行脚本：
   ```
   $ python simple_logging_module.py
   2005-03-19 15:10:26,618 - simple_example - DEBUG - debug message
   2005-03-19 15:10:26,620 - simple_example - INFO - info message
   2005-03-19 15:10:26,695 - simple_example - WARNING - warn message
   2005-03-19 15:10:26,697 - simple_example - ERROR - error message
   2005-03-19 15:10:26,773 - simple_example - CRITICAL - critical message
   ```

2. 创建logging的配置文件`logging.conf`，并在代码中使用[fileConfig()](https://docs.python.org/zh-cn/3/library/logging.config.html#logging.config.fileConfig)函数读取配置文件：

   logging.conf文件：
   ```ini
   [loggers]
   keys=root,simpleExample
   
   [handlers]
   keys=consoleHandler
   
   [formatters]
   keys=simpleFormatter
   
   [logger_root]
   level=DEBUG
   handlers=consoleHandler
   
   [logger_simpleExample]
   level=DEBUG
   handlers=consoleHandler
   qualname=simpleExample
   propagate=0
   
   [handler_consoleHandler]
   class=StreamHandler
   level=DEBUG
   formatter=simpleFormatter
   args=(sys.stdout,)
   
   [formatter_simpleFormatter]
   format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
   ```
   在代码中读取配置：
   ```python
   import logging
   import logging.config
   
   logging.config.fileConfig('logging.conf')
   
   # create logger
   logger = logging.getLogger('simpleExample')
   
   # 'application' code
   logger.debug('debug message')
   logger.info('info message')
   logger.warning('warn message')
   logger.error('error message')
   logger.critical('critical message')
   ```
   运行脚本，日志输出：
   ```
   $ python simple_logging_config.py
   2005-03-19 15:38:55,977 - simpleExample - DEBUG - debug message
   2005-03-19 15:38:55,979 - simpleExample - INFO - info message
   2005-03-19 15:38:56,054 - simpleExample - WARNING - warn message
   2005-03-19 15:38:56,055 - simpleExample - ERROR - error message
   2005-03-19 15:38:56,130 - simpleExample - CRITICAL - critical message
   ```
   
   可以看到配置文件方法相较于 Python 代码方法有一些优势，主要是配置和代码的分离以及非开发者轻松修改日志记录属性的能力。

3. 创建logging配置信息字典，并在代码中使用[dictConfig()](https://docs.python.org/zh-cn/3/library/logging.config.html#logging.config.dictConfig)函数读取：
   
   在 Python 3.2 中，引入了一种新的配置日志记录的方法，使用字典来保存配置信息。 
   
   这提供了上述基于配置文件方法的功能的超集，并且是新应用程序和部署的推荐配置方法。 因为 Python 字典用于保存配置信息，并且由于你可以使用不同的方式填充该字典，因此你有更多的配置选项。 
   
   例如，你可以使用 JSON 格式的配置文件，或者如果你有权访问 YAML 处理功能，则可以使用 YAML 格式的文件来填充配置字典。当然，你可以在 Python 代码中构造字典，通过套接字以 pickle 形式接收它，或者使用对你的应用程序合理的任何方法。

   以下是与上述相同配置的示例，采用 YAML 格式，用于新的基于字典的方法：
   ```yaml
   version: 1
   formatters:
     simple:
       format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   handlers:
     console:
       class: logging.StreamHandler
       level: DEBUG
       formatter: simple
       stream: ext://sys.stdout
   loggers:
     simpleExample:
       level: DEBUG
       handlers: [console]
       propagate: no
   root:
     level: DEBUG
     handlers: [console]
   ```
   然后在代码中读取该yaml文件，将其转换为Python字典，在使用dictConfig()方法即可。

***警告*** :

    fileConfig() 函数接受一个默认参数 disable_existing_loggers ，出于向后兼容的原因，默认为 True 。这可能与您的期望不同，因为除非在配置中明确命名它们（或其父级），否则它将导致在 fileConfig() 调用之前存在的任何非 root 记录器被禁用。有关更多信息，请参阅参考文档，如果需要，请将此参数指定为 False 。

    传递给 dictConfig() 的字典也可以用键 disable_existing_loggers 指定一个布尔值，如果没有在字典中明确指定，也默认被解释为 True 。这会导致上面描述的记录器禁用行为，这可能与你的期望不同——在这种情况下，请明确地为其提供 False 值。

---

## 12. 如果没有为logging提供配置会怎样？

如果未提供日志记录配置，则可能出现需要输出日志记录事件但无法找到输出事件的处理器的情况。 在这些情况下，logging 包的行为取决于 Python 版本。

* 对于 3.2 之前的 Python 版本，行为如下：

  * 如果 logging.raiseExceptions 为 False （生产模式），则会以静默方式丢弃该事件。

  * 如果 logging.raiseExceptions 为 True （开发模式），则会打印一条消息 'No handlers could be found for logger X.Y.Z'。

* 在 Python 3.2 及更高版本中，行为如下：

  * 事件使用存储在 logging.lastResort 中的“handler of last resort” 输出。 这个内置的处理器与任何记录器都没有关联，它的作用类似于 StreamHandler（将事件描述消息写入 sys.stderr）。 不对消息进行格式化，只打印裸事件描述消息。处理器的级别设置为 WARNING，因此将输出此级别和更高级别的所有事件。

如果想要执行 python3.2 之前的行为，可以设置 logging.lastResort 为 None。

---

## 13. 日志级别的数字化表示是什么？

每个日志级别都有一个对应的数字表示，如下表所示：
|级别|数值|
|--|--|
|CRITICAL|50|
|ERROR|40|
|WARNING|30|
|INFO|20|
|DEBUG|10|
|NOTSET|0|

如果你想要定义自己的级别，并且需要它们具有相对于预定义级别的特定值，那么这你可能对以下内容感兴趣。如果你定义具有相同数值的级别，它将覆盖预定义的值；预定义的名称将失效。

级别也可以与记录器相关联，由开发人员设置或通过加载已保存的日志记录配置。在记录器上调用日志记录方法时，记录器会将其自己的级别与与方法调用关联的级别进行比较。如果记录器的级别高于方法调用的级别，则实际上不会生成任何记录消息。这是`控制日志记录输出详细程度的基本机制`。

---

## 14. LogRecord对象的作用是什么？

记录消息使用 LogRecord 类实例表示。当记录器决定实际记录事件时，将为记录消息创建 LogRecord 实例。

记录消息受 handlers（Handler 类的子类实例）建立的调度机制控制。处理器负责确保记录的消息（以 LogRecord 的形式）最终位于对该消息的目标受众（例如最终用户、 支持服务台员工、系统管理员、开发人员）有用的特定位置（或一组位置）上。处理器传递适用于特定目标的 LogRecord 实例。 每个记录器可以有零个、一个或多个与之关联的处理器（通过 Logger 的 addHandler() 方法）。除了与记录器直接关联的所有处理器之外，还调用与记录器的所有祖先关联的处理器来分派消息（除非记录器的 propagate 标志设置为 false 值，这将停止传递到上级处理器）。

就像记录器一样，处理器可以具有与它们相关联的级别。处理器的级别和记录器的级别一样，都是作为过滤器使用。如果处理器决定调度一个事件，则使用 [emit()方法](https://docs.python.org/zh-cn/3/library/logging.html#logging.Handler.emit)将消息发送到其目标。大多数用户定义的 Handler 子类都需要重载 emit() 。

---

## 15. 记录消息时触发异常会怎样？

logging 包设计为`忽略记录日志生产时发生的异常`。这样，处理日志记录事件时发生的错误（例如日志记录错误配置、网络或其他类似错误）不会导致使用日志记录的应用程序过早终止。

SystemExit 和 KeyboardInterrupt 异常永远不会被忽略。 在 Handler 子类的 emit() 方法中发生的其他异常被传递给它的 handleError() 方法。

Handler 中默认实现的 handleError() 检查是否设置了模块级变量 raiseExceptions 。如果有设置，则会将回溯打印到 sys.stderr 。如果未设置，则忽略异常。

注解： raiseExceptions 默认值是 True。 这是因为在开发期间，你通常希望收到任何发生异常的通知。建议你将 raiseExceptions 设置为 False 以供生产环境使用。

---

## 16. 如何使用任意对象作为消息？

在前面的部分和示例中，都假设记录事件时传递的消息是字符串。 但是，这不是唯一的可能性。你可以将任意对象作为消息传递，并且当日志记录系统需要将其转换为字符串表示时，将调用其 `__ str__() 方法`。

实际上，如果你愿意，你可以完全避免计算字符串表示。例如， SocketHandler 用 pickle 处理事件后通过网络进行发送。

---

更多复杂操作参考[日志操作手册](https://docs.python.org/zh-cn/3/howto/logging-cookbook.html#logging-cookbook)。