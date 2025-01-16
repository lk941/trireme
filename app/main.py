from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
import pandas as pd
import json
import os
from openai import OpenAI
from docx import Document
import pandas as pd
import tempfile
from pathlib import Path
import openpyxl
from dotenv import load_dotenv
import threading
import uvicorn

# Load environment variables
load_dotenv()

# step 1 find a way to make the excel anonymisation work (/)
# step 2 make sure excel to test script by gpt works (/)
# step 3 do up database, make sure db upload and storage works
# step 4 create functions to retrieve and craft better prompt
# step 5 link to AI and test
# step 6 get UI up
print(os.environ.get("OPENAI_API_KEY"))

# Initialize OpenAI API client
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # Replace with your API key

# Initialize FastAPI app
app = FastAPI()
# Determine environment
CONFIG_MODE = os.getenv("CONFIG_MODE", "local")  # Default to 'local'
BASE_DIR = Path(__file__).resolve().parent

# Define file paths based on environment
if CONFIG_MODE == "docker":
    STATIC_DIR = BASE_DIR / "app" / "templates"
else:
    STATIC_DIR = BASE_DIR / "templates"
    
print(f"Running in {CONFIG_MODE} mode")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Adjust the origin as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to load JSON files
def load_request_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Endpoint to load HTML UI
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open(BASE_DIR / "templates" / "index.html") as f:
        return HTMLResponse(content=f.read())

# Function to run the FastAPI server
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    print("upload backend triggered")
    try:
        # Save uploaded file to temporary directory
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        test_scripts = ""
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        if (file.filename.split('.').pop().lower() == ".docx"):
            # Extract text from the Word document
            document_text = extract_text_from_docx(file_path)

            # Generate test scripts using OpenAI
            test_scripts = await generate_test_scripts(document_text)
        else:
            # Extract text from the Word document
            document_text = extract_excel_content(file_path)

            # Generate test scripts using OpenAI
            test_scripts = await generate_test_scripts(document_text)

        # Generate Excel file with test scripts
        excel_file_path = generate_excel_file(test_scripts)

        # Send the Excel file as a response
        return FileResponse(excel_file_path, filename="test-scripts.xlsx")
    finally:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)

# Extract text from a Word document
def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_excel_content(file_path):
    try:
        # Load the workbook
        workbook = openpyxl.load_workbook(file_path, data_only=True)

        output = []

        # Iterate through all sheets
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            output.append(f"\n### Sheet: {sheet_name} ###\n")

            # Iterate through rows and columns
            for row in sheet.iter_rows(values_only=True):
                row_content = "\t".join(str(cell) if cell is not None else "" for cell in row)
                output.append(row_content)

        return "\n".join(output)

    except Exception as e:
        return f"Error reading Excel file: {str(e)}"

# Query OpenAI to generate test scripts
async def generate_test_scripts(document_text: str) -> list:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Replace with your model
        messages=[
            {"role": "system", "content": "You are an assistant that generates software test scripts."},
            {"role": "user", "content": f"Generate test scripts for the following document:\n\n{document_text}. Limit your response to the test script contents only."}
        ]
    )
    output = response.choices[0].message.content
    # Convert output into a list of test cases
    return [{"Test Script": line.strip()} for line in output.split("\n") if line.strip()]

# Generate Excel file from test scripts
def generate_excel_file(test_scripts: list) -> str:
    df = pd.DataFrame(test_scripts)
    temp_dir = tempfile.mkdtemp()
    excel_file_path = os.path.join(temp_dir, "test-scripts.xlsx")
    df.to_excel(excel_file_path, index=False)
    return excel_file_path
