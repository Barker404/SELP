from django.shortcuts import render
from django.db.models import Q
from models import Battle

def startBattleView(request):
    return render(request, 'battles/startBattle.html')

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
    # Check the player is in a battle
    if (not player.player1 is None):
        battle = player.player1
        playerNo = 1
    elif (not player.player2 is None):
        battle = player.player2
        playerNo = 2
    else:
        return False

    # Check that the battle is waiting for the player to choose a 
    # move
    if (battle.status != battle.WAITING_FOR_CHOICE or
        not player.currentMove is None):
        return False

    moveMade = player.addMove(move)

    # Re-get battle from db?
    if (not battle.player1.currentMove is None and 
        not battle.player2.currentMove is None):
    battle.status = Battle.CALCULATING
    battle.save()
    
    success = True
    # success = calculateTurn(battle)
    return success


