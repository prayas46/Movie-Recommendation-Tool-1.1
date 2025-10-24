"""
Recommendation Engine - Smart rule-based recommendations
"""
import numpy as np
from utils import calculate_similarity_score, normalize_scores

class RecommendationEngine:
    """Generate recommendations using intelligent rule-based algorithms"""
    
    def __init__(self, data_manager, file_handler):
        self.data_manager = data_manager
        self.file_handler = file_handler
    
    def get_mood_recommendations(self, mood_profile, n=5):
        """
        Get recommendations based on mood profile
        
        Args:
            mood_profile: Dict with emotion, energy, complexity, etc.
            n: Number of recommendations
            
        Returns:
            List of (movie_dict, score, reason) tuples
        """
        # Start with all movies
        candidates = self.data_manager.movies_df.copy()
        
        # Filter by complexity
        if mood_profile['complexity'] in ['low', 'medium', 'high']:
            complexity_matches = candidates[candidates['complexity'] == mood_profile['complexity']]
            if len(complexity_matches) >= n:
                candidates = complexity_matches
        
        # Calculate scores for each movie
        scores = []
        reasons = []
        
        for _, movie in candidates.iterrows():
            score, reason = self._calculate_mood_score(movie, mood_profile)
            scores.append(score)
            reasons.append(reason)
        
        # Add scores to dataframe
        candidates = candidates.copy()
        candidates['score'] = scores
        candidates['reason'] = reasons
        
        # Sort by score
        candidates = candidates.sort_values('score', ascending=False)
        
        # Get top N
        top_movies = candidates.head(n)
        
        results = []
        for _, movie in top_movies.iterrows():
            movie_dict = movie.to_dict()
            results.append((movie_dict, movie['score'], movie['reason']))
        
        return results
    
    def _calculate_mood_score(self, movie, mood_profile):
        """Calculate match score for a movie based on mood"""
        score = 0.0
        reason_parts = []
        
        # Base score from rating (0-50 points)
        score += (movie['rating'] / 10) * 50
        
        # Genre match (0-30 points)
        movie_genres = movie['genres'].split('|')
        preferred_genres = mood_profile['preferred_genres']
        
        genre_match_count = sum(1 for g in movie_genres if g in preferred_genres)
        if genre_match_count > 0:
            genre_score = (genre_match_count / len(movie_genres)) * 30
            score += genre_score
            reason_parts.append(f"Perfect {movie_genres[0]} for {mood_profile['primary_emotion']} mood")
        
        # Time-based bonus (0-10 points)
        time_genres = mood_profile['time_genres']
        time_match = sum(1 for g in movie_genres if g in time_genres)
        if time_match > 0:
            score += time_match * 5
            reason_parts.append("Great for this time of day")
        
        # Complexity match (0-15 points)
        if movie['complexity'] == mood_profile['complexity']:
            score += 15
            if mood_profile['complexity'] == 'low':
                reason_parts.append("Easy to follow")
            elif mood_profile['complexity'] == 'high':
                reason_parts.append("Intellectually engaging")
        
        # Energy level considerations (0-10 points)
        if mood_profile['energy_level'] == 'low' and movie['complexity'] == 'low':
            score += 10
            reason_parts.append("Perfect for relaxing")
        elif mood_profile['energy_level'] == 'high' and 'Action' in movie['genres']:
            score += 10
            reason_parts.append("High-energy entertainment")
        
        # Default reason if none found
        if not reason_parts:
            reason_parts.append(f"Highly rated {movie_genres[0]}")
        
        reason = " • ".join(reason_parts[:2])
        
        return score, reason
    
    def get_genre_based_recommendations(self, favorite_genres, n=5):
        """Get recommendations based on favorite genres"""
        if not favorite_genres:
            # Return top-rated movies
            top_movies = self.data_manager.movies_df.nlargest(n, 'rating')
            return [(movie.to_dict(), movie['rating'] * 10, "Highly rated") 
                    for _, movie in top_movies.iterrows()]
        
        # Filter by genres
        candidates = self.data_manager.filter_by_genres(favorite_genres)
        
        if len(candidates) == 0:
            # Fallback to top-rated
            candidates = self.data_manager.movies_df
        
        # Calculate similarity scores
        scores = []
        for _, movie in candidates.iterrows():
            movie_genres = movie['genres'].split('|')
            similarity = calculate_similarity_score(favorite_genres, movie_genres)
            # Boost by rating
            final_score = (similarity * 0.7) + (movie['rating'] * 3)
            scores.append(final_score)
        
        candidates = candidates.copy()
        candidates['score'] = scores
        candidates = candidates.sort_values('score', ascending=False)
        
        top_movies = candidates.head(n)
        
        results = []
        for _, movie in top_movies.iterrows():
            movie_dict = movie.to_dict()
            reason = f"Matches your taste in {', '.join(favorite_genres[:2])}"
            results.append((movie_dict, movie['score'], reason))
        
        return results
    
    def get_similar_movies(self, movie_id, n=5):
        """Find similar movies based on genres"""
        target_movie = self.data_manager.get_movie_by_id(movie_id)
        if not target_movie:
            return []
        
        target_genres = target_movie['genres'].split('|')
        
        # Calculate similarity for all other movies
        similarities = []
        
        for _, movie in self.data_manager.movies_df.iterrows():
            if movie['id'] == movie_id:
                continue
            
            movie_genres = movie['genres'].split('|')
            similarity = calculate_similarity_score(target_genres, movie_genres)
            
            # Boost by rating
            final_score = (similarity * 0.8) + (movie['rating'] * 2)
            similarities.append((movie.to_dict(), final_score))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for movie, score in similarities[:n]:
            reason = "Similar style and genre"
            results.append((movie, score, reason))
        
        return results
