from fastapi import BackgroundTasks, FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import shutil
from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field
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
# from scripts.anonymise import process_file_for_anonymization, de_anonymize_with_generated_terms

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
    
print(f"Running in {CONFIG_MODE} mode")

logging.basicConfig(level=logging.DEBUG)

app.mount("/frontend", StaticFiles(directory="../frontend/dist", html=True), name="static")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the API!"}

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open(BASE_DIR / "templates" / "index.html") as f:
        return HTMLResponse(content=f.read())

class TestConnectionPayload(BaseModel):
    message: str

@app.post("/test-connection")
async def test_connection(payload: TestConnectionPayload):
    logging.debug(f"Payload: {payload}")
    print(f"Received message: {payload.message}")
    return {"message": f"Message received: {payload.message}"}


def cleanup_files(temp_dir, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)

# @app.post("/anonymize")
# async def anonymize(
#     file: UploadFile = File(...),
#     keywords: str = Form(...),
#     background_tasks: BackgroundTasks = BackgroundTasks()
# ):
#     print("Anonymize backend triggered")
#     temp_dir = tempfile.mkdtemp()  # Create temporary directory
#     try:
#         # Save the uploaded file
#         file_path = os.path.join(temp_dir, file.filename)
#         keywords_list = keywords.split(",")
#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         # Process the file
#         excel_file_path = process_file_for_anonymization(file_path, keywords_list)

#         # Add cleanup task
#         background_tasks.add_task(cleanup_files, temp_dir, file_path)

#         # Return the file response
#         return FileResponse(
#             excel_file_path,
#             headers={"Content-Disposition": 'attachment; filename="anonymized.xlsx"'},
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
#     except Exception as e:
#         # Cleanup in case of errors
#         cleanup_files(temp_dir, file_path)
#         raise e


# @app.post("/deanonymize")
# async def deanonymize(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
#     print("Deanonymize backend triggered")
#     temp_dir = tempfile.mkdtemp()  # Create a single temporary directory
#     try:
#         # Save uploaded file to temporary directory
#         file_path = os.path.join(temp_dir, file.filename)
#         with open(file_path, "wb") as f:
#             f.write(await file.read())
        
#         # Use pandas.ExcelFile with context manager to ensure it closes
#         with pd.ExcelFile(file_path) as input_excel:
#             cover_page_df = input_excel.parse(sheet_name=0)
#             test_case_sheet_df = input_excel.parse(sheet_name=1)

#         # Process the data
#         restored_cover_page_df = de_anonymize_with_generated_terms(cover_page_df)
#         restored_test_case_sheet_df = de_anonymize_with_generated_terms(test_case_sheet_df)
        
#         # Save the deanonymized file
#         deanonymized_excel_path = os.path.join(temp_dir, "deanonymized_file.xlsx")
#         with pd.ExcelWriter(deanonymized_excel_path, engine='xlsxwriter') as writer:
#             restored_cover_page_df.to_excel(writer, sheet_name="Cover Page", index=False)
#             restored_test_case_sheet_df.to_excel(writer, sheet_name="Test Cases", index=False)

#         print(f"Deanonymized Excel file saved to {deanonymized_excel_path}.")
        
#         # Schedule cleanup of temporary files
#         background_tasks.add_task(cleanup_files, temp_dir, deanonymized_excel_path)

#         # Return the file response with correct headers
#         return FileResponse(
#             deanonymized_excel_path,
#             headers={"Content-Disposition": 'attachment; filename="deanonymized.xlsx"'},
#             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
#     except Exception as e:
#         print(f"Error: {e}")
#         raise HTTPException(status_code=500, detail="An error occurred while processing the file.")

