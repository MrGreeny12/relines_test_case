FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/perx

RUN apt update
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/perx

EXPOSE 8000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic"]