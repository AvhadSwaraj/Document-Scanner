from app import db, app
from models import User  # Ensure this matches your table name (users, not user)

with app.app_context():
    db.create_all()  # Create tables first
    
    # Insert a test user only if the table is empty
    if not User.query.first():
        test_user = User(username="testuser", password_hash="hashedpassword", credits=20)
        db.session.add(test_user)
        db.session.commit()
    
    print("Database initialized successfully!")
