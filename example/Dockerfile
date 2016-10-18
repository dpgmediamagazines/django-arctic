# Dockerfile for Arctic example project

FROM python:3.5

ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN mkdir -p /code
ADD ./requirements /code/requirements
RUN pip install -r /code/requirements/requirements.txt

ADD . /code/

RUN python manage.py migrate
RUN python manage.py loaddata fixtures/demo_data.json

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
