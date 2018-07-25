FROM python:3.5

RUN apt-get update && apt-get install -y --no-install-recommends \
                      postgresql \
                      postgresql-contrib \
                   && pip install --upgrade pip \
                   && pip install \
                          Pillow==5.1.0 \
                          django==1.11.2 \
                          numpy==1.14.5 \
                          scipy==1.1.0 \
                          scikit-learn \
                          matplotlib==2.2.2 \
                          opencv-python \
                          django-session-security \
                          psycopg2 \
                   && rm -rf /var/lib/apt/list/*
                   
EXPOSE 8000                      
