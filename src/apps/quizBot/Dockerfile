FROM python:latest

WORKDIR /usr/src/app

COPY ./src/apps/quizBot/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/apps/quizBot ./src/apps/quizBot
COPY ./src/data ./src/data
COPY ./src/extensions ./src/extensions

CMD [ "python", "./src/apps/quizBot/main.py" ]
