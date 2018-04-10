# EOS - Image processing on Web 
This project allows user to process rock crystal image on web. The main technology used are OpenCV, Django and JQuery.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites
Ubuntu 14.04 


### Installing

Django 1.11

OpenCV-python 3.0

Django Session security
```
pip install django-session-security
```

Postgresql database
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Django Postgresql
```
pip install psycopg2
```

### Initial setup

Create a new database
```
sudo su - postgres
sudo -u postgres createuser <username>
CREATE DATABASE <dbname> OWNER <username>;
ALTER USER <username> PASSWORD <password>;
```

Change DATABASE in settings.py accordingly


Run Django migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```

## To run 
```
cd EOSWebApp/
python3 manage.py runserver
```

