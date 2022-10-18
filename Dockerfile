FROM python:3.7.0

RUN python -m pip install --upgrade pip

COPY . /app

WORKDIR /app

ENV PYTHONPATH /seeyaArchive

RUN pip install -r requirements.txt

RUN pip install gunicorn==20.1.0

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c" , "python manage.py collectstatic --noinput --settings=settings.production && python manage.py migrate --settings=settings.production && gunicorn wsgi:application --bind 0.0.0.0:8000"]
