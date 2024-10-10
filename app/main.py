from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
import os

app = FastAPI()

# Load the tokenizer and model
tokenizer = MistralTokenizer.from_file("/root/mistral_models/Nemo-Instruct/tokenizer.model.v3")
model = Transformer.from_folder("/root/mistral_models/Nemo-Instruct")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_model(request: QueryRequest):
    # Create chat completion request
    completion_request = ChatCompletionRequest(messages=[UserMessage(content=request.question)])
    # Encode message
    tokens = tokenizer.encode_chat_completion(completion_request).tokens
    # Generate response
    out_tokens, _ = generate([tokens], model, max_tokens=64, temperature=0.0, eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id)
    # Decode the output
    result = tokenizer.instruct_tokenizer.tokenizer.decode(out_tokens[0])
    return {"response": result}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return f.read()
