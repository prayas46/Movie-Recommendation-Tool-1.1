"""
Configuration file for CineMatch
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MOVIES_FILE = os.path.join(DATA_DIR, 'movies.csv')
WATCH_HISTORY_FILE = os.path.join(DATA_DIR, 'watch_history.json')
USER_PROFILE_FILE = os.path.join(DATA_DIR, 'user_profile.json')

# UI Colors (Modern Dark Theme)
COLORS = {
    'bg_dark': '#1a1a2e',
    'bg_medium': '#16213e',
    'bg_light': '#0f3460',
    'accent': '#e94560',
    'accent_light': '#ff6b7a',
    'text_primary': '#ffffff',
    'text_secondary': '#b8b8b8',
    'success': '#00d9ff',
    'warning': '#ffd32d'
}

# Fonts
FONTS = {
    'title': ('Helvetica', 24, 'bold'),
    'heading': ('Helvetica', 16, 'bold'),
    'subheading': ('Helvetica', 12, 'bold'),
    'body': ('Helvetica', 10),
    'small': ('Helvetica', 8)
}

# Emotion to Genre Mapping (Rule-Based)
EMOTION_GENRE_MAP = {
    'happy': ['Comedy', 'Romance', 'Animation', 'Musical', 'Family'],
    'sad': ['Drama', 'Romance', 'Animation'],
    'angry': ['Action', 'Thriller', 'Crime', 'War'],
    'stressed': ['Comedy', 'Animation', 'Family', 'Documentary'],
    'anxious': ['Comedy', 'Animation', 'Romance', 'Feel-Good'],
    'bored': ['Action', 'Adventure', 'Sci-Fi', 'Fantasy', 'Mystery'],
    'excited': ['Action', 'Adventure', 'Thriller', 'Sci-Fi'],
    'lonely': ['Romance', 'Drama', 'Comedy'],
    'tired': ['Animation', 'Comedy', 'Light Drama'],
    'motivated': ['Biography', 'Documentary', 'Drama', 'Sport'],
    'romantic': ['Romance', 'Romantic Comedy', 'Drama'],
    'scared': ['Horror', 'Thriller', 'Mystery'],
    'curious': ['Documentary', 'Mystery', 'Sci-Fi', 'History'],
    'nostalgic': ['Classic', 'Animation', 'Drama', 'Period'],
    'adventurous': ['Adventure', 'Action', 'Fantasy', 'Sci-Fi']
}

# Mood Keywords (Rule-Based Detection)
MOOD_KEYWORDS = {
    'happy': ['happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'cheerful', 'delighted', 'glad'],
    'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable', 'heartbroken', 'gloomy', 'blue', 'crying'],
    'angry': ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated', 'rage', 'upset'],
    'stressed': ['stressed', 'overwhelmed', 'pressure', 'tense', 'anxious', 'worried', 'exam', 'deadline', 'busy'],
    'anxious': ['anxious', 'nervous', 'worried', 'uneasy', 'restless', 'concerned', 'panic'],
    'bored': ['bored', 'boring', 'dull', 'monotonous', 'tedious', 'nothing to do', 'uninterested'],
    'excited': ['excited', 'thrilled', 'pumped', 'energetic', 'enthusiastic', 'hyped'],
    'lonely': ['lonely', 'alone', 'isolated', 'solitary', 'breakup', 'broke up', 'missing'],
    'tired': ['tired', 'exhausted', 'fatigued', 'drained', 'weary', 'sleepy', 'worn out'],
    'motivated': ['motivated', 'inspired', 'driven', 'ambitious', 'determined', 'focused'],
    'romantic': ['romantic', 'love', 'relationship', 'date', 'valentine', 'crush'],
    'scared': ['scared', 'afraid', 'frightened', 'terrified', 'fear'],
    'curious': ['curious', 'wondering', 'interested', 'learn', 'discover', 'explore'],
    'nostalgic': ['nostalgic', 'memories', 'remember', 'childhood', 'old times', 'past'],
    'adventurous': ['adventure', 'adventurous', 'explore', 'travel', 'journey']
}

# Time-based preferences
TIME_PREFERENCES = {
    'morning': ['Documentary', 'Biography', 'Family', 'Light Comedy'],
    'afternoon': ['Action', 'Adventure', 'Comedy', 'Drama'],
    'evening': ['Drama', 'Thriller', 'Romance', 'Mystery'],
    'night': ['Horror', 'Thriller', 'Mystery', 'Sci-Fi', 'Psychological']
}

# Complexity levels
COMPLEXITY_MAP = {
    'low': ['Animation', 'Family', 'Comedy', 'Romance', 'Feel-Good'],
    'medium': ['Action', 'Adventure', 'Drama', 'Crime'],
    'high': ['Thriller', 'Mystery', 'Sci-Fi', 'Psychological', 'Art House']
}

# ==================== TMDb API CONFIGURATION ====================

# TMDb API Settings
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')  # Set your API key in environment or .env file
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# TMDb API Endpoints
TMDB_ENDPOINTS = {
    'popular': '/movie/popular',
    'movie_details': '/movie/{movie_id}',
    'search': '/search/movie'
}

# TMDb Genre ID to Name Mapping
TMDB_GENRE_MAP = {
    28: "Action",
    12: "Adventure", 
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Sci-Fi",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western"
}

# API Configuration
TMDB_CONFIG = {
    'pages_to_fetch': 10,  # Number of pages to fetch (20 movies per page)
    'total_movies': 200,   # Total movies to fetch
    'request_timeout': 10,  # Timeout in seconds
    'retry_attempts': 3,    # Number of retry attempts
    'cache_expiry_days': 7  # Days before refreshing cached data
}

# Complexity assignment for TMDb genres
TMDB_GENRE_COMPLEXITY = {
    'Animation': 'low',
    'Family': 'low',
    'Comedy': 'low',
    'Romance': 'low',
    'Action': 'medium',
    'Adventure': 'medium',
    'Drama': 'medium',
    'Crime': 'medium',
    'Thriller': 'high',
    'Mystery': 'high',
    'Sci-Fi': 'high',
    'Horror': 'high',
    'Documentary': 'medium',
    'Fantasy': 'medium',
    'History': 'medium',
    'Music': 'low',
    'TV Movie': 'medium',
    'War': 'high',
    'Western': 'medium'
}
