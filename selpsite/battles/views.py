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
    spaces = Battle.objects.filter(Q(player1__isnull=True,
                                     player2__isnull=False,
                                     status=WAITING_FOR_PLAYERS) |
                                   Q(player1__isnull=False,
                                     player2__isnull=True,
                                     status=WAITING_FOR_PLAYERS))

    if (spaces):
        # (sort-of) prevent other players trying to join
        # Obvious race condition, might need to fix later
        game = spaces.first()
        game.status = CALCULATING
        game.save()

        success = game.tryAddPlayer(player)
        if (success):
            return True
        else:
            return False
    else:
        Battle.objects.create(player1=player)
        return True