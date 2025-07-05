FROM python:3.11

WORKDIR /app

# Copy only requirements if موجود
COPY requirements.txt .  # احذف هذا السطر لو ما عندك requirements.txt

# Install dependencies if موجود
# RUN pip install --no-cache-dir -r requirements.txt  ← فقط إذا عندك ملف requirements

# Copy all project files
COPY . .

# Run main file (عدّل الاسم لو مختلف)
CMD ["python", "api_handler.py"]
