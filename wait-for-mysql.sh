#!/usr/bin/env bash


until echo '\q' | mysql -h $API_MYSQL_HOST -u $API_MYSQL_ROOT_USER -p$API_MYSQL_ROOT_PASSWORD 'mysql'; do
    >&2 echo "MySQL is unavailable - sleeping"
    sleep 1
done

>&2 echo "MySQL and Data are up - executing command"
