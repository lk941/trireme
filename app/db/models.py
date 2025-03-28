from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ForeignKeyConstraint, UniqueConstraint, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)  # Unique project ID
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship to modules
    modules = relationship("Module", back_populates="project")
    suites = relationship("Suite", back_populates="project")
    

# script content here refers to mandatory steps for module
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)  # Global unique module ID
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)  
    project_specific_id = Column(Integer, index=True)  # Sequential within project

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    script_content = Column(JSON, nullable=True)
    scr_update = Column(JSON, nullable=True)
    
    project = relationship("Project", back_populates="modules")

    # Ensure (project_id, project_specific_id) is unique
    __table_args__ = (
        UniqueConstraint("project_id", "project_specific_id", name="uq_project_specific_id"),
    )

# script content here is for script versions, etc SCR docs or optimised mandatory steps
class TestScripts(Base):
    __tablename__ = "test_scripts"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), index=True)  
    module_specific_id = Column(Integer, index=True)  # Sequential within project
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    script_content = Column(JSON, nullable=True)
    
    
class Suite(Base):
    __tablename__ = "suites"

    id = Column(Integer, primary_key=True, index=True)  # Global unique module ID
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)  
    project_specific_id = Column(Integer, index=True)  # Sequential within project

    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    script_content = Column(JSON, nullable=True)
    
    project = relationship("Project", back_populates="suites")
    
    # Ensure (project_id, project_specific_id) is unique
    __table_args__ = (
        UniqueConstraint("project_id", "project_specific_id", name="uq_suite_project_specific_id"),
    )
    

class SoftwareChangeRequest(Base):
    __tablename__ = "software_change_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)  
    module_id = Column(Integer, ForeignKey("modules.id"), index=True)  

    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    contents = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
