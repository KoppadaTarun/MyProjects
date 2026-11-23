from app.services.rag_service import ask_question


result = ask_question(
    question=(
        "What is the approved marketing budget "
        "and how much has been spent?"
    ),
    departments=["Finance", "Marketing"]
)

print("\nQUESTION:")
print(result["question"])

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nSOURCES:")
for source in result["sources"]:
    print(source)

print("\nRETRIEVED CHUNKS:")
print(result["retrieved_chunks"])