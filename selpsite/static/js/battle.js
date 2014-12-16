// Start a battle
$(document).ready(function() {
    $('#startBattle').click(function() {
        startBattle()
    });
});

// Get an update
$(document).ready(function() {
    $('#getStatus').click(function() {
        id = $('#playerId').val()
        $.get('/battle/getBattleStatus/', {playerId: id}, function(data){
           alert(data.battle.fields.status)
           status = JSON.parse(data);
           alert(status.battle.fields.status);
        });
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