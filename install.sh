#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PY=python3
"$PY" manage.py migrate --noinput

# ADMIN_USERNAME="set-me-manually"
# ADMIN_PASSWORD="set-a-strong-password-manually"
# if [[ "$ADMIN_USERNAME" == "set-me-manually" || "$ADMIN_PASSWORD" == "set-a-strong-password-manually" ]]; then
#   echo "Set ADMIN_USERNAME and ADMIN_PASSWORD manually in install.sh before running." >&2
#   exit 1
# fi

ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin"
 
"$PY" manage.py shell -c "from messenger.models import User; User.objects.get_or_create(name='$ADMIN_USERNAME', defaults={'password': '$ADMIN_PASSWORD', 'isadmin': True})"
echo "Admin user created with username '$ADMIN_USERNAME' and password '$ADMIN_PASSWORD'."