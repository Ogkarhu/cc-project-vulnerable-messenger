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
ADMIN_USERNAME="${ADMIN_USERNAME:-admin}" ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}" \
"$PY" manage.py shell -c "import os;from django.contrib.auth import get_user_model as g;U=g();u,_=U.objects.get_or_create(username=os.environ['ADMIN_USERNAME']);u.is_staff=u.is_superuser=True;u.set_password(os.environ['ADMIN_PASSWORD']);u.save()"