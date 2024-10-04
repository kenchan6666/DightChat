import eventlet
eventlet.monkey_patch()  # 确保在导入其他模块之前打补丁

from app import create_app, db  # 从你的应用导入 Flask 实例和数据库实例
from models import init_db  # 从你的 models 文件中导入初始化数据库的函数

def initialize_database():
    app = create_app()  # 创建 Flask 应用
    with app.app_context():  # 确保在应用上下文中
        init_db()  # 初始化数据库
        print("Database initialized successfully!")

if __name__ == '__main__':
    initialize_database()
