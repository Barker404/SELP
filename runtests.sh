#!/bin/bash
# Activate the virtualenv
source selpenv/bin/activate
# Run the tests - omit coverage on all migrations and on the mechs app (unused code) 
coverage run --source='selpsite' --omit=*migrations*,*mechs/* selpsite/manage.py test selpsite/
# Show the report
coverage report