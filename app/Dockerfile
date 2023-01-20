FROM python:3.9.7

WORKDIR /app
ENV FLASK_APP=app

COPY ./flaskapp/requirements.txt ./


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6


RUN pip install --upgrade pip


RUN pip install opencv-python
RUN pip install opencv-contrib-python


RUN pip install -r requirements.txt