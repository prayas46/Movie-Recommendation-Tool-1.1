"""
TMDb API Fetcher - Fetch real movie data from The Movie Database
"""
import requests
import time
import os
from datetime import datetime, timedelta
from config import (
    TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL,
    TMDB_ENDPOINTS, TMDB_GENRE_MAP, TMDB_CONFIG, TMDB_GENRE_COMPLEXITY
)

class TMDbFetcher:
    """Fetch movie data from TMDb API"""
    
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base_url = TMDB_IMAGE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})
    
    def is_configured(self):
        """Check if API key is configured"""
        return bool(self.api_key and self.api_key != '')
    
    def fetch_popular_movies(self, pages=10):
        """
        Fetch popular movies from TMDb
        
        Args:
            pages: Number of pages to fetch (20 movies per page)
            
        Returns:
            List of movie dictionaries
        """
        if not self.is_configured():
            print("⚠️  TMDb API key not configured. Using fallback sample data.")
            return []
        
        all_movies = []
        
        print(f"🎬 Fetching {pages} pages of popular movies from TMDb...")
        
        for page in range(1, pages + 1):
            try:
                movies = self._fetch_page(page)
                if movies:
                    all_movies.extend(movies)
                    print(f"   ✅ Fetched page {page}/{pages} ({len(movies)} movies)")
                time.sleep(0.25)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Error fetching page {page}: {e}")
                continue
        
        print(f"✅ Total movies fetched: {len(all_movies)}")
        return all_movies
    
    def _fetch_page(self, page):
        """Fetch a single page of popular movies"""
        url = f"{self.base_url}{TMDB_ENDPOINTS['popular']}"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': 'en-US'
        }
        
        for attempt in range(TMDB_CONFIG['retry_attempts']):
            try:
                response = self.session.get(
                    url, 
                    params=params, 
                    timeout=TMDB_CONFIG['request_timeout']
                )
                response.raise_for_status()
                data = response.json()
                return data.get('results', [])
            except requests.exceptions.RequestException as e:
                if attempt < TMDB_CONFIG['retry_attempts'] - 1:
                    time.sleep(1)
                    continue
                else:
                    raise e
        
        return []
    
    def fetch_movie_details(self, movie_id):
        """
        Fetch detailed information for a specific movie
        
        Args:
            movie_id: TMDb movie ID
            
        Returns:
            Dictionary with movie details
        """
        if not self.is_configured():
            return None
        
        url = f"{self.base_url}{TMDB_ENDPOINTS['movie_details'].format(movie_id=movie_id)}"
        params = {
            'api_key': self.api_key,
            'language': 'en-US'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=TMDB_CONFIG['request_timeout'])
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for movie {movie_id}: {e}")
            return None
    
    def search_movies(self, query, page=1):
        """
        Search for movies by title
        
        Args:
            query: Search query
            page: Page number
            
        Returns:
            List of movie dictionaries
        """
        if not self.is_configured():
            return []
        
        url = f"{self.base_url}{TMDB_ENDPOINTS['search']}"
        params = {
            'api_key': self.api_key,
            'query': query,
            'page': page,
            'language': 'en-US'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=TMDB_CONFIG['request_timeout'])
            response.raise_for_status()
            data = response.json()
            return data.get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching for '{query}': {e}")
            return []
    
    def process_movie_data(self, movie_data, fetch_details=False):
        """
        Process raw TMDb movie data into our format
        
        Args:
            movie_data: Raw movie data from TMDb API
            fetch_details: Whether to fetch additional details (runtime)
            
        Returns:
            Dictionary in our movie format
        """
        # Get genre names
        genre_ids = movie_data.get('genre_ids', [])
        genres = [TMDB_GENRE_MAP.get(gid, 'Unknown') for gid in genre_ids if gid in TMDB_GENRE_MAP]
        genres_str = '|'.join(genres) if genres else 'Drama'
        
        # Determine complexity based on primary genre
        primary_genre = genres[0] if genres else 'Drama'
        complexity = TMDB_GENRE_COMPLEXITY.get(primary_genre, 'medium')
        
        # Get runtime if fetching details
        runtime = 120  # Default runtime
        if fetch_details:
            details = self.fetch_movie_details(movie_data['id'])
            if details and 'runtime' in details:
                runtime = details['runtime'] or 120
        else:
            # Estimate runtime based on genre
            runtime = self._estimate_runtime(primary_genre)
        
        # Extract year from release_date
        release_date = movie_data.get('release_date', '')
        year = int(release_date.split('-')[0]) if release_date else 2020
        
        # Convert vote_average (0-10) to our rating format
        rating = round(movie_data.get('vote_average', 7.0), 1)
        
        # Get poster path
        poster_path = movie_data.get('poster_path', '')
        poster_url = f"{self.image_base_url}{poster_path}" if poster_path else ''
        
        return {
            'id': movie_data['id'],
            'title': movie_data.get('title', 'Unknown'),
            'year': year,
            'genres': genres_str,
            'rating': rating,
            'runtime': runtime,
            'complexity': complexity,
            'overview': movie_data.get('overview', ''),
            'popularity': movie_data.get('popularity', 0),
            'vote_count': movie_data.get('vote_count', 0),
            'poster_url': poster_url,
            'original_language': movie_data.get('original_language', 'en')
        }
    
    def _estimate_runtime(self, genre):
        """Estimate runtime based on genre"""
        runtime_map = {
            'Animation': 95,
            'Comedy': 105,
            'Horror': 95,
            'Action': 120,
            'Adventure': 130,
            'Drama': 120,
            'Thriller': 110,
            'Sci-Fi': 125,
            'Fantasy': 135,
            'Romance': 110,
            'Crime': 115,
            'Mystery': 115,
            'War': 140,
            'History': 140,
            'Documentary': 100
        }
        return runtime_map.get(genre, 120)
    
    def fetch_and_process_movies(self, pages=10, fetch_details=False):
        """
        Fetch popular movies and process them into our format
        
        Args:
            pages: Number of pages to fetch
            fetch_details: Whether to fetch runtime details (slower)
            
        Returns:
            List of processed movie dictionaries
        """
        raw_movies = self.fetch_popular_movies(pages)
        
        if not raw_movies:
            return []
        
        processed_movies = []
        
        print(f"\n🔄 Processing {len(raw_movies)} movies...")
        for i, movie in enumerate(raw_movies, 1):
            try:
                processed = self.process_movie_data(movie, fetch_details=fetch_details)
                processed_movies.append(processed)
                if i % 20 == 0:
                    print(f"   ✅ Processed {i}/{len(raw_movies)} movies")
            except Exception as e:
                print(f"   ⚠️  Error processing movie: {e}")
                continue
        
        print(f"✅ Successfully processed {len(processed_movies)} movies\n")
        return processed_movies
    
    def get_cache_age(self, cache_file):
        """Get age of cache file in days"""
        if not os.path.exists(cache_file):
            return float('inf')
        
        modified_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        age = datetime.now() - modified_time
        return age.days
    
    def should_refresh_cache(self, cache_file):
        """Check if cache should be refreshed"""
        cache_age = self.get_cache_age(cache_file)
        return cache_age >= TMDB_CONFIG['cache_expiry_days']


def test_tmdb_connection():
    """Test TMDb API connection"""
    print("🧪 Testing TMDb API Connection...\n")
    
    fetcher = TMDbFetcher()
    
    if not fetcher.is_configured():
        print("❌ TMDb API key not configured!")
        print("   Please set TMDB_API_KEY environment variable or update config.py")
        return False
    
    print(f"✅ API key configured: {fetcher.api_key[:8]}...")
    
    try:
        print("\n📡 Fetching first page of popular movies...")
        movies = fetcher._fetch_page(1)
        
        if movies:
            print(f"✅ Successfully fetched {len(movies)} movies")
            print(f"\n🎬 Sample movie: {movies[0].get('title', 'Unknown')}")
            print(f"   Rating: {movies[0].get('vote_average', 0)}/10")
            print(f"   Genres: {movies[0].get('genre_ids', [])}")
            return True
        else:
            print("❌ No movies returned")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    # Test the API connection
    test_tmdb_connection()
