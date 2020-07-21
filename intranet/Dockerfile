FROM python:3.7
LABEL maintainer="avery.uslaner@redbutte.utah.edu"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install cron

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

COPY . /code/
WORKDIR /code/

RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

COPY box_report /etc/cron.d/box_report
RUN chmod 0644 /etc/cron.d/box_report
RUN crontab /etc/cron.d/box_report
RUN touch /var/log/cron.log

EXPOSE 8000

