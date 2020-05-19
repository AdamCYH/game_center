const CHAT_ACTION = 'chat';
const JOIN_ACTION = 'join';
const READY_ACTION = 'ready';
const ESTABLISH_ACTION = 'establish';

const iconPath = "/static/five_in_a_row/img/";

let gameStarted = false;

$(document).ready(function () {
    const gameId = $("#game-id").html();
    chatLog = $("#chat-log");

    myPlayerName = $("#my-player-name").html();
    myPlayerId = $("#my-player-id").html();
    player1Id = $("#player1-id").html();
    player2Id = $("#player2-id").html();
    myStatus = $("#my-status").html();

    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/five-in-a-row-game/'
        + gameId
        + '/'
    );

    chatSocket.onopen = function (e) {
        if (myStatus === "reconnect") {
            message = {
                'action': RECONNECT_ACTION,
                'player_id': myPlayerId,
                'player_name': myPlayerName,
                'gameID': gameId
            };
            send(message);
        } else {
            message = {
                'action': JOIN_ACTION,
                'player_id': myPlayerId,
                'player_name': myPlayerName,
                'gameID': gameId
            };
            send(message);
        }
    };


    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        switch (data.action) {
            case 'chat':
                updateChat(data);
                break;
            case 'ready':
                updateChat(data);
                updateReadyStatus(data);
                break;
            case 'join':
                if (myPlayerId !== data.player_id) {
                    joinPlayer(data.player_name);
                }
                updateChat(data);
                updateBoard(data);
                break;
            case 'reconnect':
                gameStarted = true;
                updateChat(data);
                updateBoard(data);
                updateTurn(data);
                break;
            case 'start game':
                gameStarted = true;
                $(".ready").remove();
                updatePieceColor(data);
                updateTurn(data);
                updateChat(data);
                break;
            case 'establish':
                updateBoard(data);
                updateTurn(data);
                break;
            case 'Wins!':
                gameStarted = false;
                updateBoard(data);
                finishGame(data);
                break;
        }


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

    $(".grid").on('click', function () {
        message = {
            'player_id': myPlayerId,
            'player_name': myPlayerName,
            'gameID': gameId,
            'coordinate': this.id,
            'action': ESTABLISH_ACTION
        };
        if (gameStarted) {
            send(message);
        }
    });

    $(".ready").on('click', function () {
        message = {
            'action': READY_ACTION,
            'player_id': myPlayerId,
            'player_name': myPlayerName,
            'gameID': gameId
        };
        send(message);
    });

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = $('#chat-message-input');
        if (!messageInputDom.val()) {
            return
        }
        message = {
            'message': messageInputDom.val(),
            'action': CHAT_ACTION,
            'player_id': myPlayerId,
            'player_name': myPlayerName,
            'gameID': gameId
        };
        send(message);
        messageInputDom.val("");
    };

});

function send(message) {
    chatSocket.send(JSON.stringify(message));
}

function updateChat(data) {
    chatLog.val(chatLog[0].value += (data.message + '\n'));
    chatLog.scrollTop(chatLog[0].scrollHeight + 30);
}

function updateReadyStatus(data) {
    const readyBtn = $("#player-" + data.player_id);
    readyBtn.html("Ready");
    readyBtn.css("background-color", "#bdf0c3");

}

function joinPlayer(player) {
    $(".player2-container").append("<div class=\"player-piece-info inline-block\"><img class=\"player-piece\" id=\"player2-piece\"></div>");
    $(".player2-container").append("<div id=\"player2-name\" class=\"player-name inline-block\">" + player + "</div>");
}

function updatePieceColor(data) {
    if (data[player1Id] === "Black") {
        $("#player1-piece").attr('src', "/static/five_in_a_row/img/black-piece.png");
        $("#player2-piece").attr('src', "/static/five_in_a_row/img/white-piece.png");
    } else {
        $("#player1-piece").attr('src', "/static/five_in_a_row/img/white-piece.png");
        $("#player2-piece").attr('src', "/static/five_in_a_row/img/black-piece.png");
    }
}

function updateTurn(data) {
    if (data.turn === player1Id) {
        $("#player1-piece").addClass("piece-lg");
        $("#player2-piece").removeClass("piece-lg");
    } else {
        $("#player2-piece").addClass("piece-lg");
        $("#player1-piece").removeClass("piece-lg");

    }
}

function updateBoard(data) {
    let board = data.board;
    for (const row in board) {
        for (const col in board[row]) {
            const coordinate = getCoordinate(row, col);
            let piece = $("#" + coordinate);
            if (board[row][col].piece === "Black") {
                piece.empty();
                piece.append("<img class='piece' src='" + iconPath + "black-piece.png" + "'>");
            } else if (board[row][col].piece === "White") {
                piece.empty();
                piece.append("<img class='piece' src='" + iconPath + "white-piece.png" + "'>");
            }
        }
    }
}

function getCoordinate(x, y) {
    return x + "-" + y;
}