const CHAT_ACTION = 'chat';
const JOIN_ACTION = 'join';
const READY_ACTION = 'ready';
const SELECT_ACTION = 'select';
let chatSocket = null;
let message = "";
let gameStarted = false;

$(document).ready(function () {

    const gameId = $("#game-id").html();
    const player = $("#player-name").html();
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/animal-chess-game/'
        + gameId
        + '/'
    );
    chatSocket.onopen = function (e) {
        message = {
            'action': JOIN_ACTION,
            'player': player,
            'gameID': gameId
        };
        send(message);
    };


    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        switch (data.action) {
            case 'ready':
                break;
            case 'start game':
                gameStarted = true;
                break;
            case 'select':
                updateBoard(data.board)
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

    $(".piece").on('click', function () {
        message = {
            'action': SELECT_ACTION,
            'player': player,
            'gameID': gameId,
            'coordinate': this.id,
        };
        if (gameStarted) {
            send(message);
        }
    });

    $(".ready").on('click', function () {
        message = {
            'action': READY_ACTION,
            'player': player,
            'gameID': gameId
        };
        send(message);
    });

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = $('#chat-message-input');
        message = {
            'message': messageInputDom.val(),
            'action': CHAT_ACTION,
            'player': player,
            'gameID': gameId
        };
        send(message);
        messageInputDom.val("");
    };
});

function send(message) {
    chatSocket.send(JSON.stringify(message));
}

function updateBoard(coordinates) {
    for (let row in coordinates) {
        for (let col in coordinates[row]) {
            const coordinate = row + "-" + col;
            $("#" + coordinate).html(coordinates[row][col].piece)
        }
    }
}