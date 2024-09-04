git push
ssh $SSH_URL "cd code/FastAPI_webhook_to_SQS/;git pull; docker compose down;docker compose -f docker-compose.yml up -d --build"




