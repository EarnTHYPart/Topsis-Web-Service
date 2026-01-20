"""
API routes for TOPSIS Web Service
"""

from flask import Blueprint, request, jsonify
import numpy as np
from ..utils.topsis import TOPSIS, parse_weights, parse_impacts
from ..models.schemas import TOPSISRequest, TOPSISResponse

# Create blueprint
topsis_bp = Blueprint('topsis', __name__, url_prefix='/api/topsis')


@topsis_bp.route('/evaluate', methods=['POST'])
def evaluate():
    """
    Evaluate alternatives using TOPSIS method.
    
    Expected JSON payload:
    {
        "decision_matrix": [[row1], [row2], ...],
        "weights": [w1, w2, ...],
        "impacts": ["benefit", "cost", ...],
        "alternative_names": ["Alt1", "Alt2", ...],
        "criterion_names": ["C1", "C2", ...]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided',
                'error': 'Request body is empty'
            }), 400
        
        required_fields = ['decision_matrix', 'weights', 'impacts']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'error': f'Missing fields: {", ".join(missing_fields)}'
            }), 400
        
        # Parse input data
        decision_matrix = np.array(data['decision_matrix'])
        weights = np.array(data['weights'])
        impacts = data['impacts']
        alternative_names = data.get('alternative_names', [])
        criterion_names = data.get('criterion_names', [])
        
        # Validate matrix dimensions
        if decision_matrix.ndim != 2:
            return jsonify({
                'success': False,
                'message': 'Decision matrix must be 2-dimensional',
                'error': 'Invalid matrix dimensions'
            }), 400
        
        n_alternatives, n_criteria = decision_matrix.shape
        
        # Validate weights
        if len(weights) != n_criteria:
            return jsonify({
                'success': False,
                'message': f'Expected {n_criteria} weights, got {len(weights)}',
                'error': 'Weight count mismatch'
            }), 400
        
        # Validate impacts
        if len(impacts) != n_criteria:
            return jsonify({
                'success': False,
                'message': f'Expected {n_criteria} impacts, got {len(impacts)}',
                'error': 'Impact count mismatch'
            }), 400
        
        # Validate impact values
        valid_impacts = {'benefit', 'cost'}
        for impact in impacts:
            if impact.lower() not in valid_impacts:
                return jsonify({
                    'success': False,
                    'message': f'Invalid impact: {impact}. Must be "benefit" or "cost"',
                    'error': 'Invalid impact value'
                }), 400
        
        # Set default names if not provided
        if not alternative_names:
            alternative_names = [f'Alternative_{i+1}' for i in range(n_alternatives)]
        
        if not criterion_names:
            criterion_names = [f'Criterion_{i+1}' for i in range(n_criteria)]
        
        # Normalize weights
        weights = weights / np.sum(weights)
        
        # Perform TOPSIS evaluation
        topsis = TOPSIS()
        scores, ranks = topsis.evaluate(decision_matrix, weights, impacts)
        
        # Prepare results
        results = []
        for i, (score, rank) in enumerate(zip(scores, ranks)):
            results.append({
                'alternative': alternative_names[i],
                'index': i,
                'score': float(score),
                'rank': int(rank)
            })
        
        # Sort by rank
        results.sort(key=lambda x: x['rank'])
        
        response = {
            'success': True,
            'message': 'TOPSIS evaluation completed successfully',
            'data': {
                'results': results,
                'summary': {
                    'n_alternatives': n_alternatives,
                    'n_criteria': n_criteria,
                    'best_alternative': results[0]['alternative'],
                    'best_score': results[0]['score']
                }
            }
        }
        
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'error': 'Validation error'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred during evaluation',
            'error': str(e)
        }), 500


@topsis_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'TOPSIS API is running',
        'status': 'healthy'
    }), 200


@topsis_bp.route('/info', methods=['GET'])
def info():
    """Get information about TOPSIS method"""
    return jsonify({
        'success': True,
        'message': 'Information about TOPSIS method',
        'data': {
            'name': 'TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)',
            'description': 'A multi-criteria decision-making method that ranks alternatives based on their similarity to an ideal solution',
            'methodology': [
                '1. Normalize the decision matrix',
                '2. Calculate weighted normalized matrix',
                '3. Determine ideal best and worst solutions',
                '4. Calculate separation distances',
                '5. Calculate TOPSIS scores',
                '6. Rank alternatives'
            ],
            'impact_types': ['benefit', 'cost'],
            'api_endpoints': [
                {
                    'method': 'POST',
                    'endpoint': '/api/topsis/evaluate',
                    'description': 'Perform TOPSIS evaluation'
                },
                {
                    'method': 'GET',
                    'endpoint': '/api/topsis/health',
                    'description': 'Check API health'
                },
                {
                    'method': 'GET',
                    'endpoint': '/api/topsis/info',
                    'description': 'Get TOPSIS information'
                }
            ]
        }
    }), 200
