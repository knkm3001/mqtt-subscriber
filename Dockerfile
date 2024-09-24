FROM python:3.12.6-slim-bullseye


WORKDIR /app

COPY requirements.txt ./
COPY src/* ./

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 subscribe.py