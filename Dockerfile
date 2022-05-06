FROM python:3.9.0

RUN python -m pip install --upgrade pip

WORKDIR /home

RUN git clone -b develop --single-branch https://github.com/SEEYA-ARCHIVE/SEEYA-ARCHIVE-BACK.git

WORKDIR /home/SEEYA-ARCHIVE-BACK

RUN pip install -r requirements.txt

EXPOSE 80


ENTRYPOINT ["/bin/sh", "-c" , "cd /home/SEEYA-ARCHIVE-BACK && python manage.py migrate --settings=seeyaArchive.settings.production && gunicorn seeyaArchive.wsgi:application --bind 0.0.0.0:80"]
#ENTRYPOINT ["/bin/sh", "-c" , "python SEEYA-ARCHIVE-BACK/manage.py collectstatic --noinput && python SEEYA-ARCHIVE-BACK/manage.py migrate --settings=seeyaArchive.settings.production"]

#CMD ["gunicorn", "seeyaArchive.wsgi", "--bind", "0.0.0.0:80" ]