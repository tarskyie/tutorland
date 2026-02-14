# Deployment Guide for Render.com

This guide will help you deploy the newcubebackend Django application to Render.com.

## Prerequisites

- A Render.com account
- Git repository with your code pushed
- A GitHub/GitLab account connected to Render

## Deployment Steps

### 1. Generate a Secret Key

For production, generate a new SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Create a Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub/GitLab repository
4. Fill in the service details:
   - **Name**: `newcubebackend`
   - **Environment**: Python 3
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn newcubebackend.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Set Environment Variables

In the Render dashboard, add the following environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `DEBUG` | `False` | Disable debug mode in production |
| `SECRET_KEY` | `<generated-key>` | Your generated secret key |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` | Your deployed domain |
| `CORS_ALLOWED_ORIGINS` | `https://yourdomain.onrender.com` | Allowed CORS origins |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.onrender.com` | Allowed CSRF origins |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |
| `SECURE_HSTS_SECONDS` | `31536000` | HSTS max age (1 year) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True` | Include subdomains in HSTS |
| `SECURE_HSTS_PRELOAD` | `True` | Enable HSTS preload |
| `SESSION_COOKIE_SECURE` | `True` | Secure session cookies |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF cookies |

### 4. (Optional) Database Configuration

Currently, the project uses SQLite. For production with persistent data, you may want to:

1. Create a PostgreSQL database on Render
2. Set the `DATABASE_URL` environment variable
3. The settings.py already supports this via dj-database-url

### 5. Deploy

Once you've set the environment variables, click "Create Web Service" to deploy.

Render will:
1. Pull your repository
2. Install dependencies from requirements.txt
3. Run the build script (build.sh):
   - Install dependencies
   - Collect static files
   - Run migrations
4. Start the gunicorn server

## Important Notes

- **SSL Certificate**: Render automatically provides a free SSL certificate
- **Static Files**: WhiteNoise handles static file serving
- **Database**: SQLite with Render's ephemeral storage will lose data on redeploy. Consider using PostgreSQL for production.
- **Media Files**: For file uploads, consider using cloud storage (AWS S3, Cloudinary, etc.)

## Troubleshooting

### Check Logs
In the Render dashboard, click on your service and view the "Logs" tab for deployment and runtime errors.

### Common Issues

1. **Import errors**: Ensure all packages in requirements.txt are installed
2. **Static files not loading**: Run `python manage.py collectstatic` locally to test
3. **Database errors**: Check if migrations have run in the build.sh output
4. **CORS errors**: Verify CORS_ALLOWED_ORIGINS matches your frontend URL

## Monitoring

- Use Render's built-in monitoring for CPU, memory, and bandwidth usage
- Check application logs regularly for errors
- Set up error tracking with services like Sentry (optional)

## Updates

To deploy updates:
1. Commit and push changes to your repository
2. Render will automatically redeploy on new commits (if auto-deploy is enabled)

---

**For more information, visit the [Render Django Documentation](https://render.com/docs/deploy-django)**
