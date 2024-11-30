from .database import engine, Base
from .models import TestScripts

# Create all tables
Base.metadata.create_all(bind=engine)
