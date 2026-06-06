# init_db.py — run once to create all tables
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.database import engine, Base
from backend.models.schemas import User, ResearchPaper, Experiment, KnowledgeGraphEdge

def init_database():
    print("Creating all database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! Tables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")

if __name__ == "__main__":
    init_database()