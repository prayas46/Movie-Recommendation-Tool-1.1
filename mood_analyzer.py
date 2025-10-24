"""
Mood Analyzer - Rule-based text analysis (No NLP libraries needed!)
"""
from config import MOOD_KEYWORDS, EMOTION_GENRE_MAP, TIME_PREFERENCES, COMPLEXITY_MAP
from utils import get_time_of_day

class MoodAnalyzer:
    """Analyzes mood from text using keyword matching"""
    
    def __init__(self):
        self.mood_keywords = MOOD_KEYWORDS
    
    def analyze(self, text):
        """
        Analyze text and return mood profile
        
        Returns:
            dict: {
                'primary_emotion': str,
                'secondary_emotions': list,
                'energy_level': str,
                'preferred_genres': list,
                'complexity': str,
                'time_genres': list
            }
        """
        text_lower = text.lower()
        
        # Detect emotions using keyword matching
        emotion_scores = {}
        for emotion, keywords in self.mood_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Primary emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else 'bored'
        
        # Secondary emotions
        secondary_emotions = sorted(
            [(e, s) for e, s in emotion_scores.items() if e != primary_emotion],
            key=lambda x: x[1],
            reverse=True
        )[:2]
        secondary_emotions = [e[0] for e in secondary_emotions]
        
        # Energy level detection
        energy_level = self._detect_energy(text_lower)
        
        # Complexity detection
        complexity = self._detect_complexity(text_lower, energy_level)
        
        # Get genre preferences
        preferred_genres = EMOTION_GENRE_MAP.get(primary_emotion, ['Drama', 'Comedy'])
        
        # Add secondary emotion genres
        for emotion in secondary_emotions:
            preferred_genres.extend(EMOTION_GENRE_MAP.get(emotion, []))
        
        # Remove duplicates while preserving order
        preferred_genres = list(dict.fromkeys(preferred_genres))
        
        # Time-based genres
        time_of_day = get_time_of_day()
        time_genres = TIME_PREFERENCES.get(time_of_day, [])
        
        return {
            'primary_emotion': primary_emotion,
            'secondary_emotions': secondary_emotions,
            'energy_level': energy_level,
            'preferred_genres': preferred_genres,
            'complexity': complexity,
            'time_genres': time_genres,
            'raw_text': text
        }
    
    def _detect_energy(self, text):
        """Detect energy level from text"""
        high_energy = ['energetic', 'excited', 'pumped', 'active', 'hyper', 'motivated']
        low_energy = ['tired', 'exhausted', 'sleepy', 'drained', 'lazy', 'calm', 'relaxed']
        
        high_count = sum(1 for word in high_energy if word in text)
        low_count = sum(1 for word in low_energy if word in text)
        
        if high_count > low_count:
            return 'high'
        elif low_count > high_count:
            return 'low'
        else:
            return 'medium'
    
    def _detect_complexity(self, text, energy_level):
        """Detect preferred movie complexity"""
        if any(word in text for word in ['simple', 'easy', 'light', 'mindless', 'brain off']):
            return 'low'
        elif any(word in text for word in ['complex', 'deep', 'thought', 'intellectual', 'mind-bending']):
            return 'high'
        elif energy_level == 'low':
            return 'low'
        elif energy_level == 'high':
            return 'medium'
        else:
            return 'medium'
