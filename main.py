from website import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(debug=True)