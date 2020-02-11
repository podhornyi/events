#!/usr/bin/env bash


chmod +x ./wait-for-mysql.sh
./wait-for-mysql.sh

echo "Initialize database."
python init_db.py --action init

echo "Start the server"
python api/main.py
