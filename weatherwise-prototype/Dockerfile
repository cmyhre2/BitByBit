# Use official Python slim image
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy backend code into container
COPY backend/ ./backend/

# Change to backend directory
WORKDIR /app/backend

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask/Gunicorn
EXPOSE 5000

# Run with gunicorn in production mode
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2", "--threads", "4", "--log-level", "info"]