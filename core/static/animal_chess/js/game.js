const CHAT_ACTION = 'chat';
const JOIN_ACTION = 'join';
const READY_ACTION = 'ready';
const SELECT_ACTION = 'select';
const MOVE_ACTION = 'move';
const RECONNECT_ACTION = 'reconnect';
const iconPath = "/static/icon/";

let myPlayerName = "";
let myPlayerId = "";
let player1Id;
let player2Id;
let myStatus;

let chatSocket = null;
let chatLog = null;
let message = "";
let gameStarted = false;
let movableCoordinates = [];
let stagingPiece = null;

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
        + '/ws/animal-chess-game/'
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
                updateTurn(data);
                updateChat(data);
                break;
            case 'select':
                clearMovablePiece();
                clearSelected();
                if (data.movable) {
                    updateMovagblePiece(data);
                    updateSelected(data);
                }
                updateBoard(data);
                updateTurn(data);
                break;
            case 'move':
                clearSelected();
                clearMovablePiece();
                updateBoard(data);
                updateTurn(data);
                break;
            case 'Wins!':
                gameStarted = false;
                clearSelected();
                clearMovablePiece();
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

    $(".piece").on('click', function () {
        message = {
            'player_id': myPlayerId,
            'player_name': myPlayerName,
            'gameID': gameId,
            'coordinate': this.id,
        };
        if ($(this).hasClass("hidden") || movableCoordinates.length === 0) {
            message['action'] = SELECT_ACTION;
            stagingPiece = this.id
        } else {
            message['action'] = MOVE_ACTION;
            message['src_coordinate'] = stagingPiece;
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
            'player_name': myPlayerName,
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

function updateTurn(data) {
    if (data.turn === player1Id) {
        $("#player1-name").addClass("player1");
        $("#player2-name").removeClass("player2");
    } else {
        $("#player2-name").addClass("player2");
        $("#player1-name").removeClass("player1");

    }
}

function updateBoard(data) {
    let board = data.board;
    for (const row in board) {
        for (const col in board[row]) {
            const coordinate = getCoordinate(row, col);
            let piece = $("#" + coordinate);
            piece.children().removeClass("player1");
            piece.children().removeClass("player2");
            if (board[row][col].piece === "empty") {
                piece.children().attr("src", iconPath + "empty.png");
            } else if (board[row][col].piece === "hidden") {
                piece.addClass("hidden");
                piece.children().attr("src", iconPath + "hidden.png")
            } else {
                piece.children().attr("src", iconPath + board[row][col].piece + ".png");
                piece.removeClass("hidden");
                if (board[row][col].player === player1Id) {
                    piece.children().addClass("player1");
                } else {
                    piece.children().addClass("player2");
                }
            }
        }
    }
}

function updateMovagblePiece(data) {
    clearMovablePiece();
    movableCoordinates = data.movable_coordinates;
    for (const idx in movableCoordinates) {
        const coordinate = getCoordinate(movableCoordinates[idx][0], movableCoordinates[idx][1]);
        $("#" + coordinate).css("opacity", 0.5);
    }
}

function updateSelected(data) {
    const coordinate = getCoordinate(data.coordinate[0], data.coordinate[1]);
    $("#" + coordinate).children().addClass("selected-card")
}

function clearSelected() {
    $(".selected-card").removeClass("selected-card");
}

function clearMovablePiece() {
    for (const idx in movableCoordinates) {
        const coordinate = getCoordinate(movableCoordinates[idx][0], movableCoordinates[idx][1]);
        $("#" + coordinate).css("opacity", 1);
    }
    movableCoordinates = [];
}

function getCoordinate(x, y) {
    return x + "-" + y;
}

function joinPlayer(player) {
    $(".player2-container").append("<div id=\"player2-name\" class=\"player-name inline-block\">" + player + "</div>");
}

function finishGame(data) {
    $("#win-message").html(data.winner + " Won!!! Congratulations!");
    $("#id01").css("display", "block")
}