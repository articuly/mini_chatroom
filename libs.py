from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from functools import wraps

# 创建数据库对象
db = SQLAlchemy()


# functools.wraps方式修饰全局的函数，如果没有登陆则跳转到登陆页
def login_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login'))
        else:
            print(func)
            return func(*args, **kwargs)

    return decorator_nest
