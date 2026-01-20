"""
TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) Implementation
This module provides the core TOPSIS algorithm for Multi-Criteria Decision Making
"""

import numpy as np
import pandas as pd
from typing import Union, List, Tuple


class TOPSIS:
    """
    TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
    A decision-making method that ranks alternatives based on their similarity to an ideal solution.
    """
    
    def __init__(self):
        self.decision_matrix = None
        self.weights = None
        self.impacts = None
        self.normalized_matrix = None
        self.weighted_matrix = None
        
    def normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """
        Normalize the decision matrix using vector normalization.
        
        Args:
            matrix: Decision matrix (n x m)
            
        Returns:
            Normalized matrix
        """
        # Calculate the sum of squares for each column
        sum_squares = np.sqrt(np.sum(matrix ** 2, axis=0))
        
        # Avoid division by zero
        sum_squares[sum_squares == 0] = 1
        
        # Normalize each column
        normalized = matrix / sum_squares
        
        return normalized
    
    def calculate_weighted_matrix(self, normalized_matrix: np.ndarray, 
                                 weights: np.ndarray) -> np.ndarray:
        """
        Calculate the weighted normalized decision matrix.
        
        Args:
            normalized_matrix: Normalized decision matrix
            weights: Weights for each criterion
            
        Returns:
            Weighted normalized matrix
        """
        weighted = normalized_matrix * weights
        return weighted
    
    def calculate_ideal_solutions(self, weighted_matrix: np.ndarray, 
                                 impacts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate ideal best and ideal worst solutions.
        
        Args:
            weighted_matrix: Weighted normalized matrix
            impacts: List of 'benefit' or 'cost' for each criterion
            
        Returns:
            Tuple of (ideal_best, ideal_worst)
        """
        ideal_best = []
        ideal_worst = []
        
        for i, impact in enumerate(impacts):
            if impact.lower() == 'benefit':
                ideal_best.append(np.max(weighted_matrix[:, i]))
                ideal_worst.append(np.min(weighted_matrix[:, i]))
            else:  # cost
                ideal_best.append(np.min(weighted_matrix[:, i]))
                ideal_worst.append(np.max(weighted_matrix[:, i]))
        
        return np.array(ideal_best), np.array(ideal_worst)
    
    def calculate_separation(self, weighted_matrix: np.ndarray,
                           ideal_point: np.ndarray) -> np.ndarray:
        """
        Calculate separation distance from ideal point.
        
        Args:
            weighted_matrix: Weighted normalized matrix
            ideal_point: Ideal point (best or worst)
            
        Returns:
            Separation distances
        """
        separation = np.sqrt(np.sum((weighted_matrix - ideal_point) ** 2, axis=1))
        return separation
    
    def calculate_topsis_scores(self, distance_best: np.ndarray,
                               distance_worst: np.ndarray) -> np.ndarray:
        """
        Calculate TOPSIS scores based on distances to ideal solutions.
        
        Args:
            distance_best: Distance to ideal best solution
            distance_worst: Distance to ideal worst solution
            
        Returns:
            TOPSIS scores
        """
        # Avoid division by zero
        denominator = distance_best + distance_worst
        denominator[denominator == 0] = 1
        
        scores = distance_worst / denominator
        return scores
    
    def evaluate(self, decision_matrix: np.ndarray, 
                weights: np.ndarray, 
                impacts: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform TOPSIS evaluation on a decision matrix.
        
        Args:
            decision_matrix: Decision matrix (alternatives x criteria)
            weights: Weights for each criterion (should sum to 1)
            impacts: Impact type for each criterion ('benefit' or 'cost')
            
        Returns:
            Tuple of (scores, ranks)
            
        Raises:
            ValueError: If inputs are invalid
        """
        self.decision_matrix = decision_matrix
        self.weights = weights
        self.impacts = impacts
        
        # Validate inputs
        if decision_matrix.shape[1] != len(weights):
            raise ValueError("Number of weights must match number of criteria")
        
        if decision_matrix.shape[1] != len(impacts):
            raise ValueError("Number of impacts must match number of criteria")
        
        if not np.isclose(np.sum(weights), 1.0):
            raise ValueError("Sum of weights must equal 1.0")
        
        if len(impacts) != len(set([i.lower() for i in impacts])):
            pass  # Allow duplicate impacts
        
        for impact in impacts:
            if impact.lower() not in ['benefit', 'cost']:
                raise ValueError("Impact must be 'benefit' or 'cost'")
        
        # Step 1: Normalize the matrix
        self.normalized_matrix = self.normalize_matrix(decision_matrix)
        
        # Step 2: Calculate weighted normalized matrix
        self.weighted_matrix = self.calculate_weighted_matrix(
            self.normalized_matrix, weights
        )
        
        # Step 3: Determine ideal best and worst solutions
        ideal_best, ideal_worst = self.calculate_ideal_solutions(
            self.weighted_matrix, impacts
        )
        
        # Step 4: Calculate separation distances
        distance_best = self.calculate_separation(self.weighted_matrix, ideal_best)
        distance_worst = self.calculate_separation(self.weighted_matrix, ideal_worst)
        
        # Step 5: Calculate TOPSIS scores
        scores = self.calculate_topsis_scores(distance_best, distance_worst)
        
        # Step 6: Rank alternatives (higher score = better rank)
        ranks = np.argsort(-scores) + 1  # +1 because ranks start from 1
        
        return scores, ranks
    
    def get_results_dataframe(self, scores: np.ndarray, 
                             ranks: np.ndarray,
                             alternative_names: List[str] = None) -> pd.DataFrame:
        """
        Get results as a pandas DataFrame.
        
        Args:
            scores: TOPSIS scores
            ranks: Ranks of alternatives
            alternative_names: Names of alternatives (optional)
            
        Returns:
            DataFrame with results
        """
        if alternative_names is None:
            alternative_names = [f"Alternative_{i+1}" for i in range(len(scores))]
        
        results_df = pd.DataFrame({
            'Alternative': alternative_names,
            'TOPSIS_Score': scores,
            'Rank': ranks
        })
        
        results_df = results_df.sort_values('Rank').reset_index(drop=True)
        
        return results_df


def parse_impacts(impacts_str: str) -> List[str]:
    """
    Parse impacts string into list.
    
    Args:
        impacts_str: Comma-separated string of impacts
        
    Returns:
        List of impacts
    """
    return [impact.strip().lower() for impact in impacts_str.split(',')]


def parse_weights(weights_str: str) -> np.ndarray:
    """
    Parse weights string into numpy array.
    
    Args:
        weights_str: Comma-separated string of weights
        
    Returns:
        Numpy array of weights
    """
    weights = np.array([float(w.strip()) for w in weights_str.split(',')])
    
    # Normalize weights to sum to 1
    weights = weights / np.sum(weights)
    
    return weights
