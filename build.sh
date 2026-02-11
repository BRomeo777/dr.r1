#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Remove old database
rm -f db.sqlite3

# Collect static
python manage.py collectstatic --no-input

# Run only Django's default migrations (creates auth, admin tables)
python manage.py migrate

echo "✅ Build complete!"
