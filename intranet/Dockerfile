FROM python:3.7
LABEL maintainer="avery.uslaner@redbutte.utah.edu"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install \
    cron \
    libldap2-dev \
    libsasl2-dev

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

COPY . /code/
WORKDIR /code/

COPY box_report /etc/cron.d/box_report
RUN chmod 0644 /etc/cron.d/box_report

RUN useradd wagtail
RUN chown -R wagtail /code
RUN touch /var/log/cron.log
RUN chown wagtail /etc/cron.d/box_report
RUN chown wagtail /var/log/cron.log
USER wagtail

RUN crontab /etc/cron.d/box_report


EXPOSE 8000

