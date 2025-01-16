FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application files into the container
COPY ./app ./app

# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH=/app

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
