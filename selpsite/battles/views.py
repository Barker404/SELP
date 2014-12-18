import json
from django.http import (
                        HttpResponse, 
                        HttpResponseBadRequest, 
                        HttpResponseForbidden
                        )
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from models import Battle, Player, Move
from django.core import serializers

# View for displaying the start battle page
def battleView(request):
    # Redirect to login page if user is not logged in
    if not request.user.is_authenticated():
        return redirect('/users/login/?next=%s' % request.path)
    else:
        return render(request, 'battles/startBattle.html')

# View for creating a player object in preparation for starting a 
# battle
def ajaxCreatePlayerView(request):
    # Check user is logged in
    if (not request.user.is_authenticated()):
        return HttpResponseForbidden()
    # and sending a POST request
    if (not request.method == 'POST'):
        return HttpResponseBadRequest()

    player = Player.objects.create(user=request.user);
    return HttpResponse(player.pk);

# View for actually starting a battle via ajax
def ajaxStartBattleView(request):
    # Check user is logged in
    if (not request.user.is_authenticated()):
        return HttpResponseForbidden()
    # and sending a POST request
    if (not request.method == 'POST'):
        return HttpResponseBadRequest()
    # With a playerId attatched
    if (not 'playerId' in request.POST):
        return HttpResponseBadRequest()

    playerId = request.POST['playerId']
    # Check the playerId they sent exists
    player = get_object_or_404(Player, pk=playerId)
    # Check the user is logged in as the user of the sent player
    if (player.user != request.user):
        return HttpResponseForbidden()
    # and that their player is not in a battle
    if (player.isInBattle()):
        return HttpResponseBadRequest()

    # Try to join/create a battle
    success = joinBattle(player)
    # Respond with success
    if (success):
        return HttpResponse("success")
    else:
        return HttpResponse("failure")

# View for choosing a move to use via ajax
def ajaxChooseMoveView(request):
    # Check user is logged in
    if (not request.user.is_authenticated()):
        return HttpResponseForbidden()
    # and sending a POST request
    if (not request.method == 'POST'):
        return HttpResponseBadRequest()
    # With a playerId and moveChoice attatched
    if (not 'playerId' in request.POST or 
        not 'moveChoice' in request.POST):
        return HttpResponseBadRequest()

    playerId = request.POST['playerId']
    moveChoice = request.POST['moveChoice']
    # Check move sent is valid
    valid = False
    for choice in Move.MOVE_CHOICES:
        if (choice[0] == moveChoice):
            valid = True
            break
    if (not valid):
        return HttpResponseBadRequest()
        
    # Check the playerId they sent exists
    player = get_object_or_404(Player, pk=playerId)
    # Check the user is logged in as the user of the sent player
    if (player.user != request.user):
        return HttpResponseForbidden()
    # and that their player is in a battle
    if (not player.isInBattle()):
        return HttpResponseBadRequest()

    success = chooseMove(player, moveChoice)
    if (success):
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def ajaxGetBattleDetailsView(request):
    # Check user is logged in
    if (not request.user.is_authenticated()):
        return HttpResponseForbidden()
    # and sending a GET request
    if (not request.method == 'GET'):
        return HttpResponseBadRequest()
    # With a playerId attatched
    if (not 'playerId' in request.GET):
        return HttpResponseBadRequest()

    playerId = request.GET['playerId']
    # Check the playerId they sent exists
    player = get_object_or_404(Player, pk=playerId)
    # Check the user is logged in as the user of the sent player
    if (player.user != request.user):
        return HttpResponseForbidden()
    # and that their player is in a battle
    if (not player.isInBattle()):
        return HttpResponseBadRequest()

    # Serialize the data
    # We serialize the objects in lists because the django 
    # serialization requires a list of objects
    battleData = serializers.serialize('json', [player.getBattle(),])
    playerData = serializers.serialize('json', [player,])
    if (not player.opponent is None):
        opponentData = serializers.serialize('json', [player.opponent,])

    # Add to dictionary
    # Since we want to output individual objects within a single 
    # larger object, we know reload each object and take the first item 
    # from the single-item list we made earlier
    responseData = {}
    responseData['battle'] = json.loads(battleData)[0]
    responseData['player'] = json.loads(playerData)[0]
    if (not player.opponent is None):
        responseData['opponent'] = json.loads(opponentData)[0]
    else:
        responseData['opponent'] = None

    # Add the players' usernames
    responseData['player']['username'] = player.user.username
    if (not player.opponent is None):
        responseData['opponent']['username'] = player.opponent.user.username

    # Finally, dump the full object
    serializedData = json.dumps(responseData)
    return HttpResponse(serializedData, 
                        content_type="application/json")


