FROM python:3.5

WORKDIR /home/EOS/EOSWebApp
COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends \
                      postgresql \
                      postgresql-contrib \
                   && pip install --upgrade pip \
                   && pip install -r requirements.txt \
                   && rm -rf /var/lib/apt/list/*
                   
COPY . .

EXPOSE 8000                      
