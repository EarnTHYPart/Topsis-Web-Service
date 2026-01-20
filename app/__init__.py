"""
Flask application factory and configuration
"""

from flask import Flask, jsonify
from flask_cors import CORS
from .routes.topsis_routes import topsis_bp


def create_app(config=None):
    """
    Create and configure Flask application.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Configure app
    if config:
        app.config.update(config)
    else:
        app.config['JSON_SORT_KEYS'] = False
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(topsis_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint not found',
            'error': str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(error)
        }), 500
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'TOPSIS MCDM Web Service',
            'version': '1.0.0',
            'endpoints': {
                'topsis_api': '/api/topsis',
                'health': '/api/topsis/health',
                'info': '/api/topsis/info',
                'evaluate': '/api/topsis/evaluate'
            }
        }), 200
    
    @app.route('/api')
    def api_root():
        return jsonify({
            'success': True,
            'message': 'TOPSIS MCDM API',
            'available_endpoints': [
                'GET  /',
                'GET  /api',
                'GET  /api/topsis/health',
                'GET  /api/topsis/info',
                'POST /api/topsis/evaluate'
            ]
        }), 200
    
    return app
