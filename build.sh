#!/usr/bin/env bash
# Production build script for Render / Railway / Cloud Linux hosts
set -o errexit

# Install python dependencies
pip install -r requirements.txt

# Collect static files with WhiteNoise compression
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Seed database with initial doctor data, clinic info & catalog (safe & idempotent)
python manage.py seed_data
