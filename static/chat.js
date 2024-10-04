var socket = io();

socket.on('message', function(msg) {
    let messages = document.getElementById('messages');
    let newMessage = document.createElement('li');
    newMessage.textContent = msg;
    messages.appendChild(newMessage);
});

function sendMessage() {
    let input = document.getElementById('msg');
    let message = input.value;
    socket.send(message);
    input.value = '';
}