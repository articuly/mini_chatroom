from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField, RadioField, widgets
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo


# 定义多选框的类
class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    option_widget = widgets.CheckboxInput()


# 登陆功能表单类
class LoginForm(FlaskForm):
    username = StringField('用户名', render_kw={'class': 'form-control', 'placeholder': '请输入用户名'},
                           validators=[DataRequired('请填写注册的用户名')])
    password = PasswordField('密码', render_kw={'class': 'form-control', 'placeholder': '请输入密码'},
                             validators=[DataRequired('请填写用户密码'),
                                         Length(6, 20, message='密码长度在6-20位之间')])
    submit = SubmitField('', render_kw={'class': 'btn btn-default', 'value': '登陆'})


# 敏感词列表功能
class BadWords:
    def __init__(self, bad_words, message=None):
        self.bad_words = bad_words
        if not message:
            message = '不能包含敏感词'
        self.message = message

    def __call__(self, form, field):
        print('自定义验证器调用')
        for word in self.bad_words:
            if field.data.find(word) != -1:
                raise ValidationError(self.message)


# 注册功能表单类
class RegisterForm(FlaskForm):
    realname = StringField('姓名：',
                           validators=[DataRequired('请填写真实姓名'),
                                       BadWords(['admin', 'articuly', '客户'], message='不能包括敏感词')],
                           render_kw={'class': 'form-control', 'placeholder': "请填写您的真实姓名"})
    username = StringField('用户名：',
                           validators=[DataRequired('请填写用户名'),
                                       BadWords(['admin', 'articuly', '客户服务'], message='不能包括敏感词'),
                                       Length(6, 20, message='用户名长度在6-20位之间')],
                           render_kw={'class': 'form-control', 'placeholder': '请填写您的用户名，至少6个字符'})
    password = PasswordField('设置密码：', validators=[DataRequired(message='请提供密码'), Length(6, 20, message='密码长度在6-20位之间')],
                             render_kw={'class': 'form-control', 'placeholder': "设置一个密码，至少6个字符"})
    confirmpassword = PasswordField('验证密码：', validators=[EqualTo('password', message='两次输入密码不一样')],
                                    render_kw={'class': 'form-control', 'placeholder': "请确认您的密码"})
    sex = RadioField('性别：',
                     choices=[("1", '男'), ("2", '女'), ('3', '保密')])
    is_single = RadioField('状态',
                           choices=[('1', '单身'), ('2', '非单身')])
    city = SelectField('城市：', validators=[DataRequired('请填写所在城市')],
                       choices=[('', '所在城市'), ('010', '北京'), ('021', '上海'), ('020', '广州'), ('0755', '深圳'),
                                ('0571', '杭州'), ('023', '重庆'), ('0512', '苏州')],
                       render_kw={'class': 'form-control'})
    education = SelectField('学历：', validators=[DataRequired('请选择学历')],
                            choices=[('', '学历'), ('1', '博士以上'), ('2', '硕士'), ('3', '本科'), ('4', '大专'),
                                     ('5', '高中或中专'), ('6', '初中以下')],
                            render_kw={'class': 'form-control'})
    hobby = CheckBoxField('爱好：', choices=[('travel', '旅行'), ('talking', '聊天'), ('singing', '唱歌'), ('fishing', '钓鱼'),
                                          ('writing', '写作'), ('gym', '健身'), ('dancing', '跳舞')],
                          render_kw={"class": "checkbox-inline"})
    submit = SubmitField('', render_kw={'class': 'btn btn-primary pull-right', 'value': '立即注册'})


class EditInfoForm(FlaskForm):
    realname = StringField('姓名：',
                           validators=[DataRequired('请填写真实姓名'),
                                       BadWords(['admin', '客户'], message='不能包括敏感词')],
                           render_kw={'class': 'form-control', 'placeholder': "请填写您的真实姓名"})
    sex = RadioField('性别：', coerce=int,
                     choices=[("1", '男'), ("2", '女'), ('3', '保密')])
    is_single = RadioField('状态', coerce=int,
                           choices=[('1', '单身'), ('2', '非单身')])
    city = SelectField('城市：', validators=[DataRequired('请填写所在城市')],
                       choices=[('', '所在城市'), ('010', '北京'), ('021', '上海'), ('020', '广州'), ('0755', '深圳'),
                                ('0571', '杭州'), ('023', '重庆'), ('0512', '苏州')],
                       render_kw={'class': 'form-control'})
    education = SelectField('学历：', validators=[DataRequired('请选择学历')],
                            choices=[('', '学历'), ('1', '博士以上'), ('2', '硕士'), ('3', '本科'), ('4', '大专'),
                                     ('5', '高中或中专'), ('6', '初中以下')],
                            render_kw={'class': 'form-control'})
    hobby = CheckBoxField('爱好：', choices=[('travel', '旅行'), ('talking', '聊天'), ('singing', '唱歌'), ('fishing', '钓鱼'),
                                          ('writing', '写作'), ('gym', '健身'), ('dancing', '跳舞')],
                          render_kw={"class": "checkbox-inline"})
    password = PasswordField('验证密码：',
                             validators=[DataRequired(message='必须提供密码'), Length(6, 20, message='密码长度在6-20位之间')],
                             render_kw={'class': 'form-control', 'placeholder': "请输入自己的密码"})
