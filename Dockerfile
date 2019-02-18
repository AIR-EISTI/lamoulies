FROM python:3.7-alpine

ADD requirements.txt /requirements.txt

RUN set -ex \
	&& apk add --no-cache --virtual .build-deps\
		postgresql-dev \
		postgresql-client \
		gcc \
		make \
		libc-dev \
		musl-dev \
		linux-headers \
		pcre-dev \
		py3-virtualenv \
		python3-dev \
	&& python -m venv /venv \
	&& /venv/bin/pip install -U pip \
	&& /venv/bin/pip install -r /requirements.txt

WORKDIR /code/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=lamouliesdor.settings

ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=lamouliesdor/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

#RUN DATABASE_URL=none /venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive", "--touch-reload=/code/lamouliesdor/settings.py", "--static-map", "/static=/code/static"]
