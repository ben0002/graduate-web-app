# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy and install FastAPI project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the FastAPI app source code to the container
COPY . .

# Change the working directory to a subdirectory within your app
WORKDIR /app/fastAPI

# Expose a port (e.g., 8000) for the FastAPI app to run
EXPOSE 80

# Command to start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]