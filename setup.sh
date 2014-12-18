#!/bin/bash
# Create the virtualenv
virtualenv selpenv
# Activate it
source selpenv/bin/activate
# Installrequirements
pip install -r requirements.txt
# Sync the database (do not create an admin account)
python selpsite/manage.py syncdb --noinput
# Migrate the tables in the database which use migrations
python selpsite/manage.py migrate
