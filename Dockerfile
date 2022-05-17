
FROM python:3.9.0

RUN python -m pip install --upgrade pip

WORKDIR /home

RUN git clone -b develop --single-branch https://github.com/SEEYA-ARCHIVE/SEEYA-ARCHIVE-BACK.git

WORKDIR /home/SEEYA-ARCHIVE-BACK

RUN pip install -r requirements.txt

RUN pip install gunicorn==20.1.0

EXPOSE 80

ENTRYPOINT ["/bin/sh", "-c" , "cd /home/SEEYA-ARCHIVE-BACK && python manage.py collectstatic --noinput --settings=seeyaArchive.settings.production && python manage.py migrate --settings=seeyaArchive.settings.production && gunicorn seeyaArchive.wsgi:application --bind 0.0.0.0:80"]