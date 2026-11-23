
from pathlib import Path

from app.database.connection import SessionLocal
from app.database.models import Document, Department, User
from app.services.document_indexing_service import index_document


BASE_DIR = Path(__file__).resolve().parent

SAMPLE_DOCUMENTS_DIR = BASE_DIR / "data" / "sample_documents"

DEPARTMENTS = {
    "hr": "HR",
    "finance": "Finance",
    "marketing": "Marketing",
    "engineering": "Engineering",
    "operations": "Operations"
}

db = SessionLocal()


def register_and_index_documents():

    try:
        # Find an existing user to associate with uploads
        user = db.query(User).first()

        if not user:
            print("No user found in SQLite.")
            print("Register a user before indexing documents.")
            return

        total_indexed = 0
        total_failed = 0

        for folder_name, department_name in DEPARTMENTS.items():

            folder_path = SAMPLE_DOCUMENTS_DIR / folder_name

            if not folder_path.exists():
                print(f"Missing folder: {folder_path}")
                continue

            department = db.query(Department).filter(
                Department.name == department_name
            ).first()

            if not department:
                print(f"Department not found: {department_name}")
                continue

            files = [
                file for file in folder_path.iterdir()
                if file.is_file() and file.suffix.lower() in {
                    ".pdf", ".docx", ".txt", ".csv"
                }
            ]

            for file_path in files:

                print(f"\nProcessing: {file_path.name}")

                try:
                    resolved_path = str(file_path.resolve())

                    # Avoid creating duplicate records
                    document = db.query(Document).filter(
                        Document.file_path == resolved_path
                    ).first()

                    if document:
                        print("Document record already exists.")
                    else:
                        document = Document(
                            filename=file_path.name,
                            file_path=resolved_path,
                            file_type=file_path.suffix.lower().lstrip("."),
                            status="uploaded",
                            department_id=department.id,
                            uploaded_by=user.id
                        )

                        db.add(document)
                        db.commit()
                        db.refresh(document)

                    # Index document into ChromaDB
                    result = index_document(
                        document_id=document.id,
                        db=db
                    )

                    print("Successfully indexed:", result)
                    total_indexed += 1

                except Exception as error:
                    db.rollback()
                    print(f"Failed: {file_path.name}")
                    print("Error:", error)
                    total_failed += 1

        print("\n========== INDEXING SUMMARY ==========")
        print("Successfully indexed:", total_indexed)
        print("Failed:", total_failed)

    finally:
        db.close()


if __name__ == "__main__":
    register_and_index_documents()
