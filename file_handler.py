"""
File Handler - Manage watch history and user profile
"""
import json
import os
from datetime import datetime
from config import WATCH_HISTORY_FILE, USER_PROFILE_FILE

class FileHandler:
    """Handle file operations for user data"""
    
    def __init__(self):
        self.watch_history = self._load_watch_history()
        self.user_profile = self._load_user_profile()
    
    def _load_watch_history(self):
        """Load watch history from JSON file"""
        if os.path.exists(WATCH_HISTORY_FILE):
            with open(WATCH_HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_watch_history(self):
        """Save watch history to JSON file"""
        with open(WATCH_HISTORY_FILE, 'w') as f:
            json.dump(self.watch_history, f, indent=2)
    
    def add_to_watch_history(self, movie_id, movie_title, genres, mood=None):
        """Add movie to watch history"""
        entry = {
            'movie_id': movie_id,
            'title': movie_title,
            'genres': genres,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        }
        self.watch_history.append(entry)
        self._save_watch_history()
    
    def get_watch_history(self):
        """Get all watch history"""
        return self.watch_history
    
    def get_genre_frequency(self):
        """Calculate frequency of watched genres"""
        genre_counts = {}
        for entry in self.watch_history:
            genres = entry['genres'].split('|')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        return genre_counts
    
    def get_watch_dates(self):
        """Get dates of watched movies"""
        dates = []
        for entry in self.watch_history:
            try:
                date = datetime.fromisoformat(entry['timestamp']).date()
                dates.append(date)
            except:
                pass
        return dates
    
    def _load_user_profile(self):
        """Load user profile"""
        if os.path.exists(USER_PROFILE_FILE):
            with open(USER_PROFILE_FILE, 'r') as f:
                return json.load(f)
        return {
            'favorite_genres': [],
            'disliked_genres': [],
            'preferred_complexity': 'medium',
            'preferred_runtime': 'any'
        }
    
    def save_user_profile(self):
        """Save user profile"""
        with open(USER_PROFILE_FILE, 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def update_favorite_genres(self, genres):
        """Update favorite genres"""
        self.user_profile['favorite_genres'] = genres
        self.save_user_profile()
    
    def clear_watch_history(self):
        """Clear all watch history"""
        self.watch_history = []
        self._save_watch_history()
