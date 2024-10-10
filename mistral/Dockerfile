# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Install required dependencies
RUN pip install torch transformers mistral_inference mistral_common

# Download the Mistral model files (from the provided link)
RUN curl -L -o mistral-nemo-instruct-2407.tar https://models.mistralcdn.com/mistral-nemo-2407/mistral-nemo-instruct-2407.tar \
    && mkdir -p /root/mistral_models/Nemo-Instruct \
    && tar -xf mistral-nemo-instruct-2407.tar -C /root/mistral_models/Nemo-Instruct

# Copy the inference script (if necessary)
COPY inference-script.py .

# Set the environment variable for model path
ENV MODEL_PATH="/root/mistral_models/Nemo-Instruct"

# Run the inference script (or interactive CLI)
CMD ["python", "inference-script.py"]
