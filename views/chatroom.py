# coding:utf-8
from flask import render_template, session, request, jsonify
from libs import db, login_required
from models import Message
from flask import Blueprint
import app

chat_app = Blueprint("chat_app", __name__)


@chat_app.route('/chatroom', methods=['get', 'post'])
@login_required
def chatroom():
    # 使用跨文件方式调用变量userList，并更新session['userList']，在聊天室刷新即可看到最新在线的用户列表
    # 否则只能在调动login函数后才会新用户更新到session['userList']
    session['userList'] = app.userList
    if session['user'] not in app.userList:  # 确保session['userList']没有将当前漏用户
        session['userList'].append(session['user'])
    print(session['user'], '→在线用户', session['userList'])
    if request.method == 'GET':  # 当用户刷新页面取得最新的三类消息列表
        # 获得发给当前用户的消息，为私人消息
        receive_messages = db.session.query(Message).filter(Message.to_user == session['user']).order_by(
            Message.send_time.desc()).all()
        receive_messages.reverse()  # 让最新消息显示在下方
        receive_messages = receive_messages[-20:]  # 截取最新20条消息
        # 获得最新没有收信人的消息，为公共消息
        public_messages = db.session.query(Message).filter(
            (Message.to_user == None) | (Message.to_user == "")).order_by(Message.send_time.desc()).all()
        public_messages.reverse()
        public_messages = public_messages[-10:]
        # 获得最近自己发出去的消息，为近期消息
        recent_messages = db.session.query(Message).filter(Message.from_user == session['user'],
                                                    Message.to_user != "").order_by(Message.send_time.desc()).all()
        recent_messages.reverse()
        recent_messages = recent_messages[-20:]
        return render_template('chat/chatroom.html', receive_messages=receive_messages, public_messages=public_messages,
                               recent_messages=recent_messages)
    # 将发出去的消息加入数据库
    if request.method == 'POST':
        from_user = session['user']
        to_user = request.form['to_user']
        content = request.form['content']
        if content == '':  # 内容为空时，则消息发送失败
            result = {'result': 'fail'}
        else:
            message = Message(
                from_user=from_user,
                to_user=to_user,
                content=content
            )
            try:
                db.session.add(message)
                db.session.commit()
                print(session['user'], '发送了一条消息')
            except Exception as e:
                print(str(e))
                result = {'result': 'fail'}
            else:
                result = {'result': 'success'}
        return jsonify(result)
