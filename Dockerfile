# Use official Python base image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy the dependencies file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Start the main Python application
CMD ["python", "main.py"]
