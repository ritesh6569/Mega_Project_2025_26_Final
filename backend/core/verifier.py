def verify_document(extracted_features):
    """
    Compares extracted features and classifies the document as original or tampered.
    In a fully trained pipeline, this would pass the features into a trained SVM or NN.
    For this implementation, we use a scoring heuristic based on the ML simulation.
    """
    # Using the simulated anomaly score from the feature extraction step
    # A score closer to 1.0 means highly confident it's genuine based on learned patterns.
    # A score lower than 0.85 might indicate tampering.
    
    score = extracted_features.get('simulated_anomaly_score', 0.90)
    
    # 0.85 is our strict threshold for "Verified"
    is_verified = bool(score >= 0.85)
    
    confidence_percentage = round(score * 100, 2)
    
    return {
        'verified': is_verified,
        'similarity_score': round(score, 3),
        'confidence_percentage': confidence_percentage
    }
