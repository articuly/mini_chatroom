from flask import Flask, render_template, redirect, url_for, session
from libs import db
from models import User
from settings import config
from views.users import user_app
from views.chatroom import chat_app
from forms.account_form import LoginForm

# 实例化Flask
app = Flask(__name__)
app.config.from_object(config['development'])

# 初始化各种插件
db.init_app(app)

# 注册蓝图功能
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(chat_app, url_prefix='/chat')


@app.route('/')
def html():
    return render_template('index.html')


@app.route('/index')
def index():
    return redirect(url_for('html'))


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):  # 验证密码
            session['user'] = user.username
            print(f'{username} 登陆成功')
            return redirect(url_for('index'))
        else:
            message = '用户名与密码不匹配'
    else:
        print(form.errors)
    return render_template('login.html', message=message, form=form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')  # 删除session中的用户
    return redirect(url_for('index'))


# 上下文处理函数，全局传出的模板变量username
@app.context_processor
def account():
    username = session.get('user')
    return {'username': username}

# if __name__ == '__main__':
#     app.run()
