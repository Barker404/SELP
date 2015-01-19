 Software Engineering Large Practical
=======
 
 A simple website made for my undergraduate 3rd year semester 1 course __SELP__, written using Django.
 The basic concept is a PvP battling game, where player are ranked based on their wins.

The proposal can be found in Proposal/
The report can be found in Report/

There are 3 bash scripts that can be used:
* setup.sh 		- Sets up the virtualenv and database. This should be run first.
* runserver.sh 	- Runs the server on 127.0.0.1:8000. There is a line within the script which can be uncommented (and the original line commented out) to run the server so that is accessible from any computer on the local network.
* runtests.sh 	- Runs the automated test suite and all of the written tests. Also shows coverage report.

The practical was awarded a final mark of 90% (initially 95%, but capped down to 90% for non-early submission). 

## Unfinished aspects/Possible improvements
The battle matchup system is pretty basic, and not necessarily done in the best way. In particular, there is no concept of a player being "connected" or "disconnected", nor is there any kind of turn timer - if a player leaves the game, it will never finish, and similarly if a player leaves when they are in the process of finding a game, they will stay in the queue and later e matched with another player (potentially even themselves). 

The web frontend is very basic due to my lack of web design experience, and the fact that the practical was not about design. If I was to change this I would probably glue on some defauly bootstrap theme, but during development I became fond of the minimal design.

The user system has a lot of polish that could be easily added - editing the user profile description, emails for validation/password reset, authentication checks etc. This largely be done using Django built-in methods/views/forms though, so is not of much significance from a software development point of view.
