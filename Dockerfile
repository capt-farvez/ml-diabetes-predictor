# Use the official lightweight Python image
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies (gcc & musl-dev are often needed for pip builds)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    python3-dev \
    openssl-dev \
    cargo \
    && pip install --upgrade pip

# Copy requirements separately to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]