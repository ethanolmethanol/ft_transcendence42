#!/bin/bash
sudo apt-get install -y postgresql-client
cd back/ 
python3 -m venv venv 
source venv/bin/activate 
pip install --upgrade pip 
pip install django django-cors-headers
pip install django-hurricane 
pip install psycopg2
