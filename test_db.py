from website import create_app,db
from sqlalchemy.sql import text

app = create_app()
# Ensure application context is active
with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1"))
        print("Flask-SQLAlchemy connection successful!")
        print(result.fetchone())
    except Exception as e:
        print(f"Flask-SQLAlchemy connection failed: {e}")
