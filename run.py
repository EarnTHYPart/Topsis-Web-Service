"""
Main entry point for TOPSIS Web Service
"""

import os
from app import create_app
from config.config import get_config


if __name__ == '__main__':
    # Get configuration from environment
    env = os.getenv('FLASK_ENV', 'development')
    config = get_config(env)
    
    # Create Flask app
    app = create_app(config.__dict__)
    
    # Run the app
    if env == 'production':
        # Use gunicorn in production
        # gunicorn -w 4 -b 0.0.0.0:5000 run:app
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        # Development server
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