# Will try to find a game/make one and join it
# Returns true if the player is now in a battle, else false
# If true the player should wait for another to join the game
# If false, the player should retry until success
def joinBattle(player):
    # Get all battles with space
    spaces = Battle.objects.filter(Q(player1__isnull=True,
                                     player2__isnull=False,
                                     status=Battle.WAITING_FOR_PLAYER) |
                                   Q(player1__isnull=False,
                                     player2__isnull=True,
                                     status=Battle.WAITING_FOR_PLAYER))

    if (spaces):
        # (sort-of) prevent other players trying to join
        # Still obvious race condition, might need to fix later
        game = spaces.first()
        game.status = Battle.CALCULATING
        game.save()

        # Model method handles actually joining
        success = game.tryAddPlayer(player)
        if (success):
            # Reset the status
            if (bool(game.player1) and bool(game.player2)):
                game.status = Battle.WAITING_FOR_CHOICE
            else:
                game.status = Battle.WAITING_FOR_PLAYER
            game.save()
            return True
        else:
            # Need to properly define what to do with status here
            # In theory if the join was unsuccessful because there's 
            # another joined player, they should set the status 
            # afterwards.
            return False
    else:
        # No spaces in existing games, so make a new one!
        Battle.objects.create(player1=player)
        return True

def chooseMove(player, move):
    # Most of the checks in this function are done in the calling view
    # But we do them anyway, just to be sure 
    # (or in case it's called from somewhere else)

    # Check the player is in a battle
    playerNo = player.getPlayerNumber()
    if (playerNo == 0):
        return False
    battle = player.getBattle()

    # Check that the battle is waiting for the player to choose a 
    # move
    if (battle.status != battle.WAITING_FOR_CHOICE or
        not player.currentMove is None):
        return False

    # Check move is valid
    valid = False
    for choice in Move.MOVE_CHOICES:
        if (choice[0] == move):
            valid = True
            break
    if (not valid):
        return False

    moveMade = player.addMove(move)

    success = True
    # Re-get battle from db?
    if (not battle.player1.currentMove is None and 
        not battle.player2.currentMove is None):
        battle.status = Battle.CALCULATING
        battle.save()
    
        success = calculateTurn(battle)
    return success

# Defines how much damage is dealt to each party for a particular move 
# combination
# damages[p1Move][p2Move] = (p1damage, p2damage)
damages = {
    'R': { 'R': (00,00), 'P': (30,00), 'S': (00,30)},
    'P': { 'R': (00,30), 'P': (00,00), 'S': (30,00)},
    'S': { 'R': (30,00), 'P': (00,30), 'S': (00,00)}
}

def calculateDamage(move1, move2):
    return damages[move1][move2]

def calculateTurn(battle):

    # Check battle is ready for calculating
    if (battle.player1 is None or 
        battle.player2 is None or
        battle.player1.currentMove is None or
        battle.player2.currentMove is None or
        battle.status != Battle.CALCULATING):
        return False

    player1 = battle.player1
    player2 = battle.player2

    move1 = player1.currentMove
    move2 = player2.currentMove
    # Calculate damage - This will get more sophisticated when 
    # battle system is expanded


    damage1, damage2 = calculateDamage(move1.moveUsed, move2.moveUsed)

    player1.hp -= damage1
    player2.hp -= damage2

    player1.save()
    player2.save()

    if (player1.hp <= 0 or player2.hp <= 0):
        # Someone has died, battle is over
        battle.status = Battle.FINISHED
        # Set the winner
        if (player1.hp > 0):
            battle.winner = player1
        elif (player2.hp > 0):
            battle.winner = player2
        else:
            battle.winner = tieBreak(player1, player2)

        # If somebody won (it was not a draw) update wins/losses
        if (not battle.winner is None):
            # Loser
            if (battle.winner == player1):
                player2.user.profile.addLoss()
            else:
                player1.user.profile.addLoss()
            # Winner
            battle.winner.user.profile.addWin()

            player1.user.profile.save()
            player2.user.profile.save()
    else:
        # Reset moves
        player1.currentMove = None
        player2.currentMove = None
        player1.save()
        player2.save()

        # Prepare battle for next input
        battle.turnNumber += 1
        battle.status = Battle.WAITING_FOR_CHOICE

    # Finally, save battle so clients know we're done
    battle.save()
    return True

# Function to break ties between two players
# Called in the case where both players reach 0 hp at the same time
# Can return None to define a draw
def tieBreak(player1, player2):
    return None
