from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.services.vector_store.embeddings import (
    search_similar_papers,
    get_vectorstore_count
)
from backend.services.knowledge_graph.graph_service import (
    get_graph_data,
    get_graph_stats
)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.get("/search")
def semantic_search(
    query: str = Query(..., description="search query"),
    n_results: int = Query(5, description="number of results"),
    db: Session = Depends(get_db)
):
    results = search_similar_papers(query, n_results)
    return {
        "query": query,
        "results": results,
        "total_found": len(results)
    }


@router.get("/graph")
def knowledge_graph(db: Session = Depends(get_db)):
    return get_graph_data(db)


@router.get("/graph/stats")
def graph_stats(db: Session = Depends(get_db)):
    return get_graph_stats(db)


@router.get("/stats")
def vectorstore_stats():
    return {"papers_indexed": get_vectorstore_count()}