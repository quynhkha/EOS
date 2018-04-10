# EOS - Image processing on Web 
This project allows user to process rock crystal image on web. The main technology used are OpenCV, Django and JQuery.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites
```
Ubuntu 14.04 
Python >3.4
```

### Installing

Django 1.11.2 for python3 
```
pip3 install django==1.11.2
```

OpenCV-python 3.0 (or 3.2)
```

Follow this guide:
http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/

Notes: need to update cmake to 3.2
sudo apt-get remove cmake cmake-data
sudo -E add-apt-repository -y ppa:george-edison55/cmake-3.x
sudo -E apt-get update
sudo apt-get install cmake

update bashrc
source ~/.bashrc

If have error, check this out:
https://devtalk.nvidia.com/default/topic/986950/opencv-installation-problem-nppigraphcutinitalloc-not-declared/

More precisely, modify this file "opencv-3.1.0/modules/cudalegacy/src/graphcuts.cpp" by replacing
#if !defined (HAVE_CUDA) || defined (CUDA_DISABLER)

#if !defined (HAVE_CUDA) || defined (CUDA_DISABLER)  || (CUDART_VERSION >= 8000)
```



Django Session security
```
pip3 install django-session-security
```

Postgresql database
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Django Postgresql
```
pip3 install psycopg2
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

