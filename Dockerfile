FROM python:3.9.13

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD python main.py
