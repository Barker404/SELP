var status = "0";
var turnNumber = 0;
var playerId = 0;
var choiceMade = false;
// How often to update information (ms)
var UPDATE_PERIOD = 1000;
// Timer that makes the update function run periodically
var timer;

// Enum for battle status values 
StatusEnum = {
    WAITING_FOR_PLAYER : "1",
    WAITING_FOR_CHOICE : "2",
    CALCULATING : "3",
    FINISHED : "4"
}

function statusToString(status) {
    switch(status) {
        case StatusEnum.WAITING_FOR_PLAYER:
            return 'Waiting for another player';
            break;
        case StatusEnum.WAITING_FOR_CHOICE:
            return 'Waiting for player choices';
            break;
        case StatusEnum.CALCULATING:
            return 'Calculating results';
            break;
        case StatusEnum.FINISHED:
            return 'Battle finished';
            break;
        default: 
            return "Unknown Status";
    }
}

$(document).ready(function() {
    // Start a battle
    $('#startBattle').click(function() {
        startBattle();
    });
    $('.move').click(function() {
        choice = $(this).attr('choice')
        chooseMove(choice)
    });
});

function startBattle() {
    createPlayer();
}

// Uses jQuery ajax to get the ID for a new player
function createPlayer() {
    $.post('/battle/createPlayer/', function(data) {
        // Check response http status code
        playerId = parseInt(data);
        tryJoinBattle();
    });
}

function tryJoinBattle() {
    $.post('/battle/startBattle/', {'playerId': playerId}, function(data){
            // Check response http status code
            if (data == "success") {
                time = setInterval(getUpdatedDetails, UPDATE_PERIOD);
            } else {
                alert("bad join attempt");
                tryJoinBattle();
            }
    });
}

function chooseMove(choice) {
    $.post('/battle/chooseMove/', 
        {'playerId': playerId, 'moveChoice': choice}, 
        function(data){
            // Check response http status code
            choiceMade = true;
            displayNewPageParts();
    });
}

// Uses jQuery ajax to get the game status
function getUpdatedDetails() {
    $.getJSON('/battle/getBattleDetails/', {'playerId': playerId}, function(data){
       
        // Check response http status code
        displayUpdatedDetails(data);

        // Check both the status AND the turn number
        // During th battle, the status will almost always be
        // "Waiting for player choice"
        // But we can tell if a turn has processed and we need to
        // input again by the turn number
        var oldStatus = status;
        status = data.battle.fields.status;
        var oldTurnNumber = turnNumber;
        turnNumber = Number(data.battle.fields.turnNumber);
        if (oldStatus != status) {
            displayNewPageParts();
        }
        if (turnNumber != oldTurnNumber) {
            choiceMade = false;
            displayNewPageParts();
        }
    });
}


// Display parts of the page based on the status
function displayNewPageParts() {
    hideAll();
    switch(status) {
        case StatusEnum.WAITING_FOR_PLAYER:
            displayWaitingForPlayer();
            break;
        case StatusEnum.WAITING_FOR_CHOICE:
            if (!choiceMade) {
                displayWaitingForChoice();
            } else {
                displayWaitingForOtherChoice();
            }
            break;
        case StatusEnum.CALCULATING:
            displayCalculating();
            break;
        case StatusEnum.FINISHED:
            displayFinished();
            break;
        default:
            displayError();
    }

}

// This updates the battle details on the page
function displayUpdatedDetails(data) {
    // SHow the player's info
    if (data.player != null) {
        $("#playerHp").text(data.player.fields.hp);
        $("#playerName").text(data.player.username);
        if (data.player.lastMove != null) {
            $("#playerLastMove").text(data.player.lastMove);
        }
    }
    // Show the opponent's info
    if (data.opponent != null) {
        $("#opponentHp").text(data.opponent.fields.hp);
        $("#opponentName").text(data.opponent.username);
        if (data.opponent.lastMove != null) {
            $("#opponentLastMove").text(data.opponent.lastMove);
        }
    }
    // Show general info
    if (data.battle != null) {
        $("#turnNumber").text(data.battle.fields.turnNumber);
        
        // Translate distance into words
        distance = data.battle.fields.distance;
        if (distance == 1) {
            distanceWords = "Short Range";
        }
        else if (distance == 2) {
            distanceWords = "Mid Range";
        }
        else if (distance == 3) {
            distanceWords = "Long Range";
        }
        else {
            distanceWords = "Unknown Range";
        }
        $("#distance").text(distanceWords);

        // Displays the winner by comparing the winner (a player pk)
        // to both players' pks
        if (data.battle.fields.winner == null) {
            $("#winnerName").text("Nobody");
        }
        else if (data.battle.fields.winner == data.player.pk) {
            $("#winnerName").text("You");
        } 
        else if (data.opponent != null &&
                 data.battle.fields.winner == data.opponent.pk) {
            $("#winnerName").text(data.opponent.username);
        }
        else {
            $("#winnerName").text("I don't know who");
        }
    }
}

// Below functions display the correct parts of the page for each
// point in a battle

// Hides all of the parts of the page which can be shown with 
// below functions
function hideAll() {
    $("#preBattle").hide();
    $("#joining").hide();
    $("#moveChoice").hide();
    $("#waiting").hide();
    $("#calculating").hide();
    $("#finished").hide();
    $("#error").hide();
}

function displayPreBattle() {
    $("#preBattle").show();
}
function displayWaitingForPlayer() {
    $("#joining").show();
}
function displayWaitingForChoice() {
    $("#moveChoice").show();
}
// This function is for the display when the player has made a choice,
// but the game is still "waiting for player choice" - the other
// player has not made a choice yet
function displayWaitingForOtherChoice() {
    $("#waiting").show();
}
function displayCalculating() {
    $("#calculating").show();
}
function displayFinished() {
    $("#finished").show();
}
function displayError() {
    $("#error").show();
}

// Code below is for avoiding cross-site request forgery by adding
// the crsf token to ajax requests

// Taken from the django website at:
// https://docs.djangoproject.com/en/1.6/ref/contrib/csrf/#ajax

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});