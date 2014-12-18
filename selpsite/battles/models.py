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
    SHORT_RANGE = 'SR'
    MID_RANGE = 'MR'
    LONG_RANGE = 'LR'
    MOVE_AWAY = 'MA'
    MOVE_CLOSE = 'MC'
    MOVE_CHOICES = (
        (SHORT_RANGE, 'Short Range'),
        (MID_RANGE, 'Mid Range'),
        (LONG_RANGE, 'Long Range'),
        (MOVE_AWAY, 'Move Away'),
        (MOVE_CLOSE, 'Move Close'),
    )
    moveUsed = models.CharField(max_length=2,
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
    lastMove = models.ForeignKey(Move, 
                                 related_name='lastMove', 
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

    # Returns either 1 or 2 based on the player number in the related
    # Battle object, or 0 if the player is not in any Battle
    # TODO: This should be a field which is automatically updated in
    # Battle.save()
    def getPlayerNumber(self):
        # The attributes to check area related_names for the OneToOne
        # relations player1 and player2 of Battle
        # Therefore the attribute might not even exist, so we check
        # this first
        if (hasattr(self, 'player1') and 
            not self.player1 is None):
            return 1
        elif (hasattr(self, 'player2') and
            not self.player2 is None):
            return 2
        else:
            return 0

    # Returns the battle which the player is in, or None if they are 
    # not in any
    # TODO: This should be a field which is automatically updated in
    # Battle.save()
    def getBattle(self):
        playerNo = self.getPlayerNumber()
        if (playerNo == 1):
            return self.player1
        elif(playerNo == 2):
            return self.player2
        else:
            return None

    # Returns boolean indicating if the player is either player1 or
    # player2 of some battle
    # TODO: This should be a field which is automatically updated in
    # Battle.save()
    def isInBattle(self):
        return (self.getPlayerNumber() != 0)

    # This method is only for adding the move, it contains no logic for
    # if a move can be made at this time, or the effect of it
    def addMove(self, moveUsed):
        # Get the battle the player is in
        battle = self.getBattle()
        if (battle is None):
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
    # The "distance" between player changes how much damage moves do
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    DISTANCES = (
        (SHORT, 'Short'),
        (MEDIUM, 'Medium'),
        (LONG, 'Long')
    )
    distance = models.IntegerField(choices=DISTANCES,
                                   default=MEDIUM)
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
                player.opponent = self.player2
                player.save()
                self.player2.opponent = player
                self.player2.save()
            # Add to slot
            self.player1 = player
            self.save()
            return True
        elif(self.player2 is None):
            # Add opponent
            player.opponent = self.player1
            player.save()
            self.player1.opponent = player
            self.player1.save()
            # Add to slot
            self.player2 = player
            self.save()
            return True
        else:
            return False

