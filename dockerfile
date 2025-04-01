# Use an official Python image with the correct version
FROM python:3.10  

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project
COPY . .

# Expose port 8000
EXPOSE 8000

# Run Gunicorn to start the Django app
CMD ["gunicorn", "ecommerce.wsgi", "--bind", "0.0.0.0:8000"]
