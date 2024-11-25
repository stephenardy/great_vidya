## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Create a `.env` file in the root directory by copying `.env.example`:
   ```
   cp .env.example .env
   ```
3. Fill in the necessary values in `.env`:
   ```
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///your_database.db
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the app:
    ```
    flask run
    ```
