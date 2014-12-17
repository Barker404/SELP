var status = "0";
var playerId = 0;
var choiceMade = false;

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
        choice = $(this).attr('move')
        chooseMove(choice)
    });
});

// AJAX calls required:
// 1. POST (?) trying to join a game
// 2. GET status
// 3. POST move choice

function startBattle() {
    alert("To be implemented");
    createPlayer();
}

// Uses jQuery ajax to get the ID for a new player
function createPlayer() {
    $.post('/battle/createPlayer/', function(data) {
        // Check response http status code
        playerId = parseInt(data);
    });
}
function doBattle() {
    // more looping
    // keep checking that game status, update screen when it changes
    // Every cycle might as well update the hp etc
    // When "status" actually changes, then show new parts of screen

    // There will be 3 states:
    // Choosing a move
    // Waiting for the other player/server calculation
    // Game finished
 
}

function chooseMove(choice) {
    $.getJSON('/battle/chooseMove/', 
        {'playerId': playerId, 'chosenMove': choice}, 
        function(data){
            // Check response http status code
    });
}

// Uses jQuery ajax to get the game status
function getUpdatedDetails() {
    $.getJSON('/battle/getBattleDetails/', {'playerId': playerId}, function(data){
       
        // Check response http status code
        displayUpdatedDetails(data);

        var oldStatus = status;
        status = data.battle.fields.status;

        if (oldStatus != status) {
            hideAll();
            switch(status) {
                // Display parts of the page based on the status
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
    });
}

// This updates the battle details on the page
function displayUpdatedDetails() {

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