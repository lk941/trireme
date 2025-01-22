from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
import pandas as pd
import json
import os
from openai import OpenAI
from docx import Document
import tempfile
from pathlib import Path
import openpyxl
from dotenv import load_dotenv
import threading
import uvicorn
from openpyxl import load_workbook
import logging

# Load environment variables
load_dotenv()

# step 1 find a way to make the excel anonymisation work (/)
# step 2 make sure excel to test script by gpt works (/)

# Freedom sprint: Finish UI pages on wednesday, and streamline anonymisation -> generation -> De-anonymisation
# step 3 do up database, make sure db upload and storage works
# step 4 create functions to retrieve and craft better prompt
# step 5 link to AI and test


# Initialize OpenAI API client
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # Replace with your API key

# Initialize FastAPI app
app = FastAPI()
# Determine environment
CONFIG_MODE = os.getenv("CONFIG_MODE", "local")  # Default to 'local'
BASE_DIR = Path(__file__).resolve().parent

# Define file paths based on environment
if CONFIG_MODE == "docker":
    STATIC_DIR = BASE_DIR / "templates"
    TEMPLATE_PATH = BASE_DIR / "testdata" / "DPP2_Template.xlsx"
    OUTPUT_PATH = BASE_DIR / "generateddata" / "updated_test_cases.xlsx"
    print(TEMPLATE_PATH)
else:
    STATIC_DIR = BASE_DIR / "templates"
    TEMPLATE_PATH = BASE_DIR / "testdata" / "DPP2_Template.xlsx"
    OUTPUT_PATH = BASE_DIR / "generateddata" / "updated_test_cases.xlsx"
    print(TEMPLATE_PATH)
    
print(f"Running in {CONFIG_MODE} mode")

logging.basicConfig(level=logging.DEBUG)

app.mount("/frontend", StaticFiles(directory="../frontend/dist", html=True), name="static")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000", "http://localhost:4200", "127.0.0.1:*"],  # Adjust the origin as needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

class TestConnectionPayload(BaseModel):
    message: str

@app.post("/test-connection")
async def test_connection(payload: TestConnectionPayload):
    logging.debug(f"Payload: {payload}")
    print(f"Received message: {payload.message}")
    return {"message": f"Message received: {payload.message}"}

# Function to load JSON files
def load_request_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# # Endpoint to load HTML UI
# @app.get("/", response_class=HTMLResponse)
# async def get_ui():
#     with open(BASE_DIR / "templates" / "index.html") as f:
#         return HTMLResponse(content=f.read())

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
        excel_file_path = template_excel(test_scripts, TEMPLATE_PATH, OUTPUT_PATH)

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
            {"role": "user", "content": (
            f"Generate test scripts for the following document:\n\n{document_text}. "
            "Limit your response to only the test script contents in JSON format. "
            "Return the test cases as a JSON array (list) with each test case containing the following attributes: "
            "Test Case ID, Test Case Name, Pre-Condition, Actor(s), Test Data, Step Description, and Expected Result. "
            "Do not include any additional text, just the JSON array in text."
            )}
        ]
    )
    output = response.choices[0].message.content
    
    # Remove the ```json and ``` delimiters if present
    if output.startswith("```json"):
        output = output[7:]  # Remove the initial ```json
    if output.endswith("```"):
        output = output[:-3]  # Remove the closing ``
    
    print(output)
    
    try:
        # Parse the JSON response
        test_cases = json.loads(output)
        return test_cases  # Return the list of test case dictionaries
    except json.JSONDecodeError:
        raise ValueError("The API response is not valid JSON. Ensure the prompt enforces proper JSON formatting.")

def template_excel(test_cases: list, template_path: str, output_path: str):
    
    # Load the Excel workbook and select the active sheet
    workbook = load_workbook(template_path)
    sheet = workbook.active  # Replace with sheet name if not the active one

    # Starting row for the test cases
    start_row = 42
    
    # Iterate through the test cases and write to the Excel sheet
    for i, test_case in enumerate(test_cases):
        row = start_row + i  # Determine the row for each test case
        
        # Write test case values to the sheet in the expected column order
        sheet.cell(row=row, column=1).value = test_case.get("Test Case ID", "")
        sheet.cell(row=row, column=2).value = test_case.get("Test Case Name", "")
        sheet.cell(row=row, column=3).value = test_case.get("Pre-Condition", "")
        sheet.cell(row=row, column=4).value = test_case.get("Actor(s)", "")
        sheet.cell(row=row, column=5).value = test_case.get("Test Data", "")
        sheet.cell(row=row, column=6).value = test_case.get("Step Description", "")
        sheet.cell(row=row, column=7).value = test_case.get("Expected Result", "")
    
    # Save the updated workbook to the output path
    # workbook.save(output_path)
    # print(f"Test cases successfully transferred to {output_path}.")
    
    temp_dir = tempfile.mkdtemp()
    excel_file_path = os.path.join(temp_dir, "test-scripts.xlsx")
    workbook.save(excel_file_path)
    return excel_file_path
