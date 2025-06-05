# Use the official lightweight Python image
FROM python:3.13-slim

COPY ./requirements.txt /app/requirements.txt

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app

# Expose port 5000 for Flask
EXPOSE 5000

# Set the default command to run the Flask app
CMD ["python", "app.py"]