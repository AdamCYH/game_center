const CHAT_ACTION = 'chat';
const JOIN_ACTION = 'join';
const READY_ACTION = 'ready';
const SELECT_ACTION = 'select';
const MOVE_ACTION = 'move';
const player1Id = "1";
const player2Id = "2";

let playerName = "";
let myPlayerId = "";

let chatSocket = null;
let message = "";
let gameStarted = false;
let movableCoordinates = [];
let stagingPiece = null;

$(document).ready(function () {
    const gameId = $("#game-id").html();
    playerName = $("#player-name").html();
    myPlayerId = $("#player-id").html();

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
            'player_id': myPlayerId,
            'player_name': playerName,
            'gameID': gameId
        };
        send(message);
    };


    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        switch (data.action) {
            case 'ready':
                break;
            case 'join':
                if (myPlayerId !== data.player_id) {
                    joinPlayer(data.player_name);
                }
                break;
            case 'start game':
                gameStarted = true;
                break;
            case 'select':
                if (data.movable) {
                    updateMovagblePiece(data);
                }
                updateBoard(data);
                break;
            case 'move':
                updateBoard(data);
                clearMovablePiece();
                break;
        }
        updateTurn(data);
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
            'player_id': myPlayerId,
            'player_name': playerName,
            'gameID': gameId,
            'coordinate': this.id,
        };
        if (movableCoordinates.length > 0) {
            message['action'] = MOVE_ACTION;
            message['src_coordinate'] = stagingPiece;
        } else {
            message['action'] = SELECT_ACTION;
            stagingPiece = this.id
        }
        clearMovablePiece();
        if (gameStarted) {
            send(message);
        }
    });

    $(".ready").on('click', function () {
        message = {
            'action': READY_ACTION,
            'player_id': myPlayerId,
            'player_name': playerName,
            'gameID': gameId
        };
        send(message);
    });

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = $('#chat-message-input');
        message = {
            'message': messageInputDom.val(),
            'action': CHAT_ACTION,
            'player_id': myPlayerId,
            'player_name': playerName,
            'gameID': gameId
        };
        send(message);
        messageInputDom.val("");
    };
});

function send(message) {
    chatSocket.send(JSON.stringify(message));
}

function updateTurn(data) {
    if (data.turn === player1Id) {
        $("#player1-turn").css("background-color", "blue");
        $("#player2-turn").css("background-color", "");
    } else {
        $("#player2-turn").css("background-color", "red");
        $("#player1-turn").css("background-color", "");
    }
}

function updateBoard(data) {
    let board = data.board;
    for (const row in board) {
        for (const col in board[row]) {
            const coordinate = getCoordinate(row, col);
            let piece = $("#" + coordinate);
            if (board[row][col].piece === "empty") {
                piece.html("");
                piece.css("border", "solid grey 2px");
            } else if (board[row][col].piece === "hidden") {
                piece.html("#####");
            } else {
                piece.html(board[row][col].piece);
                if (board[row][col].player === player1Id) {
                    piece.css("border", "solid blue 2px");
                } else {
                    piece.css("border", "solid red 2px");
                }
            }
        }
    }
}

function updateMovagblePiece(data) {
    clearMovablePiece();
    movableCoordinates = data.movable_coordinates;
    for (const idx in movableCoordinates) {
        const coordinate = getCoordinate(movableCoordinates[idx].x, movableCoordinates[idx].y);
        $("#" + coordinate).css("background-color", "green");
    }
}

function clearMovablePiece() {
    for (const idx in movableCoordinates) {
        const coordinate = getCoordinate(movableCoordinates[idx].x, movableCoordinates[idx].y);
        $("#" + coordinate).css("background-color", "");
    }
    movableCoordinates = [];
}

function getCoordinate(x, y) {
    return x + "-" + y;
}

function joinPlayer(player) {
    $(".player2-container").append("<div id=\"player2-name\">" + player + "</div>");
}