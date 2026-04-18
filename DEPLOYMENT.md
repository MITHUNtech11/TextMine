# Deployment Guide for TextMine

## Local Development

### Quick Setup
```bash
git clone https://github.com/yourusername/TextMine.git
cd TextMine
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Add your Google Gemini API key
3. Add Tesseract path if needed

### Run Locally
```bash
uvicorn main:app --reload
# Open http://localhost:8000/docs
```

---

## Docker Deployment

### Build Docker Image
```bash
docker build -t textmine:latest .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  --name textmine \
  textmine:latest
```

### Docker Compose
```yaml
version: '3.8'

services:
  textmine:
    build: .
    ports:
      - "8000:8000"
    environment:
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
      TESSERACT_PATH: /usr/bin/tesseract
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
```

Run with: `docker-compose up -d`

---

## Production Deployment

### Prerequisites
- Python 3.10+
- Tesseract OCR installed
- Google Gemini API key
- SSL certificates (for HTTPS)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn
```

### 2. Configure Environment
Set environment variables:
```bash
export GOOGLE_API_KEY=your_api_key
export TESSERACT_PATH=/usr/bin/tesseract
```

### 3. Run with Gunicorn
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 4. Use Reverse Proxy (Nginx)
```nginx
upstream textmine {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    client_max_body_size 50M;

    location / {
        proxy_pass http://textmine;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Systemd Service (Linux)
Create `/etc/systemd/system/textmine.service`:
```ini
[Unit]
Description=TextMine API Service
After=network.target

[Service]
Type=notify
User=textmine
WorkingDirectory=/opt/textmine
Environment="GOOGLE_API_KEY=your_api_key"
ExecStart=/opt/textmine/venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable textmine
sudo systemctl start textmine
```

---

## Cloud Deployment

### AWS (EC2 + Gunicorn + Nginx)
1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies: `sudo apt-get install python3-pip tesseract-ocr nginx`
3. Clone repo and setup
4. Configure Nginx as reverse proxy
5. Use AWS Secrets Manager for API keys
6. Enable Auto Scaling Group

### Heroku
```bash
heroku create textmine
git push heroku main
heroku config:set GOOGLE_API_KEY=your_api_key
heroku open
```

### Google Cloud Run
```bash
gcloud run deploy textmine \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_api_key
```

### Azure App Service
```bash
az webapp up \
  --name textmine \
  --resource-group myResourceGroup \
  --runtime "PYTHON|3.11"
```

---

## Performance Optimization

### Enable Caching
```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend
from redis import asyncio as aioredis

FastAPICache2.init(RedisBackend, expire=3600)
```

### Database Connection Pooling
```python
from sqlalchemy.pool import QueuePool
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

### Async Processing
- Use Celery for long-running OCR tasks
- Queue large batch jobs
- Return job ID, let client poll for results

---

## Monitoring & Logging

### Application Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Health Check Endpoint
```bash
curl http://localhost:8000/health
```

### Metrics Endpoint
```python
from prometheus_client import Counter, Histogram, generate_latest

parse_counter = Counter('textmine_parses_total', 'Total parses')
parse_duration = Histogram('textmine_parse_duration_seconds', 'Parse duration')
```

### Log Aggregation
- Use ELK Stack (Elasticsearch, Logstash, Kibana)
- Or Splunk, DataDog, New Relic
- Monitor for errors and performance issues

---

## Security Checklist

- [ ] HTTPS/TLS enabled
- [ ] API keys in environment variables
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Input validation active
- [ ] SQL injection prevention (if using DB)
- [ ] CSRF protection enabled
- [ ] Dependencies updated
- [ ] Firewall rules configured
- [ ] Backup strategy in place
- [ ] Disaster recovery plan

---

## Scaling Strategies

### Horizontal Scaling
- Run multiple app instances behind load balancer
- Use Kubernetes for orchestration
- Database read replicas

### Vertical Scaling
- Increase worker processes
- Increase server RAM
- Use faster CPUs

### Asynchronous Processing
- Queue jobs with Celery
- Process in background
- Reduce API response time

---

## Troubleshooting

### High Memory Usage
- Reduce worker count
- Process files in chunks
- Implement garbage collection

### Slow Response Times
- Enable caching
- Add more workers
- Check Tesseract performance
- Monitor database queries

### API Rate Limiting Issues
- Implement exponential backoff
- Use connection pooling
- Check for retry storms

---

For support, see [README.md](README.md) or [CONTRIBUTING.md](CONTRIBUTING.md)
