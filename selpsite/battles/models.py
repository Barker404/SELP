from django.db import models
from django.contrib.auth.models import User


# Represents a "move" in a battle made by a single player
class Move(models.Model):
    # More moves to be added if time
    # Potentially "move backwards", "move forwards" etc
    # May also have some concept of foreign key to 
    # "Possible Move"/"Attack" object
    ROCK = 'R'
    PAPER = 'P'
    SCISSORS = 'S'
    MOVE_CHOICES = (
        (ROCK, 'Rock'),
        (PAPER, 'Paper'),
        (SCISSORS, 'Scissors'),
    )
    moveUsed = models.CharField(max_length=1,
                                 choices=MOVE_CHOICES)
    player = models.ForeignKey('Player')
    moveNo = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


# Represents one of the "players" in a single game
# Different from a user in that it represents the player's information
# for just the one game
class Player(models.Model):
    MAX_HP = 100
    user = models.ForeignKey(User)
    hp = models.IntegerField(default=MAX_HP)
    # "Locked in" moves - the player can no longer chagne them
    # When both are not null, the turn can proceed
    currentMove = models.ForeignKey(Move, 
                                    related_name='currentMove', 
                                    null=True)
    opponent = models.OneToOneField('self',
                                    related_name='_opponent',
                                    null=True)
    # Saves the current user as their opponent's opponent
    def save(self, *args, **kwargs):
        super(Player, self).save()
        self.opponent.opponent = self

    def makeMove(self, moveUsed):
        # if (self.currentMove == null)
        move = Move.objects.create(moveUsed = moveUsed,
                                   player = self,
                                   moveNo = self.battle.turnNumber)
        self.currentMove = move
        move.save()
        self.save()

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
    status = models.IntegerField(choices=STATUSES,
                                 default=WAITING_FOR_PLAYER)
    startTime = models.DateTimeField(auto_now_add=True)

    # Links to the two player objects. 
    # Will be null before players connect
    player1 = models.OneToOneField(Player,
                                   related_name='player1', 
                                   null=True)
    player2 = models.OneToOneField(Player,
                                   related_name='player2', 
                                   null=True)
    # Includes the current turn
    turnNumber = models.IntegerField(default=0)
    # Will be null during the game
    winner = models.ForeignKey(Player, 
                               related_name='winner', 
                               null=True)
    # Store the time of the most recent move so that we know if the
    # players are inactive
    lastMoveTime = models.DateTimeField(auto_now_add=True)
