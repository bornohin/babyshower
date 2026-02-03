# Quick Start Guide

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### 1. Install Dependencies
```bash
cd babyshower
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```

The app will start on `http://localhost:8080`

### 3. Test the RSVP Form
1. Open your browser to `http://localhost:8080`
2. Fill out the form
3. Submit to see it store the response
4. View all responses at `http://localhost:8080/api/responses`

---

## 🐳 Run with Docker

### 1. Build the Docker Image
```bash
docker build -t baby-shower-rsvp:latest .
```

### 2. Run the Container
```bash
docker run -p 8080:8080 baby-shower-rsvp:latest
```

The app will be available at `http://localhost:8080`

---

## ☁️ Deploy to Google Cloud Run

### Option 1: Using the Deploy Script (Recommended)

```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deployment

1. Set your GCP project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Deploy directly (gcloud builds and pushes for you):
```bash
gcloud run deploy baby-shower-rsvp \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. Once deployed, you'll get a URL like:
```
https://baby-shower-rsvp-xxxxx-uc.a.run.app
```

---

## 📊 Accessing RSVP Data

Visit the API endpoint to see all responses:
```
https://your-app-url.a.run.app/api/responses
```

Example response:
```json
{
  "total": 5,
  "attending": 4,
  "not_attending": 1,
  "total_guests": 8,
  "responses": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "attending": true,
      "guests": 2,
      "dietary": "vegetarian",
      "comments": "Can't wait!",
      "timestamp": "2026-02-02T10:30:00"
    }
  ]
}
```

---

## 🎨 Customizing the Event

Edit `templates/index.html` to customize:
- Event title
- Colors and styling
- Form fields and labels

---

## 📝 Notes

- RSVP responses are stored in `responses.json` (created automatically)
- For production deployments with multiple instances, use Google Cloud Firestore or Cloud SQL
- The `/api/responses` endpoint is public. Add authentication in production if needed.

---

## ❓ Troubleshooting

**Port 8080 already in use?**
```bash
# Use a different port
PORT=3000 python app.py
```

**Docker build fails?**
```bash
# Rebuild without cache
docker build --no-cache -t baby-shower-rsvp:latest .
```

**Cloud Run deployment fails?**
```bash
# Check gcloud authentication
gcloud auth login

# Verify project is set
gcloud config get-value project

# Check billing is enabled for the project
gcloud billing projects link YOUR_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
```

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Documentation](https://docs.docker.com/)
