# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first (for better caching)
COPY requirements.txt /app

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Download default SpaCy model if needed
RUN python -m spacy download en_core_web_sm

# Copy the rest of the code
COPY . /app

# Expose the port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=5000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]