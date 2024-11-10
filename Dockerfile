# Use an official Python image as the base image
FROM python:3.9-slim

# Install Apache HTTPD and required modules for WSGI
RUN apt-get update && apt-get install -y apache2 libapache2-mod-wsgi-py3

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY app.py /app

# Install the necessary Python packages
RUN pip install --no-cache-dir flask requests pandas

# Expose the port the app will run on
EXPOSE 5000

# Set the environment variable for Flask to run in production mode
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run Apache HTTPD in the background and start the Flask app
CMD service apache2 start && python /app/app.py
