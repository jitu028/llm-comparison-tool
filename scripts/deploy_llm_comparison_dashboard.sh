#!/bin/bash
# Deployment script for LLM Comparison Dashboard (Frontend)

PROJECT_ID="gcp-demo-028"
REGION="us-central1"
SERVICE_NAME="llm-comparison-dashboard"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Submitting Dashboard build to Google Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME ./frontend

echo "🚀 Deploying Dashboard to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1024Mi

echo "✅ Dashboard Deployment Complete!"
