from django.db import models
from django.contrib.auth.models import User


# Represents a "move" in a battle made by a single player
class Move(models.Model):
    def __unicode__(self):
        s = str(self.player) + " " +\
            str(self.moveNo) + " - " +\
            str(self.get_moveUsed_display())
        return s
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
    def __unicode__(self):
        return self.user.username
    MAX_HP = 100
    user = models.ForeignKey(User)
    hp = models.IntegerField(default=MAX_HP)
    # "Locked in" moves - the player can no longer chagne them
    # When both are not null, the turn can proceed
    currentMove = models.ForeignKey(Move, 
                                    related_name='currentMove', 
                                    null=True,
                                    default=None)
    opponent = models.OneToOneField('self',
                                    related_name='_opponent',
                                    null=True,
                                    default=None)
    # Saves the current user as their opponent's opponent
    def save(self, *args, **kwargs):
        super(Player, self).save()
        if (not self.opponent is None):
            self.opponent.opponent = self
    # This method is only for adding the move, it contains no logic for
    # if a move can be made at this time, or the effect of it
    def addMove(self, moveUsed):
        # Get the battle the player is in
        if (hasattr(self, 'player1') and 
            not self.player1 is None):
            battle = self.player1
        elif (hasattr(self, 'player1') and 
            not self.player1 is None):
            battle = self.player2
        else: 
            return None
        move = Move.objects.create(moveUsed = moveUsed,
                                   player = self,
                                   moveNo = battle.turnNumber)
        self.currentMove = move
        self.save()
        battle.lastMoveTime = move.time
        battle.save()
        return move


# Represents a "battle" between two players
class Battle(models.Model):
    def __unicode__(self):
        return str(self.startTime) + " : " +\
            str(self.player1) + " vs " +\
            str(self.player2)
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
                                   null=True,
                                   default=None)
    player2 = models.OneToOneField(Player,
                                   related_name='player2', 
                                   null=True,
                                   default=None)
    # Includes the current turn
    turnNumber = models.IntegerField(default=1)
    # Will be null during the game
    winner = models.ForeignKey(Player, 
                               related_name='winner', 
                               null=True,
                               default=None)
    # Store the time of the most recent move so that we know if the
    # players are inactive
    lastMoveTime = models.DateTimeField(null=True,
                                        default=None)

    def tryAddPlayer(self, player):
        # Check for a slot and add the player
        if (self.player1 is None):
            # Add opponent
            if (not self.player2 is None):
                # Don't need to add to the other player
                # Since saving one does this automatically
                player.opponent = self.player2
                player.save()
            # Add to slot
            self.player1 = player
            self.save()
            return True
        elif(self.player2 is None):
            # Add opponent
            # Don't need to add to the other player
            # Since saving one does this automatically
            player.opponent = self.player1
            player.save()
            # Add to slot
            self.player2 = player
            self.save()
            return True
        else:
            return False

