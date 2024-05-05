#!/usr/bin/env bash
cd /webapps/diplom/
source venv/bin/activate
pip3 install -r requirements.txt
export DJANGO_SETTINGS_MODULE="diplom.settings"
python3 manage.py migrate --noinput
systemctl restart diplom
systemctl restart nginx
