from app import db, app

# Create all tables based on the SQLAlchemy models
with app.app_context():
    db.create_all()
    print("Database initialized successfully with all tables including gender column!")