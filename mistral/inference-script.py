from mistral_inference import MistralInference
from pathlib import Path

# Set model path
model_path = Path("/root/mistral_models/Nemo-Instruct")

# Load model
mistral_model = MistralInference.from_pretrained(model_path)

# Run inference (example input)
prompt = "Tell me about Mistral AI."
output = mistral_model.generate(prompt)
print(output)
