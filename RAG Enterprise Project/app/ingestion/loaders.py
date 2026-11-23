
import csv
from pathlib import Path

from pypdf import PdfReader
from docx import Document as DocxDocument


def load_document(file_path: str | Path) -> list[dict]:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(str(file_path))

        return [
            {
                "text": page.extract_text() or "",
                "page_number": index + 1
            }
            for index, page in enumerate(reader.pages)
        ]

    elif extension == ".docx":
        doc = DocxDocument(str(file_path))

        paragraphs = [
            paragraph.text
            for paragraph in doc.paragraphs
            if paragraph.text.strip()
        ]

        tables = []
        for table in doc.tables:
            for row in table.rows:
                tables.append(" | ".join(cell.text for cell in row.cells))

        text = "\n".join(paragraphs + tables)

        return [{"text": text, "page_number": None}]

    elif extension == ".txt":
        text = file_path.read_text(
            encoding="utf-8-sig",
            errors="replace"
        )

        return [{"text": text, "page_number": None}]

    elif extension == ".csv":
        rows = []

        with file_path.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                row_text = " | ".join(
                    f"{key}: {value}"
                    for key, value in row.items()
                    if value is not None
                )
                rows.append(row_text)

        text = "\n".join(rows)

        return [{"text": text, "page_number": None}]

    else:
        raise ValueError(f"Unsupported file format: {extension}")
