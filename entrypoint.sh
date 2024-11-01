#!/bin/sh

# Apply database makemigrations
python manage.py makemigrations
# Apply database migrations
python manage.py migrate

# Start the Django development server on port 8000
python manage.py runserver 0.0.0.0:8000
