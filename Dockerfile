# Use a lightweight Python base image to keep the artifact size small
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker layer caching
# This ensures that dependencies are not re-installed unless requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src

# Ensure the 'src' package is discoverable by Python
ENV PYTHONPATH=/app

# Expose the port that the Flask app runs on
EXPOSE 5000

# Define the entry point command to start the service
CMD ["python", "src/app.py"]