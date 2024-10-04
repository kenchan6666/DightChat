from logging.handlers import RotatingFileHandler
import logging
import eventlet
eventlet.monkey_patch()

import os

from flask import Flask, render_template
from dotenv import load_dotenv
from flask_socketio import SocketIO, send
from flask_login import login_required, current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

from extensions import db



socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    socketio.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    log_path = 'app.log'

    handler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=10)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['ENCRYPTION_KEY'] = os.getenv('ENCRYPTION_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
    app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads/avatars'  # 你可以选择适合你的文件夹路径e

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)  # 这里将 app 传递给 db

    with app.app_context():
        db.create_all()

    from chatroom.views import  chatroom_blueprint
    from user.view import user_blueprint

    app.register_blueprint(chatroom_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    # 主页

    @app.route('/')
    def index():
        return render_template('base.html')

    # 处理消息
    @socketio.on('message')
    def handle_message(msg):
        print(f'Message: {msg}')
        send(msg, broadcast=True)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, use_reloader=False, log_output=True)