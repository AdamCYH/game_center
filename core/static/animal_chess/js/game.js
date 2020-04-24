const CHAT_ACTION = 'chat';
const JOIN_ACTION = 'join';
const READY_ACTION = 'ready';


$(document).ready(function () {

    const gameId = $("#game-id").html();
    const player = $("#player-name").html();
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/animal-chess-game/'
        + gameId
        + '/'
    );
    chatSocket.onopen = function (e) {
        chatSocket.send(JSON.stringify({
            'action': JOIN_ACTION,
            'player': player
        }));
    };


    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        switch (data.action) {
            case 'ready':
                break;
            case 'move':
                break;
        }
        document.querySelector('#chat-log').value += (data.message + '\n');
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    $(".ready").on('click', function () {
        chatSocket.send(JSON.stringify({
            'action': READY_ACTION,
            'player': player,
            'gameID': gameId
        }));
    });

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
            'action': CHAT_ACTION,
            'player': player,
            'gameID': gameId
        }));
        messageInputDom.value = '';
    };
});
