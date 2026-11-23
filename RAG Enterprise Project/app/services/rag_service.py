from app.retrieval.retrieval_pipeline import retrieve_context
from app.generation.response_generator import generate_answer


def ask_question(
    question: str,
    departments: list[str]
) -> dict:

    retrieval_result = retrieve_context(
        question=question,
        departments=departments,
        top_k=5,
        candidate_k=15
    )

    context = retrieval_result["context"]

    if not context.strip():
        return {
            "question": question,
            "answer": (
                "I couldn't find relevant information "
                "in the company knowledge base."
            ),
            "sources": [],
            "retrieved_chunks": 0
        }

    answer = generate_answer(
        question=question,
        context=context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": retrieval_result["sources"],
        "retrieved_chunks": retrieval_result["retrieved_chunks"]
    }