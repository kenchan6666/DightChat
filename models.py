from datetime import datetime

import bcrypt
from flask_login import UserMixin
from extensions import db



class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    dob = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128),nullable=False)
    role = db.Column(db.String(64), nullable=False, default='user')

    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    current_login_at = db.Column(db.DateTime, nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=False)
    current_login_ip = db.Column(db.String(128), nullable=True)
    last_login_ip = db.Column(db.String(128), nullable=True)
    total_login_count = db.Column(db.Integer, nullable=False)

    custom_background_color = db.Column(db.String(20), default='#ffffff')  # 用户背景颜色
    custom_background_image = db.Column(db.String(255), nullable=True)  # 用户背景图片
    avatar = db.Column(db.String(255), nullable=True)  # 头像图片
    email_public = db.Column(db.Boolean, default=False)  # 是否公开电子邮件

    # 密码修改历史
    password_changed_at = db.Column(db.DateTime, nullable=True)  # 最后一次修改密码的时间

    chat_background_color = db.Column(db.String(20), default='#ffffff')  # 默认白色背景
    chat_font_size = db.Column(db.String(5), default='14px')  # 默认字体大小


    def __init__(self, username, email, password, dob, role='user'):
        self.username = username
        self.email = email
        self.dob = dob
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.registered_on = datetime.utcnow()
        self.current_login_at = datetime.utcnow()  # 在用户创建时设置当前登录时间
        self.last_login_at = None  # 初次登录时没有上次登录时间
        self.total_login_count = 0  # 初始化登录次数
        self.last_login_at = datetime.utcnow()  # 初始化时设置 last_login_at

    def update_secure_fields_on_login(self, ip_addr: str) -> None:
        self.last_login_at = self.current_login_at
        self.current_login_at = datetime.utcnow()
        self.last_login_ip = self.current_login_ip
        self.current_login_ip = ip_addr
        self.total_login_count += 1
        db.session.commit()

    def verify_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def set_password_secure(self, password) -> None:
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.session.commit()

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def get_friends(self):
        return Friend.query.filter_by(user_id=self.id).all()

    def get_chats(self):
        return Chat.query.filter(
            (Chat.user1_id == self.id) | (Chat.user2_id == self.id)).all()


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    started_on = db.Column(db.DateTime, default=datetime.utcnow)

    # 添加唯一性约束
    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id', name='unique_chat'),)

    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])

    messages = db.relationship('Message', backref='chat', lazy='dynamic')

    def get_messages(self):
        return Message.query.filter_by(chat_id=self.id).all()


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(500), nullable=False)  # 限制消息长度
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])

class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),)

    user = db.relationship('User', foreign_keys=[user_id])
    friend = db.relationship('User', foreign_keys=[friend_id])


class GroupChat(db.Model):
    __tablename__ = 'group_chats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    def get_group_messages(group_chat_id):
        return GroupMessage.query.filter_by(group_chat_id=group_chat_id).order_by(GroupMessage.timestamp).all()

    def send_group_message(group_chat_id, sender_id, message_content):
        new_message = GroupMessage(
            group_chat_id=group_chat_id,
            sender_id=sender_id,
            message=message_content
        )
        db.session.add(new_message)
        db.session.commit()

    def get_group_members(group_chat_id):
        return GroupChatUser.query.filter_by(group_chat_id=group_chat_id).all()

    def get_user_groups(user_id):
        return GroupChatUser.query.filter_by(user_id=user_id).all()


class GroupChatUser(db.Model):
    __tablename__ = 'group_chat_users'

    id = db.Column(db.Integer, primary_key=True)
    group_chat_id = db.Column(db.Integer, db.ForeignKey('group_chats.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('group_chat_id', 'user_id', name='unique_group_membership'),)

    user = db.relationship('User', foreign_keys=[user_id])

class GroupMessage(db.Model):
    __tablename__ = 'group_messages'

    id = db.Column(db.Integer, primary_key=True)
    group_chat_id = db.Column(db.Integer, db.ForeignKey('group_chats.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
    group = db.relationship('GroupChat', foreign_keys=[group_chat_id])


class Emoji(db.Model):
    __tablename__ = 'emojis'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)  # 表情图片链接
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 上传者
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)



from models import User


def init_db():
    from app import create_app
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     username='admin',
                     role='admin',
                     dob='12/09/2001')
        db.session.add(admin)
        db.session.commit()

