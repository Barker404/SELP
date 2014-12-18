#!/bin/bash
# Activate the virtualenv
source selpenv/bin/activate
# Run the tests
python selpsite/manage.py test selpsite/
