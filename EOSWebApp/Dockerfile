FROM python:3.5

RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip && pip --no-cache-dir install \
	django==1.11.2 \
	opencv-python \
	django-session-security \
	psycopg2 \
	Pillow==5.1.0 \
	scipy \
	scikit-learn \
	scikit-image \
	matplotlib

ADD . /code/