# RL Bot API Rock Paper Scissors

Reinforcement learning bot - API to play Rock / Paper / Scissors with an AI Bot. The more you play the more Bot is learning and tries to win. A few games are needed for the bot to be trained.

## Install and run Project

To run the project:
```bash
docker-compose up
```

To shutdown the service:
```bash
docker-compose down
```

## API

Swagger documentation on the browser:
```bash
http://localhost:5000/api/v1/rps/
```

Play request:
```bash
curl --location --request POST 'http://localhost:5000/api/v1/rps/game/play' \
--header 'Content-Type: application/json' \
--data-raw '{
    "myHand": "rock"
}'
```

Results request:
```bash
curl --location --request GET 'http://localhost:5000/api/v1/rps/game/results'
```

Reset request:
```bash
curl --location --request GET 'http://localhost:5000/api/v1/rps/game/reset'
```