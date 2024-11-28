import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from app.database import engine  # Import after setting the path

def test_connection():
    try:
        with engine.connect() as conn:
            print("Database connection successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    test_connection()
