from app.vectorstore.chroma_client import chroma_client

DEPARTMENTS = {
    "HR": "hr_knowledge",
    "Finance": "finance_knowledge",
    "Marketing": "marketing_knowledge",
    "Engineering": "engineering_knowledge",
    "Operations": "operations_knowledge"
}


def get_collection(department: str):
    collection_name = DEPARTMENTS.get(department)

    if not collection_name:
        raise ValueError(f"Invalid department: {department}")

    return chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )


def initialize_collections():
    for department in DEPARTMENTS:
        get_collection(department)

    print("All department collections initialized!")