# Flask入门

## Flask介绍

FLask是一款发布于2010年非常流程的 Python Web 框架，WSGI工具箱采用Werkzeug（路由模块），模板引擎则使用Jinja2，这两个是Flask框架的核心。其拥有一下特点：

- 微框架、简洁，给开发者提供很大的扩展性
- Flask 拥有众多好用的插件，做到了开箱即用
- 开发效率高

FLask的灵活度很好，开发者可以按照自己的意愿进行更改。Flask本身相当于一个内核，其他几乎所有的功能都要用到扩展（邮件扩展 Flask-Mail，用户认证 Flask-Login，数据库 Flask-SQLAlchemy），都需要用第三方的扩展来实现。下面是flask常见的扩展：

- Flask-SQLalchemy：操作数据库
- Flask-script：插入脚本
- Flask-migrate：管理迁移数据库
- Flask-Session：Session存储方式指定
- Flask-WTF：表单
- Flask-Mail：邮件
- Flask-Bable：提供国际化和本地化支持，翻译
- Flask-Login：认证用户状态
- Flask-OpenID：认证
- Flask-RESTful：开发REST API的工具
- Flask-Bootstrap：集成前端Twitter Bootstrap框架
- Flask-Moment：本地化日期和时间
- Flask-Admin：简单而可扩展的管理接口的框架

## Flask的安装

``` 
pip install flask -i https://pypi.douban.com/simple 
```

## 第一个Flask程序

```python
# 引入FLask对象用于创建web应用
from flask import Flask

# 创建对象
app = Flask(__name__)

# 创建路由
@app.route("/")
def home_view():
    return "Hello world"

# 启动 web 应用
if __name__ == "__main__":
    # 默认监听127.0.0.1:5000
    app.run()
```

启动服务

```shell
 $ python 01_hello.py
 * Serving Flask app '01_flask第一个程序'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## Flask应用运行方式

- 通过对象运行 

```python
app.run(host="0.0.0.0", port=5000)
```

- 通过python方式运行

```shell
python filename.py 
```

- 通过flask自带命令运行,这种运行方式可以省略程序中的`app.run()`

```shell
export FLASK_APP=01_flask第一个程序
flask.exe run

# 参数解析
flask.exe run -h 0.0.0.0 -p 8000
```

## Flask配置加载方式

- 运行时传递参数，开启debug模式：`app.run(debug=True)`
- 通过debug参数设置：`app.debug=True`
- 通过修改配置参数config：`app.config.update(DEBUG=True)` or `app.config['DEBUG'] = True`
- 通过from_mapping加载: `app.config.from_mapping({"DEBUG": True})`
- 通过配置对象设置config

```python
from flask import Flask
class BaseConfig:
    DEBUG=True

app = Flask(__name__)
@app.route("/")
def home_view():
    return "Hello world"

if __name__ == "__main__":
    app.config.from_object(BaseConfig)
    app.run()
```

- 通过配置文件设置config

```python
#config.py
DEBUG = True
```
```python
from flask import Flask

app = Flask(__name__)
@app.route("/")
def home_view():
    return "Hello world"

if __name__ == "__main__":
    app.config.from_pyfile("config.py")
    app.run()
```

- 通过环境变量

```python
# settings.cfg
DEBUG = True
```
```python
# 01_hello.py
import os

from flask import Flask

app = Flask(__name__)
@app.route("/")
def home_view():
    return "Hello world"

# if os.getenv("DEBUG"):
#     print(os.getenv("DEBUG"))
if __name__ == "__main__":
    app.config.from_envvar('CONF')
    app.run()
```
```shell
export CONF='settings.cfg'
python 01_hello.py
```

## 动态路由

####  路径参数类型

Flask可以传递多种类型的数据，语法为`converter:variable`, 其中converter 为类型名称，其可以用一下几种：

- string: 如果没有指定具体类型，默认为 string 类型
- int: 数据传递只能是int类型
- float: 数据传递只能是float类型
- path: 可以接受任意字符串，包括斜杆等路径
- uuid: 只能接收符合uuid的字符串
- any： 数据类型可以在一个url中指定多个路径 

```python
import os

from flask import Flask

app = Flask(__name__)

# http://127.0.0.1:5000/book/1001
# http://127.0.0.1:5000/user/1001
@app.route("/<any(user,book):item>/<int:id>")
def view(item, id):
    print(item, id)
    return f"{item}=={id}"

# if os.getenv("DEBUG"):
#     print(os.getenv("DEBUG"))
if __name__ == "__main__":
    app.run(debug=True)
```

> 若是数据与设置的类型不能匹配，则会返回 Not Found

#### 自定义转换器

路径参数可以直接识别数据类型的根本原因是因为wekzeug.routing 导入 BaseConverter 类来识别底层类型，int 路径参数调用底层 IntegerConverter 类来作为格式判断，float 路径参数调用底层 FloatConverter 类来作为格式判断，所以如果Flask内置转换器无法满足需求时，需要自定义转换器。自定义转换器方法如下：

- 创建转换器，保存匹配时的正则表达式
- 将自定义的转换器注册到Flask应用
- 子使用转换器的地方定义使用

下面是一个手机号转换器的自定义样例

```python
import os
from werkzeug.routing import BaseConverter

