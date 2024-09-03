git push
ssh root@webhook.booijanalytics.nl "cd code/webinargeek_microservice;git pull; docker compose down;docker compose -f docker-compose.yml up -d --build"




