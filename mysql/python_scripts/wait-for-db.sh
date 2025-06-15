#!/bin/sh

echo "Waiting for database to start."

until mysqladmin ping -h"db" -u"root" -p"root" --silent; do
  sleep 2
done

sleep 2

echo "Database is up – launching updater script"
exec python -u updater.py