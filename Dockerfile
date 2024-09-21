# Base image with Python
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    xvfb \
    chromium \
    chromium-driver

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 3000

# Command to run the Flask app
CMD ["python", "main.py"]
