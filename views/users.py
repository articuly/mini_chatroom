from flask import redirect, url_for, render_template, session
from libs import db, login_required
from models import User
from flask import Blueprint
from forms.account_form import RegisterForm, EditInfoForm

user_app = Blueprint("user_app", __name__)


# 用户注册功能
@user_app.route('/register', methods=['get', 'post'])
def register():
    message = None
    form = RegisterForm()
    if form.validate_on_submit():
        if validate_username(form.data['username']):
            return render_template('user/register.html', message='用户名重复')
        realname = form.data['realname']
        username = form.data['username']
        password = form.data['password']
        sex = form.data['sex']
        is_single = form.data['is_single']
        city = form.data['city']
        education = form.data['education']
        hobby = ', '.join(form.data['hobby'])
        user = User(
            realname=realname,
            username=username,
            password=password,
            sex=sex,
            is_single=is_single,
            city=city,
            education=education,
            hobby=hobby,
        )
        # Hash方式加密原来的密码
        user.hash_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            message = '注册失败' + str(e)
    else:
        print(form.errors)
    return render_template('user/register.html', message=message, form=form)


# 验证是否存在同名用户
def validate_username(username):
    return User.query.filter_by(username=username).first()


# 会员修改自己的信息，普通会员只能修改自己的资料
@user_app.route("/edit_info/", methods=['get', 'post'])
@login_required
def edit_info():
    message = None
    form = EditInfoForm()
    user = User.query.filter_by(username=session['user']).one()
    if form.validate_on_submit():
        user.realname = form.data['realname']
        user.sex = form.data['sex']
        user.is_single = form.data['is_single']
        user.city = form.data['city']
        user.education = form.data['education']
        user.hobby = ', '.join(form.data['hobby'])
        password = form.data['password']
        if user.validate_password(password):
            try:
                db.session.commit()
                message = '修改成功'
            except Exception as e:
                print(str(e))
                message = '后台发生错误'
        else:
            message = '用户名与密码不匹配'
    elif form.errors:
        print(form.errors)
        message = '表单发生错误'
    else:
        form.realname.data = user.realname
        form.sex.data = user.sex
        form.is_single.data = user.is_single
        form.city.data = user.city
        form.education.data = user.education
        form.hobby.data = user.hobby
    return render_template("user/edit_info.html", message=message, user=user, form=form)
