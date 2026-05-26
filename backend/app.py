from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import api

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for frontend communication
    CORS(app)
    
    # Initialize SQLite database
    init_db()
    
    # Register blueprints
    app.register_blueprint(api)
    
    @app.route('/')
    def home():
        return {'message': 'Portfolio API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
    
