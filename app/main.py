from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import requests
import json
import os

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

# /query route function
@app.post("/query")
async def query_model(request: QueryRequest):
    print("Received request for /query")  # Debug log

    # Set up the request
    url = "http://ollama:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": f"{request.question}"
    }
    headers = {"Content-Type": "application/json"}

    # Send the request with `stream=True` to handle the streamed response
    response = requests.post(url, json=payload, headers=headers, stream=True)
    responses = []

    # Process each line as a separate JSON object
    for line in response.iter_lines():
        if line:
            line_data = line.decode('utf-8')
            try:
                json_line = json.loads(line_data)
                response_text = json_line.get("response", "")
                responses.append(response_text)
                print("Partial response:", response_text)  # Print each part
            except ValueError:
                print("Error parsing JSON line:", line_data)

    full_response = "".join(responses)
    print("Full response for /query:\n", full_response)  # Print final response
    return {"response": full_response}

# /generate route function
# @app.post("/generate")
# async def generate_test_data(request: QueryRequest):
#     print("Received request for /generate")  # Debug log

#     # Read and process Excel file
#     file_path = "app/testdata/Software_Change_Request_ID_Generation.xlsx"
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")
#     df = pd.read_excel(file_path, sheet_name="Software Change Request")
#     data_as_text = df.to_csv(index=False)
#     print("Excel data processed for /generate")  # Log data processing

#     # Set up the request
#     url = "http://ollama:11434/api/generate"
#     payload = {
#         "model": "mistral",
#         "prompt": f"Based on the following data, please generate sample test data and the expected IDs:\n{data_as_text}"
#     }
#     headers = {"Content-Type": "application/json"}

#     response = requests.post(url, json=payload, headers=headers, stream=True)
#     responses = []

#     # Process each line as a separate JSON object
#     for line in response.iter_lines():
#         if line:
#             line_data = line.decode('utf-8')
#             try:
#                 json_line = json.loads(line_data)
#                 response_text = json_line.get("response", "")
#                 responses.append(response_text)
#                 print("Partial response for /generate:", response_text)  # Log each part
#             except ValueError:
#                 print("Error parsing JSON line:", line_data)

#     full_response = "".join(responses)
#     print("Full response for /generate:\n", full_response)  # Log final response
#     return {"response": full_response}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    file_path = "app/templates/index.html"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    with open(file_path) as f:
        content = f.read()
    print("Served index.html")  # Debug log for the HTML page
    return content
