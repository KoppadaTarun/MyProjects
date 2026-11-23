
from app.database.connection import SessionLocal
from app.database.models import Department

departments = [
    "HR",
    "Finance",
    "Marketing",
    "Engineering",
    "Operations"
]

db = SessionLocal()

try:
    for name in departments:
        existing = db.query(Department).filter(
            Department.name == name
        ).first()

        if not existing:
            db.add(Department(name=name))

    db.commit()
    print("Departments seeded successfully!")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()
