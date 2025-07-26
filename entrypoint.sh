#!/bin/sh
echo "Applying migrations..."
uv run manage.py makemigrations --noinput
uv run manage.py migrate --noinput

echo "Creating superuser..."
echo "
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
" | uv run manage.py shell

echo "Starting server..."
uv run manage.py runserver 0.0.0.0:8000
