#!/bin/bash
PROJECT_ID="gcp-demo-028"
REGION="us-central1"
SERVICE_NAME="rag-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME:latest"

docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME

gcloud run deploy $SERVICE_NAME     --image $IMAGE_NAME     --region $REGION     --platform managed     --allow-unauthenticated
