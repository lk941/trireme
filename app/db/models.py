from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class TestScripts(Base):
    __tablename__ = "test_scripts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    script_content = Column(String)
    
class MandatoryTestCase(Base):
    __tablename__ = "mandatory_test_cases"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incremented ID
    test_case_id = Column(String, unique=True, nullable=False, index=True)  # ID from Excel
    test_case_name = Column(String, nullable=False)  # Name of the test case
    pre_condition = Column(Text, nullable=True)  # Pre-condition description
    actors = Column(String, nullable=True)  # Roles or entities involved
    test_data = Column(Text, nullable=True)  # Input data for the test
    step_description = Column(Text, nullable=False)  # Steps for the test
    expected_result = Column(Text, nullable=False)  # Expected outcome
    created_at = Column(DateTime)  # Timestamp

    
class SoftwareChangeRequests(Base):
    __tablename__ = "software_change_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True) 
    name = Column(String, nullable=False, index=True)  # Test case name
    description = Column(Text, nullable=False)  # Detailed test steps
    contents = Column(Text, nullable=False) 
    created_at = Column(DateTime)
    