from app import app, db, User, Customer

def init_db():
    with app.app_context():
        # This will create the database and all tables based on your models
        db.create_all()
        print("Database initialized and tables created successfully!")

if __name__ == "__main__":
    init_db()