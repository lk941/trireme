# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required Python packages
RUN pip install --no-cache-dir fastapi httpx uvicorn jinja2 python-multipart 

# Copy the FastAPI application files
COPY ./app ./app

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]