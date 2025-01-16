import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, MandatoryTestCase, Project
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def create_project(session, name, description):
    try:
        new_project = Project(
            name=name,
            description=description,
            created_at=datetime.now,
            updated_at=datetime.now
        )
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        print(f"Project '{name}' created successfully with ID {new_project.id}.")
        return {"id": new_project.id, "name": new_project.name, "description": new_project.description}
    except Exception as e:
        session.rollback()
        print(f"Error creating project: {e}")
        return None


# Read Excel file
def upload_mandatory_test_cases(project_id, file_path):
    # Create a new database session
    session = SessionLocal()

    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Iterate through rows and add test cases to the database
        for _, row in df.iterrows():
            test_case = MandatoryTestCase(
                project_id=project_id,
                test_case_id=row["Test Case ID"],
                test_case_name=row["Test Case Name"],
                pre_condition=row.get("Pre-Condition", ""),
                actors=row.get("Actor(s)", ""),
                test_data=row.get("Test Data", ""),
                step_description=row["Step Description"],
                expected_result=row["Expected Result"],
            )
            session.add(test_case)

        # Commit the transaction
        session.commit()
        print(f"Successfully uploaded test cases for project ID {project_id}.")

    except Exception as e:
        # Roll back the transaction in case of error
        session.rollback()
        print(f"Failed to upload test cases: {e}")

    finally:
        # Close the session
        session.close()
        
        
#     
def get_mandatory_test_cases(session, project_id):
    try:
        # Fetch the test cases associated with the project
        test_cases = session.query(MandatoryTestCase).filter_by(project_id=project_id).all()

        if not test_cases:
            return f"No mandatory test cases found for project ID {project_id}."

        # Format test cases into a prompt-friendly string
        prompt = f"Mandatory Test Cases for Project ID {project_id}:\n\n"
        for test_case in test_cases:
            prompt += (
                f"Test Case ID: {test_case.test_case_id}\n"
                f"Name: {test_case.test_case_name}\n"
                f"Pre-Condition: {test_case.pre_condition or 'None'}\n"
                f"Actor(s): {test_case.actors or 'None'}\n"
                f"Test Data: {test_case.test_data or 'None'}\n"
                f"Step Description: {test_case.step_description}\n"
                f"Expected Result: {test_case.expected_result}\n\n"
            )
        return prompt
    except Exception as e:
        print(f"Error retrieving test cases: {e}")
        return None
