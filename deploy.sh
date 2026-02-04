#!/bin/bash
# Baby Shower RSVP - GCP Cloud Run Deployment Script

set -e

echo "🎉 Baby Shower RSVP - GCP Cloud Run Deployment"
echo "=============================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get the current GCP project
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ No GCP project is set. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 GCP Project: $PROJECT_ID"
IMAGE_TAG="gcr.io/$PROJECT_ID/baby-shower-rsvp:latest"

echo "🔨 Building container image..."
gcloud builds submit --tag $IMAGE_TAG .

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy baby-shower-rsvp \
    --image $IMAGE_TAG \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars=FLASK_ENV=production

echo ""
echo "✅ Deployment successful!"
echo "🌐 Your app is now live. Visit the URL shown above."