import chromadb
from sentence_transformers import SentenceTransformer
from backend.config import settings

# using a lightweight model that runs fine on cpu
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_client = None
_collection = None


def get_model():
    global _model
    if _model is None:
        print("loading sentence transformer model...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        _collection = _client.get_or_create_collection(
            name="research_papers",
            metadata={"hnsw:space": "cosine"}
        )
    return _collection


def add_paper_to_vectorstore(paper_id: str, title: str, abstract: str, keywords: list):
    # combine the most important fields for a good embedding
    text = f"{title}. {abstract}. {' '.join(keywords or [])}"

    model = get_model()
    collection = get_collection()

    embedding = model.encode(text).tolist()

    collection.upsert(
        ids=[paper_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"title": title, "paper_id": paper_id}]
    )
    print(f"added to vector store: {title}")


def search_similar_papers(query: str, n_results: int = 5) -> list:
    model = get_model()
    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count())
    )

    papers = []
    for i, paper_id in enumerate(results["ids"][0]):
        papers.append({
            "paper_id": paper_id,
            "title": results["metadatas"][0][i].get("title", ""),
            "similarity_score": round(1 - results["distances"][0][i], 3),
            "excerpt": results["documents"][0][i][:300],
        })

    return papers


def get_vectorstore_count() -> int:
    return get_collection().count()