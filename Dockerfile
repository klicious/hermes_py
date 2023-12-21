# Use an official Python runtime as a parent image
FROM python:3.11.2-slim

# Set the working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl libpq-dev gcc


# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

