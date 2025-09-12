# 🚀 Deployment Guide

## Quick Deployment Options

### Option 1: Local Development (Recommended for Testing)
```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/ai-rockfall-prediction-system.git
cd ai-rockfall-prediction-system
python scripts/setup.py

# Start system
python run_system.py --with-simulator

# Access
# Dashboard: http://localhost:3000
# API: http://localhost:5000
```

### Option 2: Docker Deployment (Production Ready)
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-rockfall-prediction-system.git
cd ai-rockfall-prediction-system

# Start with Docker Compose
cd deployment
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option 3: Cloud Deployment

#### AWS Deployment
```bash
# Using AWS ECS/Fargate
aws ecs create-cluster --cluster-name rockfall-prediction
aws ecs create-service --cluster rockfall-prediction --service-name rockfall-api

# Using AWS Elastic Beanstalk
eb init rockfall-prediction-system
eb create production
eb deploy
```

#### Google Cloud Platform
```bash
# Using Google Cloud Run
gcloud run deploy rockfall-api --source .
gcloud run deploy rockfall-frontend --source ./frontend
```

#### Azure Deployment
```bash
# Using Azure Container Instances
az container create --resource-group rockfall-rg --name rockfall-system
```

## Environment Configuration

### Production Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/rockfall_db

# Security
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production

# Alert System
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
SENDGRID_API_KEY=your_sendgrid_key

# External APIs
WEATHER_API_KEY=your_weather_api_key
```

### SSL/HTTPS Setup
```nginx
# Nginx configuration
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

## Monitoring and Maintenance

### Health Checks
```bash
# API health
curl https://your-domain.com/api/health

# System status
curl https://your-domain.com/api/system-status
```

### Log Management
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs
tail -f logs/application.log
tail -f logs/error.log
```

### Database Backup
```bash
# PostgreSQL backup
pg_dump rockfall_db > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump rockfall_db > $BACKUP_DIR/rockfall_backup_$DATE.sql
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple backend instances
- Shared database and Redis cache
- CDN for static assets

### Performance Optimization
- Database indexing
- Redis caching
- API rate limiting
- Image optimization
- Gzip compression

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Database access restricted
- [ ] API rate limiting implemented
- [ ] Input validation enabled
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] Monitoring and alerting configured

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find and kill process
netstat -tulpn | grep :5000
kill -9 <PID>
```

#### Database Connection Issues
```bash
# Check database status
systemctl status postgresql
docker-compose logs postgres
```

#### Memory Issues
```bash
# Monitor resource usage
docker stats
htop
```

### Support

- Check [Issues](https://github.com/YOUR_USERNAME/ai-rockfall-prediction-system/issues)
- Review [Documentation](README.md)
- Join [Discussions](https://github.com/YOUR_USERNAME/ai-rockfall-prediction-system/discussions)

---

**Deploy safely and monitor continuously! 🚀🔒**