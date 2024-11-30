#!/bin/bash
set -e  # Exit on error

# Start the Ollama server in the foreground
echo "Starting Ollama server..."
exec ollama serve

sleep 10

# Pull the mistral model
echo "Pulling mistral model..."
exec ollama pull mistral

