# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (not required for Render but good practice)
EXPOSE 8080

# Run Flask app
CMD ["python", "app.py"]
