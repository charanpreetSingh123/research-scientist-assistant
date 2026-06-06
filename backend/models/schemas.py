from sqlalchemy import Column, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.models.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    papers = relationship("ResearchPaper", back_populates="owner")
    experiments = relationship("Experiment", back_populates="owner")


class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(500), nullable=False)
    authors = Column(JSON)
    abstract = Column(Text)
    keywords = Column(JSON)
    problem_statement = Column(Text)
    methodology = Column(Text)
    datasets_used = Column(JSON)
    algorithms_used = Column(JSON)
    evaluation_metrics = Column(JSON)
    results = Column(Text)
    limitations = Column(Text)
    future_work = Column(Text)
    file_path = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)  # nullable, no auth yet

    owner = relationship("User", back_populates="papers")


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    dataset_name = Column(String(200))
    problem_type = Column(String(50))
    models_trained = Column(JSON)
    best_model = Column(String(100))
    best_score = Column(Float)
    metrics = Column(JSON)
    feature_importance = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="pending")
    report_path = Column(String)
    owner_id = Column(String, ForeignKey("users.id"), nullable=True)  # nullable, no auth yet

    owner = relationship("User", back_populates="experiments")


class KnowledgeGraphEdge(Base):
    __tablename__ = "knowledge_graph_edges"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_type = Column(String(50))
    source_id = Column(String(200))
    target_type = Column(String(50))
    target_id = Column(String(200))
    relationship = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())