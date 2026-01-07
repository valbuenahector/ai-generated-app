# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app/app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV PORT 5000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port 5000 (standard for vK8s lab environment)
EXPOSE 5000

# Run the application
# Using flask run for lab simplicity as requested
CMD ["flask", "run", "--port", "5000"]
