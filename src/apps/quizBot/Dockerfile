FROM python:latest

ARG COSMOSDB_ACCOUNT_KEY
ARG COSMOSDB_ACCOUNT_URI
ARG TELEGRAM_TOKEN

ENV COSMOSDB_ACCOUNT_KEY=$COSMOSDB_ACCOUNT_KEY
ENV COSMOSDB_ACCOUNT_URI=$COSMOSDB_ACCOUNT_URI
ENV TELEGRAM_TOKEN=$TELEGRAM_TOKEN


WORKDIR /usr/src/app

COPY ./src/apps/quizBot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/apps/quizBot ./src/apps/quizBot
COPY ./src/data ./src/data
COPY ./src/extensions ./src/extensions

CMD [ "python", "./src/apps/quizBot/main.py" ]
