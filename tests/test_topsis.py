"""
Unit tests for TOPSIS algorithm
"""

import unittest
import numpy as np
from app.utils.topsis import TOPSIS, parse_weights, parse_impacts


class TestTOPSIS(unittest.TestCase):
    """Test cases for TOPSIS algorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.topsis = TOPSIS()
        
        # Simple test data
        self.decision_matrix = np.array([
            [8, 7, 6],
            [6, 8, 7],
            [7, 6, 8]
        ])
        self.weights = np.array([0.333, 0.333, 0.334])
        self.impacts = ['benefit', 'benefit', 'benefit']
    
    def test_normalize_matrix(self):
        """Test matrix normalization"""
        normalized = self.topsis.normalize_matrix(self.decision_matrix)
        
        # Check shape
        self.assertEqual(normalized.shape, self.decision_matrix.shape)
        
        # Check that columns are normalized (sum of squares = 1)
        for j in range(normalized.shape[1]):
            column_sum_squares = np.sum(normalized[:, j] ** 2)
            self.assertAlmostEqual(column_sum_squares, 1.0, places=10)
    
    def test_evaluate_basic(self):
        """Test basic TOPSIS evaluation"""
        scores, ranks = self.topsis.evaluate(
            self.decision_matrix, 
            self.weights, 
            self.impacts
        )
        
        # Check output shapes
        self.assertEqual(len(scores), 3)
        self.assertEqual(len(ranks), 3)
        
        # Check that scores are between 0 and 1
        self.assertTrue(np.all(scores >= 0))
        self.assertTrue(np.all(scores <= 1))
        
        # Check that ranks are 1, 2, 3
        self.assertEqual(set(ranks), {1, 2, 3})
    
    def test_weights_validation(self):
        """Test weights validation"""
        with self.assertRaises(ValueError):
            # Wrong number of weights
            self.topsis.evaluate(
                self.decision_matrix,
                np.array([0.5, 0.5]),  # Only 2 weights instead of 3
                self.impacts
            )
    
    def test_impacts_validation(self):
        """Test impacts validation"""
        with self.assertRaises(ValueError):
            # Invalid impact type
            self.topsis.evaluate(
                self.decision_matrix,
                self.weights,
                ['benefit', 'benefit', 'invalid']
            )
    
    def test_mixed_impacts(self):
        """Test with mixed benefit and cost impacts"""
        impacts = ['benefit', 'benefit', 'cost']
        scores, ranks = self.topsis.evaluate(
            self.decision_matrix,
            self.weights,
            impacts
        )
        
        self.assertEqual(len(scores), 3)
        self.assertEqual(len(ranks), 3)
    
    def test_parse_weights(self):
        """Test weight parsing"""
        weights_str = "0.3, 0.3, 0.4"
        weights = parse_weights(weights_str)
        
        self.assertEqual(len(weights), 3)
        self.assertAlmostEqual(np.sum(weights), 1.0)
    
    def test_parse_impacts(self):
        """Test impact parsing"""
        impacts_str = "benefit, cost, benefit"
        impacts = parse_impacts(impacts_str)
        
        self.assertEqual(len(impacts), 3)
        self.assertEqual(impacts[0], 'benefit')
        self.assertEqual(impacts[1], 'cost')
    
    def test_get_results_dataframe(self):
        """Test results dataframe generation"""
        scores = np.array([0.6, 0.7, 0.5])
        ranks = np.array([2, 1, 3])
        alt_names = ['A', 'B', 'C']
        
        df = self.topsis.get_results_dataframe(scores, ranks, alt_names)
        
        self.assertEqual(len(df), 3)
        self.assertIn('Alternative', df.columns)
        self.assertIn('TOPSIS_Score', df.columns)
        self.assertIn('Rank', df.columns)


class TestTOPSISEdgeCases(unittest.TestCase):
    """Test edge cases for TOPSIS"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.topsis = TOPSIS()
    
    def test_identical_alternatives(self):
        """Test with identical alternatives"""
        decision_matrix = np.array([
            [8, 7, 6],
            [8, 7, 6],
            [8, 7, 6]
        ])
        weights = np.array([0.333, 0.333, 0.334])
        impacts = ['benefit', 'benefit', 'benefit']
        
        scores, ranks = self.topsis.evaluate(decision_matrix, weights, impacts)
        
        # All should have same score
        self.assertAlmostEqual(scores[0], scores[1])
        self.assertAlmostEqual(scores[1], scores[2])
    
    def test_single_criterion(self):
        """Test with single criterion"""
        decision_matrix = np.array([[8], [6], [7]])
        weights = np.array([1.0])
        impacts = ['benefit']
        
        scores, ranks = self.topsis.evaluate(decision_matrix, weights, impacts)
        
        self.assertEqual(len(scores), 3)
        self.assertEqual(len(ranks), 3)


if __name__ == '__main__':
    unittest.main()
