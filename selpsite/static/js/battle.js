var status;
var playerId;

// Enum for battle status values 
StatusEnum = {
    WAITING_FOR_PLAYER : 1,
    WAITING_FOR_CHOICE : 2,
    CALCULATING : 3,
    FINISHED : 4
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
            return 'Calculating results');
            break;
        case StatusEnum.FINISHED:
            return 'Battle finished';
            break;
    }
}

// Start a battle
$(document).ready(function() {
    $('#startBattle').click(function() {
        startBattle();
    });
    $('#getStatus').click(function() {
        playerIda = $("#playerId").val();
        getUpdatedStatus();
    });
});

// AJAX calls required:
// 1. POST (?) trying to join a game
// 2. GET status
// 3. POST move choice

function startBattle() {
    alert("To be implemented");
    // gonna loop
    // Try to join a game, keep trying if it fails
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

// Uses jQuery ajax to get the game status
function getUpdatedDetails() {
    $.get('/battle/getBattleStatus/', {'playerId': playerId}, function(data){
       
        displayUpdatedStatus(data)

        var oldStatus = status;
        status = data.battle.fields.status;
        if (oldStatus != status) {
            switch(status) {
                case StatusEnum.WAITING_FOR_PLAYER:
                    return 'Waiting for another player';
                    break;
                case StatusEnum.WAITING_FOR_CHOICE:
                    return 'Waiting for player choices';
                    break;
                case StatusEnum.CALCULATING:
                    return 'Calculating results');
                    break;
                case StatusEnum.FINISHED:
                    return 'Battle finished';
                    break;
            }
        }


    });
}

// Below functions display the correct parts of the page for each
// point in a battle

function displayUpdatedDetails() {

}

function displayWaitingForChoice() {

}
// This function is for the display when the player has made a choice,
// but the game is still "waiting for player choice" - the other
// player has not made a choice yet
function displayWaitingForOtherChoice() {
    
}
function displayCalculating() {
    
}
function displayFinished() {
    
}
