FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY flask/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY flask/ .

# Expose port
EXPOSE 5005

# Environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "main.py"]