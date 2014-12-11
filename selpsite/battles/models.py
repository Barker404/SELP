from django.db import models
from django.contrib.auth.models import User

# Represents a "battle" between two players
class Battle(models.Model):
    WAITING_FOR_PLAYER = 1
    WAITING_FOR_CHOICE = 2
    CALCULATING = 3
    FINISHED = 4
    STATUSES = (
        (WAITING_FOR_PLAYER, 'Waiting for another player'),
        (WAITING_FOR_CHOICE, 'Waiting for player choices'),
        (CALCULATING, 'Calculating results'),
        (FINISHED, 'Battle finished'),
    )
    startTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES,
                                 default=WAITING_FOR_PLAYER)

    # Definitely need to have a better concept of "player1" and "player2"
    # Either some kind of indexing/tuples
    # Or seperate "player" obejcts containing the HP, current move, etc.
    player1 = models.ForeignKey(User, 
                                related_name='player1', 
                                null=True)
    player2 = models.ForeignKey(User, 
                                related_name='player2', 
                                null=True)
    # Includes the current turn
    turnNumber = models.IntegerField(default=0)
    winner = models.ForeignKey(User, 
                               related_name='winner', 
                               null=True)
    player1HP = models.IntegerField()
    player2HP = models.IntegerField()
    # "Locked in" moves - the player can no longer chagne them
    # When both are not null, the turn can proceed
    player1CurrentMove = models.ForeignKey(User, 
                                           related_name='player1CurrentMove', 
                                           null=True)
    player2CurrentMove = models.ForeignKey(User, 
                                           related_name='player2CurrentMove', 
                                           null=True)

# Represents a "move" in a battle made by a single player
class Move(models.Model):
    # More moves to be added if time
    # Potentially "move backwards", "move forwards" etc
    # May also have some concept of foreign key to "Possible Move"/"Attack" object
    ROCK = 'R'
    PAPER = 'P'
    SCISSORS = 'S'
    MOVES = (
        (ROCK, 'Rock'),
        (PAPER, 'Paper'),
        (SCISSORS, 'Scissors'),
    )
    move_used = models.CharField(max_length=1,
                                choices=MOVES,
                                default=ROCK)
    player = models.ForeignKey(User)
    # Somehow restrict to 1 or 2? 
    playerNo = models.IntegerField()
    moveNo = models.IntegerField()
