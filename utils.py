"""
Utility functions
"""
import numpy as np
from datetime import datetime

def format_runtime(minutes):
    """Convert minutes to hours and minutes"""
    hours = minutes // 60
    mins = minutes % 60
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def calculate_similarity_score(user_genres, movie_genres):
    """Calculate genre similarity using set overlap"""
    user_set = set(user_genres)
    movie_set = set(movie_genres)
    
    if not user_set or not movie_set:
        return 0.0
    
    intersection = len(user_set & movie_set)
    union = len(user_set | movie_set)
    
    # Jaccard similarity
    similarity = intersection / union if union > 0 else 0
    return similarity * 100

def get_time_of_day():
    """Get current time of day category"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 22:
        return 'evening'
    else:
        return 'night'

def normalize_scores(scores):
    """Normalize scores to 0-100 range using numpy"""
    scores_array = np.array(scores)
    if len(scores_array) == 0 or np.max(scores_array) == 0:
        return scores_array
    
    normalized = (scores_array - np.min(scores_array)) / (np.max(scores_array) - np.min(scores_array)) * 100
    return normalized

def get_match_emoji(score):
    """Get emoji based on match score"""
    if score >= 90:
        return "🎯"
    elif score >= 75:
        return "✨"
    elif score >= 60:
        return "👍"
    elif score >= 40:
        return "🤔"
    else:
        return "💭"
