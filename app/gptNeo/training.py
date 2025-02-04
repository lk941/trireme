from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

# Load your training data
data = pd.read_csv("test_case_training_data.csv")  # Columns: "Input Type", "Input", "Output"

# Combine input and output into a single text column
data["text"] = data.apply(
    lambda row: f"Task: {row['Input Type']}\nInput: {row['Input']}\nOutput: {row['Output']}",
    axis=1
)

# Load tokenizer and model
model_name = "EleutherAI/gpt-neo-1.3B"  # Use a smaller model if resources are limited
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare dataset
train_dataset = Dataset.from_pandas(data)

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512)

tokenized_train = train_dataset.map(preprocess_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=1,  # Adjust based on GPU memory
    num_train_epochs=3,
    save_steps=500,
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine_tuned_gpt_neo_test_cases")
tokenizer.save_pretrained("./fine_tuned_gpt_neo_test_cases")