class MobileConverter(BaseConverter):
    """
    手机号格式
    """
    # 1. 定义匹配的正则表达式
    regex =  r'1[3-9]\d{9}' # regex为固定写法，

from flask import Flask

app = Flask(__name__)

# 2. 注册转换器到字典中
app.url_map.converters['mobile'] = MobileConverter
@app.route("/sms/<mobile:mob_num>")
def view(mob_num):
    print(type(mob_num))
    return f"手机号=={mob_num}"

if __name__ == "__main__":
    app.run(debug=True)
```

- to_python:解决url `/user/zhanshan+18`的问题

在转换器类中，实现 to_python 方法。这个方法的返回值，将会传递到view函数中作为参数

```python
import typing as t

from flask import Flask
from werkzeug.routing import BaseConverter

class LiConverter(BaseConverter):
    def to_python(self, value: str) -> t.Any:
        return  value.split("+")

app = Flask(__name__)

app.url_map.converters["li"] = LiConverter

# http://127.0.0.1:5000/user/zhanshan+19
@app.route("/user/<li:info>")
def view(info):
    # name, age = info.split("+")
    name, age = info
    return f"用户的姓名为:{name}, 年龄：{age}"

if __name__ == "__main__":
    app.run(debug=True)
```

- to_url

在转换器中，实现 to_url 方法，这个方法的返回值，将会在调用url_for函数的时候生成复合要求的url形式


## GET查询参数的获取 

```python
from flask import Flask,request

app = Flask(__name__)

# http://127.0.0.1:5000/search?name=dengyouf&age=18
@app.route("/search")
def search():
    # name = request.args.get("name", None)
    # age = request.args.get("age", 0)
    name = request.values.get("name", None)
    age = request.values.get("age", 0)

    return f"用户:{name}, 年龄：{age}"

if __name__ == "__main__":
    app.run(debug=True)
```

## POST 请求体参数获取

```python
from flask import Flask,request

app = Flask(__name__)

'''
curl --location 'http://127.0.0.1:5000/search' \
--form 'name="dengyouf"' \
--form 'age="28"'
'''
@app.route("/search", methods=["POST"])
def search():
    # name = request.form.get("name", None)
    # age = request.form.get("age", 0)
    name = request.values.get("name", None)
    age = request.values.get("age", 0)

    return f"用户:{name}, 年龄：{age}"

if __name__ == "__main__":
    app.run(debug=True)
```

## 上传文件

```python
import os.path

from flask import Flask,request

app = Flask(__name__)

'''

'''
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("touxiang", None)
    if file:
        save_path = os.path.join(os.getcwd()+"/images/")
        # with open(save_path + "{}".format(file.filename), "wb+" ) as f:
        #     f.write(file.read())
        file.save(save_path + "{}".format(file.filename))

        return "Upload file success !!!"
    return  "Upload file failed !!!"

if __name__ == "__main__":
    app.run(debug=True)
```

## 其他参数

| 属性      | 说明             |类型 |
|---------|----------------| - |
| values  |记录请求的数据，并转换为字符串 |  * |
|form |记录请求中的表单数据| MultiDict
|args |记录请求中的查询参数 |MultiDict|
|cookies |记录请求中的cookie信息| Dict|
|headers |记录请求中的报文头| EnvironHeaders|
|method |记录请求使用的HTTP方法 |GET/POST|
|url |记录请求的URL地址| string|
|files| 记录请求上传的文件 |*|

## url_for 函数

通过函数获取路由URL

- url_for 函数可以接收1个及以上的参数，他接收函数名作为第 一个参数
- 如果还出现其他的参数，则会添加到 URL 的后面作为查询参数

```python
from flask import Flask,url_for,redirect

app = Flask(__name__)

@app.route("/get/list/<page>")
def get_list(page):
    return f"my list {page}"

@app.route("/")
def view():
    return  redirect(url_for("get_list", page=2, num=8))

if __name__ == "__main__":
    app.run(debug=True)
```

> 在定义url的时候，一定要记得在最后加一个斜杠。
>1. 如果不加斜杠，那么在浏览器中访问这个url的时候，如果最后加了斜杠，那么就访问不到。这样用户体验不太好。
>2. 搜索引擎会将不加斜杠的和加斜杠的视为两个不同的url。而其实加和不加斜杠的都是同一个url，那么就会给搜索引擎造成一个误解。加了斜杠，就不会出现没有斜杠的情况

## Flask 重定向

重定向是通过 redirect(location,code=302) 这个函数来实现的, location表示需要重定向到的 URL, 应该配合之前讲的 url_for() 函数来使用，code 表示采用哪个重定向，默认是 302 也即 暂时性重定向, 可以修改成 301 来实现永久性重定向

```python
from flask import Flask,url_for,redirect

app = Flask(__name__)
@app.route("/")
def view():
    return  "这是 Home 页"
@app.route("/home")
def home():
    return redirect(url_for("view"))
if __name__ == "__main__":
    app.run(debug=True)
```

## Flask响应

```python
from flask import Flask,Response, make_response

app = Flask(__name__)
@app.route("/")
def view():
    resp = make_response("这是响应内容")
    resp.headers["hello"] = "world"
    resp.status = '404 NOT FOUND'
    return resp

if __name__ == "__main__":
    app.run(debug=True)
```














