# Use official Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable (optional)
ENV FLASK_ENV=production

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "run.py"]
