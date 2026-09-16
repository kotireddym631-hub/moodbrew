#!/bin/bash
echo "=== MoodBrew Build ==="
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
echo "=== Build Done ==="
