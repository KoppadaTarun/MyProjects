
from app.retrieval.retrieval_pipeline import retrieve_context


question = (
    "What is the approved marketing budget "
    "and how much has been spent?"
)

result = retrieve_context(
    question=question,
    departments=["Finance", "Marketing"],
    top_k=5,
    candidate_k=15
)

print("\nQUESTION:")
print(result["question"])

print("\nRETRIEVED CONTEXT:")
print(result["context"])

print("\nSOURCES:")

for source in result["sources"]:
    print(source)

print("\nTOTAL RETRIEVED CHUNKS:")
print(result["retrieved_chunks"])
