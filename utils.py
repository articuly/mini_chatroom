from libs import db
from models import User, Message
import random


# 创建两个初始用户：admin, articuly
def create_admin():
    user1 = User(realname='admin', username='admin', is_single='1', sex='1', education='3', city='020', hobby='writing')
    user1.hash_password('123654')
    db.session.add(user1)
    user2 = User(realname='articuly', username='articuly', is_single='2', sex='1', education='3', city='020',
                 hobby='singing')
    user2.hash_password('123654')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()


# 创建N个随机用户
def random_user(n):
    words = list('abcdefghijklmnopqrstuvwxyz')
    cities = ['010', '020', '021', '023', '0755', '0571', '0512']
    hobbies = ['travel', 'talking', 'singing', 'dancing', 'writing', "fishing", "gym"]
    for i in range(n):
        random.shuffle(words)
        username = ''.join(words[:6])
        sex = random.randint(1, 3)
        is_single = random.randint(1, 2)
        education = random.randint(1, 6)
        city = cities[random.randint(0, 6)]
        random.shuffle(hobbies)
        hobby = ', '.join(hobbies[0:random.randint(0, 6)])
        user = User(
            realname=username,
            username=username,
            sex=sex,
            is_single=is_single,
            education=education,
            city=city,
            hobby=hobby,
        )
        user.hash_password('123456')  # default password is 123456
        db.session.add(user)
    db.session.commit()


# 创建N条随机消息
def random_message(n):
    words = list('abcdefghijklmnopqrstuvwxyz')
    for i in range(n):
        random.shuffle(words)
        username = ''.join(words[:6])
        message = Message(
            from_user=username,
            content='{0} is talking some random word and saying hello to the world.'
        )
        db.session.add(message)
    db.session.commit()
