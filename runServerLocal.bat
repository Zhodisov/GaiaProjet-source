@echo off

call venv\Scripts\activate

pip install -r requirements.txt

py server.py
