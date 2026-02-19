from app.db.base import SessionLocal, Base, engine
from app.db import models
from app.core import security

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def create_guest():
    email = "guest@example.com"
    password = "guestbits"
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        print(f"User {email} already exists.")
        # Update password just in case
        user.hashed_password = security.get_password_hash(password)
        db.commit()
        print("Password updated.")
    else:
        user = models.User(
            email=email,
            hashed_password=security.get_password_hash(password),
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        print(f"User {email} created.")

if __name__ == "__main__":
    create_guest()
