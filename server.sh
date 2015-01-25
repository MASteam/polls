#!/bin/bash

case "$1" in
"start") 
python manage.py runfcgi maxchildren=10 method=prefork host=127.0.0.1 port=9001 pidfile=/tmp/server.pid
;;
"stop") 
kill -9 `cat /tmp/server.pid` 
;;
"restart")
echo "Stoping server...\n";
sh $0 stop
sleep 1
echo "Starting server...\n";
sh $0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac
