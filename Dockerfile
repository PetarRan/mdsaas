# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR /app

COPY . /app

COPY run.py /app/run.py

RUN pip install spacy
RUN python -m spacy download en_core_web_sm
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "run.py" ]