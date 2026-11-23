
from app.database.connection import SessionLocal
from app.database.models import User

db = SessionLocal()

try:
    existing_user = db.query(User).filter(
        User.email == "admin@company.com"
    ).first()

    if existing_user:
        print("Test user already exists!")

    else:
        user = User(
            username="admin",
            email="admin@company.com",
            hashed_password="temporary-test-password",
            role="admin",
            is_active=True
        )

        db.add(user)
        db.commit()

        print("Test user created successfully!")

finally:
    db.close()
