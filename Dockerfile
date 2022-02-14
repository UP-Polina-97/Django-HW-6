# pull the official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

COPY . .

COPY /requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]

