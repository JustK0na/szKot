#!/bin/sh

echo "Czekam na bazę danych..."

until mysqladmin ping -h"db" -u"root" -p"root" --silent; do
  sleep 2
done

sleep 2

echo "Baza danych gotowa – uruchamiam skrypt"
exec python -u updater.py