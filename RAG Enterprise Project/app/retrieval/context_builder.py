
def build_context(
    chunks: list[dict],
    max_chunks: int = 5,
    max_context_chars: int = 12000
) -> str:

    if not chunks:
        return ""

    context_parts = []
    seen_chunks = set()
    total_chars = 0

    for index, chunk in enumerate(chunks, start=1):

        text = chunk["text"].strip()

        if not text:
            continue

        # Remove duplicate content
        normalized_text = " ".join(text.lower().split())

        if normalized_text in seen_chunks:
            continue

        metadata = chunk["metadata"]

        document_name = metadata.get(
            "document_name", "Unknown document"
        )

        department = metadata.get(
            "department", "Unknown department"
        )

        page_number = metadata.get("page_number", -1)

        # Build source information
        source = (
            f"[Source: {document_name} | "
            f"Department: {department}"
        )

        if page_number != -1:
            source += f" | Page: {page_number}"

        source += "]"

        chunk_content = (
            f"Context {len(context_parts) + 1}\n"
            f"{source}\n"
            f"{text}"
        )

        # Respect context character limit
        if total_chars + len(chunk_content) > max_context_chars:
            break

        context_parts.append(chunk_content)

        seen_chunks.add(normalized_text)

        total_chars += len(chunk_content)

        if len(context_parts) >= max_chunks:
            break

    return "\n\n".join(context_parts)
