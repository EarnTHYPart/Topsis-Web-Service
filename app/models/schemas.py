"""
Data models for TOPSIS Web Service
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import numpy as np


@dataclass
class TOPSISRequest:
    """Request model for TOPSIS evaluation"""
    decision_matrix: List[List[float]]
    weights: List[float]
    impacts: List[str]
    alternative_names: List[str] = field(default_factory=list)
    criterion_names: List[str] = field(default_factory=list)
    
    def to_numpy(self):
        """Convert to numpy arrays"""
        return np.array(self.decision_matrix)


@dataclass
class TOPSISResponse:
    """Response model for TOPSIS evaluation"""
    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: str = None
    
    def to_dict(self):
        """Convert to dictionary"""
        result = {
            'success': self.success,
            'message': self.message,
            'data': self.data
        }
        if self.error:
            result['error'] = self.error
        return result


@dataclass
class CriterionInfo:
    """Information about a single criterion"""
    name: str
    impact: str  # 'benefit' or 'cost'
    weight: float
    description: str = ""


@dataclass
class AlternativeResult:
    """Result for a single alternative"""
    name: str
    index: int
    score: float
    rank: int
