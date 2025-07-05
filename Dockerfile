# Use official Python base image
FROM python:3.11

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY main/ ./main

# Set default command
CMD ["python", "main/app.py"]
