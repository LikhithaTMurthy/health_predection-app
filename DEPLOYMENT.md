# Deployment Guide

This guide covers deploying the Health Prediction Application to various platforms.

## 🚀 Quick Start (Development)

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/yourusername/health_predection-app.git
cd health_predection-app

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py

# Application available at: http://localhost:5000
```

## 📦 Production Deployment

### Prerequisites

- Python 3.8+
- pip package manager
- Git
- Virtual environment (recommended)

### Step 1: Environment Configuration

```bash
# Create production .env file
cp .env.example .env

# Edit .env with production settings:
# - FLASK_ENV=production
# - FLASK_DEBUG=False
# - SECRET_KEY=generate-strong-key (use: python -c "import secrets; print(secrets.token_hex(32))")
# - DATABASE_URL=postgresql://user:pass@localhost/healthdb (if using PostgreSQL)
```

### Step 2: Web Server Setup

#### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run application
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# For production with multiple workers:
gunicorn -w 8 -b 0.0.0.0:8000 --timeout 60 app:app
```

#### Using Waitress

```bash
# Install Waitress
pip install waitress

# Run application
waitress-serve --port=8000 app:app
```

### Step 3: Reverse Proxy Setup (Nginx)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

### Step 4: SSL/TLS Certificate (Certbot)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certify -d yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## ☁️ Cloud Platform Deployments

### Heroku Deployment

#### 1. Create Procfile

```
web: gunicorn app:app
```

#### 2. Create Runtime Specification

```
python-3.10.11
```

#### 3. Deploy

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Database (optional)
heroku addons:create heroku-postgresql:hobby-dev
```

### PythonAnywhere Deployment

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your code via Git or file upload
3. Create virtual environment in PythonAnywhere
4. Configure WSGI file
5. Reload web app

### AWS EC2 Deployment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/health_predection-app.git
cd health_predection-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
pip install gunicorn

# Create systemd service file
sudo nano /etc/systemd/system/health-app.service
```

**Service file content:**
```ini
[Unit]
Description=Health Prediction App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/health_predection-app
Environment="PATH=/home/ubuntu/health_predection-app/venv/bin"
ExecStart=/home/ubuntu/health_predection-app/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start health-app
sudo systemctl enable health-app

# Check status
sudo systemctl status health-app
```

### Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///patients.db
    volumes:
      - ./instance:/app/instance
    restart: unless-stopped

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

#### 3. Build and Run

```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 Database Migration

### SQLite to PostgreSQL

```bash
# Install dependencies
pip install psycopg2-binary

# Update DATABASE_URL in .env
# DATABASE_URL=postgresql://user:pass@localhost/healthdb

# Create tables in PostgreSQL
# The SQLAlchemy models will handle table creation automatically

# Migrate data (if needed)
python migrate_database.py
```

## 🔒 Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Enable HTTPS/SSL
- [ ] Set FLASK_ENV=production
- [ ] Disable debug mode
- [ ] Use environment variables for secrets
- [ ] Implement user authentication
- [ ] Enable rate limiting
- [ ] Add CSRF protection
- [ ] Configure CORS properly
- [ ] Regular security updates
- [ ] Database backups enabled
- [ ] Monitoring and logging setup

## 📈 Performance Optimization

### Database Optimization

```python
# Add database indexes
db.Index('idx_email', Patient.email)

# Use connection pooling
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

### Caching

```bash
# Install Redis
pip install redis

# Configure Flask-Caching
pip install Flask-Caching
```

### Static Files

```bash
# Use CDN or compression
pip install Flask-Compress
```

## 📊 Monitoring

### Health Checks

```bash
# Add monitoring endpoint
curl http://localhost:5000/api/health
```

### Logging

```python
# Configure logging to file
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10240000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 PID
```

### Database Lock

```bash
# Remove lock file
rm patients.db-journal
```

### Permission Denied

```bash
# Fix permissions
chmod +x app.py
chmod -R 755 static/
chmod -R 755 templates/
```

---

**Version**: 1.0  
**Last Updated**: 2024
