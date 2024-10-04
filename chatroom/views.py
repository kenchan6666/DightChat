from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_socketio import send, SocketIO

from app import socketio

chatroom_blueprint = Blueprint('chatroom', __name__, template_folder='templates')

#debugging
print("Template folder:",chatroom_blueprint.template_folder)

@chatroom_blueprint.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    return render_template('chatroom/chat.html')


def invite():
    return

def createchatroom():
    return


# 处理消息
@socketio.on('message')
def handle_message(msg):
    print(f'Message: {msg}')
    send(msg, broadcast=True)