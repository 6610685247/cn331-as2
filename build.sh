#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

# ----------------------
# Upgrade pip and install dependencies
# ----------------------
pip install --upgrade pip
pip install -r requirements.txt

# ----------------------
# Collect static files
# ----------------------
python manage.py collectstatic --no-input

# ----------------------
# Apply database migrations
# ----------------------
python manage.py migrate

# ----------------------
# Create superuser only if it doesn't exist
# ----------------------
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin1234')
EOF
