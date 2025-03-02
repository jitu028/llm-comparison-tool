#!/bin/bash
# Deployment script for LLM Comparison API (Backend)

PROJECT_ID="gcp-demo-028"
REGION="us-central1"
SERVICE_NAME="llm-comparison-api"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Submitting API build to Google Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME ./backend

echo "🚀 Deploying API to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1024Mi

echo "✅ API Deployment Complete!"
