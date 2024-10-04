import os
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_user, current_user, login_required
from werkzeug.utils import secure_filename

from extensions import db
from models import User

user_blueprint = Blueprint('user', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#debugging
# print("Template folder:",user_blueprint.template_folder)

@login_required
@user_blueprint.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        user_data = {
            'username': current_user.username,
            'email': current_user.email,
            'avatar': current_user.avatar,
            'birthday': current_user.birthday.strftime('%Y-%m-%d') if current_user.birthday else None,
            'registered_on': current_user.registered_on.strftime('%Y-%m-%d')
        }
        return jsonify(user_data)
    return render_template('user/account.html',current_user=current_user)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    from app import create_app

    app = create_app()

    if request.method == 'POST':
        data = request.get_json()  # 获取JSON格式的请求数据
        username = data.get('username')
        password = data.get('password')

        # 查找用户，假设根据用户名或邮箱进行查询
        user = User.query.filter((User.username == username) | (User.email == username)).first()

        if user and user.verify_password(password):
            # 登录用户
            login_user(user)

            # 更新用户的登录信息
            user.last_login = user.current_login_at
            user.current_login_at = datetime.utcnow()
            user.last_login_ip = user.current_login_ip or request.remote_addr
            user.current_login_ip = request.remote_addr
            user.total_login_count += 1
            db.session.commit()

            # 记录日志
            app.logger.info(f"User {user.username} logged in at {user.current_login_at} from {request.remote_addr}")

            # 返回成功的JSON响应
            return jsonify({'success': True, 'message': '登录成功！'})

        else:
            # 登录失败，返回错误消息
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    # 如果是GET请求，返回登录页面
    return render_template('user/login.html')

@user_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()  # 获取前端发送的 JSON 数据

        # 从 JSON 中获取数据
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        birthday = data.get('birthday')

        # 基础验证逻辑
        if not username or not email or not password or not birthday:
            return jsonify({'success': False, 'message': '所有字段都必须填写'}), 400

        # 检查邮箱是否已注册
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': '该邮箱已注册'}), 400

        # 创建新用户（密码应使用哈希存储）
        new_user = User(username=username, email=email, password=password, dob=birthday)

        # 将用户保存到数据库
        db.session.add(new_user)
        db.session.commit()

        # 返回成功响应
        return jsonify({'success': True, 'message': '注册成功！'}), 200

    return render_template('user/register.html')

@user_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('user/reset_password.html')

@user_blueprint.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():

    if request.method == 'POST':
        # 处理头像上传
        avatar_file = request.files.get('avatar')
        if avatar_file and allowed_file(avatar_file.filename):
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join('uploads/avatars', filename)
            avatar_file.save(avatar_path)
            current_user.avatar = avatar_path  # 假设你的 User 模型有 avatar 字段

        # 处理用户名更新
        new_username = request.form.get('username')  # 从 form data 中获取
        if new_username:
            current_user.username = new_username

        # 处理背景颜色更新
        new_background_color = request.form.get('background_color')  # 从 form data 中获取
        if new_background_color:
            current_user.custom_background_color = new_background_color

        # 提交数据库更改
        db.session.commit()

        return jsonify({'success': True, 'message': '设置已更新！'})

    # 渲染设置页面（GET请求时）
    return render_template('user/setting.html',
                           avatar=current_user.avatar,
                           username=current_user.username)