 Software Engineering Large Practical
=======
 
 A simple website made for my undergraduate 3rd year semester 1 course __SELP__, written using Django.
 The basic concept is a PvP battling game, where player are ranked based on their wins.

The proposal can be found in Proposal/
The report can be found in Report/

There are 3 bash scripts that can be used:
setup.sh 		- Sets up the virtualenv and database. This should be run first.
runserver.sh 	- Runs the server on 127.0.0.1:8000. There is a line within the script which can be uncommented (and the original line commented out) to run the server so that is accessible from any computer on the local network.
runtests.sh 	- Runs the automated test suite and all of the written tests. Also shows coverage report.