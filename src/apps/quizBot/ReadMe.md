# Create a docker image
Go to root of the repo

### Build an image for Heroku

#### Login into Heroku container registry

```bash
heroku container:login
```

or

```bash
docker login --username=_ --password=$(heroku auth:token) registry.heroku.com
```

#### Build image

```bash
docker build -t registry.heroku.com/school-quiz-tg-bot/bot -f src/apps/quizBot/Dockerfile  --platform linux/amd6 ./
```

> Note the tag of the image: 
> registry.heroku.com/<app>/<process-type>

### Push image to Heroku

```bash
docker push registry.heroku.com/school-quiz-tg-bot/bot
```

### Release image

```bash
heroku container:release bot --app school-quiz-tg-bot
```

### View logs

```bash
heroku logs --tail --app school-quiz-tg-bot
```