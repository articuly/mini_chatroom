from flask import redirect, url_for, render_template, session
from libs import db, login_required
from models import Message
from flask import Blueprint

chat_app = Blueprint("chat_app", __name__)

@chat_app.route('/chatroom')
def chatroom():
    return render_template('chat/chatroom.html')