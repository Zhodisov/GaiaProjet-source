@echo off

pip install -r requirements.txt

start ngrok http 9200

py server.py

pause