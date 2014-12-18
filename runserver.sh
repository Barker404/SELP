#!/bin/bash
# Activate the virtualenv
source selpenv/bin/activate
# Run the server (use one of the two options below:
# To only connect from this computer
python selpsite/manage.py runserver
# To be able to connect from other computers on the network
# python elpsite/manage.py srunserver 0.0.0.0:8000
