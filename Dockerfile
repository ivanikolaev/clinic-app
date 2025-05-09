# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=clinic.settings
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
# Remove PostgreSQL dependency since we're using SQLite
RUN grep -v "psycopg2" requirements.txt > requirements_sqlite.txt && \
    pip install --no-cache-dir -r requirements_sqlite.txt && \
    pip install gunicorn whitenoise

# Copy project
COPY . /app/

# Create media and static directories
RUN mkdir -p /app/media /app/staticfiles

# Expose port
EXPOSE $PORT

# Create a startup script for production
RUN echo '#!/bin/bash\n\
# Collect static files\n\
python manage.py collectstatic --noinput\n\
# Apply migrations\n\
python manage.py migrate\n\
# Populate database if it is empty\n\
python manage.py populate_db\n\
# Start server with gunicorn\n\
gunicorn clinic.wsgi:application --bind 0.0.0.0:$PORT --workers 2\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]