# papers.py — FastAPI routes for paper upload and retrieval
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import get_db
from backend.services.research_parser.paper_service import (
    save_uploaded_pdf,
    process_paper,
    get_all_papers,
    get_paper_by_id,
    delete_paper,
    get_research_gap_analysis,
)

router = APIRouter(prefix="/papers", tags=["Research Papers"])


@router.post("/upload")
async def upload_paper(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse a research paper PDF."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    if file.size and file.size > 50 * 1024 * 1024:  # 50MB limit
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")

    try:
        content = await file.read()
        file_path = save_uploaded_pdf(content, file.filename)
        paper = process_paper(file_path, db)

        return {
            "message": "Paper uploaded and parsed successfully",
            "paper_id": paper.id,
            "title": paper.title,
            "algorithms_found": paper.algorithms_used,
            "datasets_found": paper.datasets_used,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def list_papers(db: Session = Depends(get_db)):
    """Get all uploaded papers."""
    papers = get_all_papers(db)
    return [
        {
            "id": p.id,
            "title": p.title,
            "authors": p.authors,
            "keywords": p.keywords,
            "algorithms_used": p.algorithms_used,
            "datasets_used": p.datasets_used,
            "uploaded_at": p.uploaded_at,
        }
        for p in papers
    ]


@router.get("/gaps")
def research_gaps(db: Session = Depends(get_db)):
    """Analyze all papers and return research gap insights."""
    return get_research_gap_analysis(db)


@router.get("/{paper_id}")
def get_paper(paper_id: str, db: Session = Depends(get_db)):
    """Get full details of a specific paper."""
    paper = get_paper_by_id(paper_id, db)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@router.delete("/{paper_id}")
def remove_paper(paper_id: str, db: Session = Depends(get_db)):
    """Delete a paper."""
    success = delete_paper(paper_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper deleted successfully"}