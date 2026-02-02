# Baby Shower RSVP App

A lightweight Flask application for managing baby shower RSVPs, optimized for deployment on Google Cloud Run.

## Features

- 🎨 Beautiful, responsive landing page with RSVP form
- 📝 Form validation and error handling
- 💾 Lightweight in-memory storage with file persistence
- 🚀 Cloud Run optimized (containerized, health checks)
- 📱 Mobile-friendly design
- ⚡ Minimal dependencies (Flask only)

## Project Structure

```
babyshower/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Landing page with RSVP form
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration for Cloud Run
├── .dockerignore         # Files to exclude from container
├── responses.json        # RSVP responses (auto-created)
└── README.md            # This file
```

## Local Development

### Prerequisites
- Python 3.11+
- pip or venv

### Setup

1. Clone/navigate to the project:
```bash
cd babyshower
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:8080
```

## API Endpoints

### GET `/`
Returns the RSVP landing page.

### POST `/api/rsvp`
Submits an RSVP response.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "attending": true,
  "guests": 2,
  "dietary": "vegetarian",
  "comments": "Looking forward to it!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "RSVP received!"
}
```

### GET `/api/responses`
Returns summary of all responses (admin/demo endpoint).

```json
{
  "total": 10,
  "attending": 8,
  "not_attending": 2,
  "total_guests": 15,
  "responses": [...]
}
```

### GET `/health`
Health check endpoint for Cloud Run.

## Deployment to Google Cloud Run

### Prerequisites
- Google Cloud Account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed locally

### Deploy

1. Set your GCP project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Build and push the container to Cloud Run:
```bash
gcloud run deploy baby-shower-rsvp \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

3. The command will output your deployment URL. Visit it to use the app!

### Manual Docker Build & Push (Alternative)

1. Build the image:
```bash
docker build -t gcr.io/YOUR_PROJECT_ID/baby-shower-rsvp:latest .
```

2. Push to Container Registry:
```bash
docker push gcr.io/YOUR_PROJECT_ID/baby-shower-rsvp:latest
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy baby-shower-rsvp \
  --image gcr.io/YOUR_PROJECT_ID/baby-shower-rsvp:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Data Storage

The app uses a simple file-based storage approach (`responses.json`) for lightweight persistence:
- RSVPs are stored in memory during runtime
- Responses are persisted to `responses.json` on each submission
- On restart, previous responses are automatically loaded

**Note:** For Cloud Run's ephemeral filesystem, each instance has its own `responses.json`. For production with multiple instances, consider:
- Using Google Cloud Firestore
- Using Google Cloud SQL
- Implementing Cloud Storage integration

## Environment Variables

- `PORT` (default: 8080) - The port the app listens on. Cloud Run automatically sets this.

## Docker Testing Locally

1. Build the image:
```bash
docker build -t baby-shower-rsvp:latest .
```

2. Run the container:
```bash
docker run -p 8080:8080 baby-shower-rsvp:latest
```

3. Visit `http://localhost:8080`

## Customization

### Update Event Details
Edit `templates/index.html` to customize:
- Event title and emoji
- Form labels and placeholder text
- Colors and styling

### Modify Backend Logic
Edit `app.py` to:
- Add new form fields
- Implement email notifications
- Add database integration
- Add authentication

## Security Notes

- The `/api/responses` endpoint is currently public. Protect it in production.
- Validate and sanitize all user inputs (currently basic validation in place).
- Use environment variables for sensitive data.
- Consider enabling authentication for the app.

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8080 or run on different port
python app.py  # Check app.py to modify PORT
```

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Docker build fails:**
```bash
docker build --no-cache -t baby-shower-rsvp:latest .
```

## License

MIT