def cleanup_temp_dir(temp_dir):
    try:
        shutil.rmtree(temp_dir)  # Removes the directory and all its contents
        print(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        print(f"Failed to clean up temporary directory: {e}")
        
# Function to load JSON files
def load_request_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

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
            
        if (file.filename.split('.').pop().lower() == "docx"):
            # Extract text from the Word document
            document_text = extract_text_from_docx(file_path)

            # Generate test scripts using OpenAI
            test_scripts = await generate_test_scripts(document_text)
        else:
            # Extract text from the Excel file
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
            
@app.post("/generate-test-cases")
async def generate_test_cases(file: UploadFile = File(...)):
    try:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        if file.filename.split('.').pop().lower() == "docx":
            document_text = extract_text_from_docx(file_path)
        else:
            document_text = extract_excel_content(file_path)
        
        test_cases = await generate_test_scripts(document_text)
        return {"test_cases": test_cases}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            

class TestCase(BaseModel):
    Test_Case_ID: str
    Test_Case_Name: str
    Pre_Condition: str
    Actor_s: str
    Test_Data: Optional[Dict[str, Union[str, List[str]]]] = None 
    Step_Description: List[str]
    Expected_Result: str


class GenerateExcelRequest(BaseModel):
    test_cases: List[TestCase]

# def template_excel(test_cases: List[TestCase], template_path: str, output_path: str) -> str:
#     workbook = load_workbook(template_path)
#     sheet = workbook.active

#     for row, test_case in enumerate(test_cases, start=2):
#         sheet.cell(row=row, column=1).value = test_case.Test_Case_ID
#         sheet.cell(row=row, column=2).value = test_case.Test_Case_Name
#         sheet.cell(row=row, column=3).value = test_case.Pre_Condition
#         sheet.cell(row=row, column=4).value = test_case.Actor_s
#         sheet.cell(row=row, column=5).value = str(test_case.Test_Data)
#         sheet.cell(row=row, column=6).value = test_case.Step_Description
#         sheet.cell(row=row, column=7).value = test_case.Expected_Result

#     workbook.save(output_path)
#     return output_path

@app.post("/generate-excel")
async def generate_excel(request: GenerateExcelRequest):
    test_cases = request.test_cases
    print("Received test cases:", test_cases)  # Log the parsed test cases
    excel_file_path = template_excel(test_cases, TEMPLATE_PATH, OUTPUT_PATH)
    return FileResponse(
        excel_file_path,
        headers={"Content-Disposition": 'attachment; filename="test-scripts.xlsx"'},
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

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
            "Test_Case_ID, Test_Case_Name, Pre_Condition, Actor_s, Test_Data, Step_Description, and Expected_Result. "
            "Do not include any additional text, just the JSON array in text."
            )}
        ]
    )
    output = response.choices[0].message.content
    
    # Remove the ```json and ``` delimiters if present
    if output.startswith("```json"):
        output = output[7:]  # Remove the initial ```json
    if output.endswith("```"):
        output = output[:-3]  # Remove the closing ```
    
    print(output)
    
    try:
        # Parse the JSON response
        test_cases = json.loads(output)
        return test_cases  # Return the list of test case dictionaries
    except json.JSONDecodeError:
        raise ValueError("The API response is not valid JSON. Ensure the prompt enforces proper JSON formatting.")

def template_excel(test_cases: List[TestCase], template_path: str, output_path: str) -> str:
    workbook = load_workbook(template_path)
    sheet = workbook.active

    for row, test_case in enumerate(test_cases, start=42):
        sheet.cell(row=row, column=1).value = test_case.Test_Case_ID
        sheet.cell(row=row, column=2).value = test_case.Test_Case_Name
        sheet.cell(row=row, column=3).value = test_case.Pre_Condition
        sheet.cell(row=row, column=4).value = test_case.Actor_s
        sheet.cell(row=row, column=5).value = str(test_case.Test_Data)
        sheet.cell(row=row, column=6).value = "\n".join(test_case.Step_Description)  # Join list into a string
        sheet.cell(row=row, column=7).value = test_case.Expected_Result
    
    # Save the updated workbook to the output path
    temp_dir = tempfile.mkdtemp()
    excel_file_path = os.path.join(temp_dir, "test-scripts.xlsx")
    workbook.save(excel_file_path)
    return excel_file_path

# Ranorex integration

# Pydantic model to validate incoming request data
class AutomationData(BaseModel):
    suite: str
    projectName: str
    websiteUrl: str
    browser: str
    testCases: list

# Helper function to call OpenAI API for generating Ranorex execution code
async def generate_execution_code(test_cases: list) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that generates Ranorex test automation scripts in C#."},
            {"role": "user", "content": (
                "Generate Ranorex-compatible C# test scripts based on the following test cases:\n\n"
                f"{json.dumps(test_cases, indent=2)}\n\n"
                "For each test case, generate a class with methods for each step. Include necessary Ranorex namespaces."
            )}
        ]
    )
    
    execution_code = response.choices[0].message.content
    return execution_code


# Function to set up the Ranorex project structure and write generated scripts
def setup_ranorex_project(data: AutomationData, execution_code: str):
    base_path = os.path.join(os.path.dirname(__file__), "RanorexProjects", data.projectName)
    modules_path = os.path.join(base_path, "Modules")
    
    # Create directories if they don't exist
    os.makedirs(modules_path, exist_ok=True)
    
    # Create a basic Ranorex project file structure
    with open(os.path.join(base_path, f"{data.projectName}.rxproj"), 'w') as project_file:
        project_file.write(f"<Project name=\"{data.projectName}\" suite=\"{data.suite}\" browser=\"{data.browser}\" url=\"{data.websiteUrl}\"></Project>")

    # Write the generated execution code to a C# file
    with open(os.path.join(modules_path, f"{data.projectName}_Tests.cs"), 'w') as script_file:
        script_file.write(execution_code)


# FastAPI endpoint to handle automation setup
@app.post("/setup-automation")
async def setup_automation(automation_data: AutomationData):
    try:
        # Generate execution code from test cases
        execution_code = await generate_execution_code(automation_data.testCases)
        
        # Setup the Ranorex project with generated files
        setup_ranorex_project(automation_data, execution_code)

        return {"message": "Ranorex project setup successfully!", "projectName": automation_data.projectName}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set up Ranorex project: {str(e)}")
