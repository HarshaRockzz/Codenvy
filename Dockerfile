# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=OJ.settings

# Install system dependencies for Djongo
RUN apt-get update && apt-get install -y libkrb5-dev

# Set up a directory for the Django project
RUN mkdir /app
WORKDIR /app

# Install the required Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files to the container
COPY . /app/

# Expose the port that Django will run on (if needed)
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]