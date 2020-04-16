FROM python:3.7
LABEL maintainer="avery.uslaner@redbutte.utah.edu"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

COPY . /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

RUN python manage.py collectstatic --noinput

EXPOSE 8000

