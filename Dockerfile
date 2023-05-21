FROM python:3.8

ENV DockerHOME=/home/app/technical

RUN mkdir -p $DockerHOME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY . $DockerHOME

EXPOSE 8000

RUN pip install -r requirements.txt
