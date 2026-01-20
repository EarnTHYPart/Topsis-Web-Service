"""
Example usage and test data for TOPSIS Web Service
"""

# Example 1: Simple 3 Alternatives, 3 Criteria
EXAMPLE_1 = {
    "decision_matrix": [
        [8, 7, 6],
        [6, 8, 7],
        [7, 6, 8]
    ],
    "weights": [0.3, 0.3, 0.4],
    "impacts": ["benefit", "benefit", "benefit"],
    "alternative_names": ["Project A", "Project B", "Project C"],
    "criterion_names": ["Cost Efficiency", "Quality", "Speed"]
}

# Example 2: 4 Alternatives, 4 Criteria (mixed benefit and cost)
EXAMPLE_2 = {
    "decision_matrix": [
        [10, 8, 7, 5],
        [8, 9, 6, 8],
        [9, 7, 8, 6],
        [7, 6, 9, 7]
    ],
    "weights": [0.25, 0.25, 0.25, 0.25],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["Vendor A", "Vendor B", "Vendor C", "Vendor D"],
    "criterion_names": ["Quality", "Reliability", "Price", "Support"]
}

# Example 3: Car Selection
EXAMPLE_3 = {
    "decision_matrix": [
        [8.5, 7.2, 45000, 8.0],
        [7.8, 8.5, 52000, 7.5],
        [9.2, 6.8, 38000, 8.8]
    ],
    "weights": [0.3, 0.2, 0.3, 0.2],
    "impacts": ["benefit", "benefit", "cost", "benefit"],
    "alternative_names": ["Toyota Camry", "Honda Accord", "Mazda 6"],
    "criterion_names": ["Performance", "Comfort", "Price", "Fuel Efficiency"]
}

# Example 4: Real Estate Selection
EXAMPLE_4 = {
    "decision_matrix": [
        [5, 8, 400000, 20, 9],
        [8, 6, 350000, 15, 7],
        [6, 7, 380000, 25, 8],
        [7, 9, 420000, 18, 6]
    ],
    "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
    "impacts": ["benefit", "benefit", "cost", "benefit", "benefit"],
    "alternative_names": ["Property A", "Property B", "Property C", "Property D"],
    "criterion_names": ["Location", "Amenities", "Price", "Space", "Safety"]
}

if __name__ == "__main__":
    import json
    
    print("Example 1 - Project Selection:")
    print(json.dumps(EXAMPLE_1, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("Example 2 - Vendor Selection:")
    print(json.dumps(EXAMPLE_2, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("Example 3 - Car Selection:")
    print(json.dumps(EXAMPLE_3, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("Example 4 - Real Estate Selection:")
    print(json.dumps(EXAMPLE_4, indent=2))
