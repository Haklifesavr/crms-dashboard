#!/bin/bash

# Check if RUN_MIGRATIONS is set to 1
if [ "$RUN_MIGRATIONS" = "1" ]; then
  echo "Running Django migrations"
  python manage.py makemigrations
  python manage.py migrate --noinput  # The --noinput flag runs the migrations without requiring user input
else
  echo "Skipping migrations"
fi

# Start the main process
exec "$@"
