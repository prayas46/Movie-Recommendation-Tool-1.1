"""
Data Manager - Handle movie data with Pandas
Supports both TMDb API and fallback sample data
"""
import pandas as pd
import numpy as np
import os
from config import MOVIES_FILE, DATA_DIR, TMDB_CONFIG

class DataManager:
    """Manage movie database using Pandas"""
    
    def __init__(self):
        self._ensure_data_dir()
        self.movies_df = self._load_or_create_movies()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
    
    def _load_or_create_movies(self):
        """
        Load movies from CSV or fetch from TMDb API
        Priority: Existing CSV > TMDb API > Sample Data
        """
        # Check if CSV exists and is recent
        if os.path.exists(MOVIES_FILE):
            try:
                df = pd.read_csv(MOVIES_FILE)
                
                # Check if we should refresh from TMDb
                if self._should_refresh_data():
                    print("🔄 Movie data is outdated. Attempting to refresh from TMDb...")
                    refreshed_df = self._fetch_from_tmdb()
                    if refreshed_df is not None and not refreshed_df.empty:
                        return refreshed_df
                
                print(f"✅ Loaded {len(df)} movies from cache")
                return df
            except Exception as e:
                print(f"⚠️  Error loading cached data: {e}")
        
        # Try fetching from TMDb
        print("📡 No cached data found. Attempting to fetch from TMDb API...")
        tmdb_df = self._fetch_from_tmdb()
        if tmdb_df is not None and not tmdb_df.empty:
            return tmdb_df
        
        # Fallback to sample data
        print("📚 Using fallback sample data (50 curated movies)")
        return self._create_sample_movies()
    
    def _should_refresh_data(self):
        """Check if movie data should be refreshed from TMDb"""
        try:
            from tmdb_fetcher import TMDbFetcher
            fetcher = TMDbFetcher()
            return fetcher.should_refresh_cache(MOVIES_FILE)
        except:
            return False
    
    def _fetch_from_tmdb(self):
        """Fetch movies from TMDb API"""
        try:
            from tmdb_fetcher import TMDbFetcher
            
            fetcher = TMDbFetcher()
            
            if not fetcher.is_configured():
                print("⚠️  TMDb API key not configured. Skipping API fetch.")
                return None
            
            # Fetch and process movies
            movies = fetcher.fetch_and_process_movies(
                pages=TMDB_CONFIG['pages_to_fetch'],
                fetch_details=False  # Set to True for accurate runtime (slower)
            )
            
            if not movies:
                print("⚠️  No movies fetched from TMDb")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(movies)
            
            # Save to CSV for caching
            df.to_csv(MOVIES_FILE, index=False)
            print(f"✅ Saved {len(df)} movies to {MOVIES_FILE}")
            
            return df
            
        except ImportError:
            print("⚠️  TMDb fetcher not available")
            return None
        except Exception as e:
            print(f"❌ Error fetching from TMDb: {e}")
            return None
    
    def _create_sample_movies(self):
        """Create sample movie database"""
        movies_data = {
            'id': range(1, 51),
            'title': [
                'The Shawshank Redemption', 'The Dark Knight', 'Forrest Gump', 'Inception',
                'Toy Story', 'The Notebook', 'The Conjuring', 'Superbad', 'Interstellar',
                'Pulp Fiction', 'The Matrix', 'Good Will Hunting', 'The Lion King',
                'Titanic', 'The Avengers', 'Jurassic Park', 'The Silence of the Lambs',
                'Saving Private Ryan', 'The Green Mile', 'Se7en', 'The Prestige',
                'The Departed', 'Gladiator', 'The Godfather', 'Schindler\'s List',
                'Fight Club', 'The Social Network', 'Whiplash', 'La La Land', 'Moonlight',
                'Parasite', 'Joker', 'Get Out', 'Dunkirk', 'Baby Driver',
                'Mad Max: Fury Road', 'The Grand Budapest Hotel', 'Her', 'Frozen',
                'Inside Out', 'Coco', 'Spider-Man: Into the Spider-Verse', 'Knives Out',
                'Jojo Rabbit', 'Little Women', '1917', 'The Lighthouse', 'Midsommar',
                'Hereditary', 'A Quiet Place'
            ],
            'year': [
                1994, 2008, 1994, 2010, 1995, 2004, 2013, 2007, 2014, 1994,
                1999, 1997, 1994, 1997, 2012, 1993, 1991, 1998, 1999, 1995,
                2006, 2006, 2000, 1972, 1993, 1999, 2010, 2014, 2016, 2016,
                2019, 2019, 2017, 2017, 2017, 2015, 2014, 2013, 2013, 2015,
                2017, 2018, 2019, 2019, 2019, 2019, 2019, 2019, 2018, 2018
            ],
            'genres': [
                'Drama', 'Action|Crime|Drama', 'Drama|Romance', 'Action|Sci-Fi|Thriller',
                'Animation|Family|Comedy', 'Romance|Drama', 'Horror|Mystery|Thriller', 'Comedy',
                'Sci-Fi|Drama|Adventure', 'Crime|Drama', 'Action|Sci-Fi', 'Drama|Romance',
                'Animation|Family|Drama', 'Romance|Drama', 'Action|Adventure|Sci-Fi',
                'Adventure|Sci-Fi|Thriller', 'Crime|Drama|Thriller', 'Drama|War',
                'Crime|Drama|Fantasy', 'Crime|Drama|Mystery', 'Drama|Mystery|Sci-Fi',
                'Crime|Drama|Thriller', 'Action|Adventure|Drama', 'Crime|Drama',
                'Biography|Drama|History', 'Drama', 'Biography|Drama', 'Drama|Music',
                'Comedy|Drama|Music|Romance', 'Drama', 'Comedy|Drama|Thriller', 'Crime|Drama',
                'Horror|Mystery|Thriller', 'Drama|Thriller|War', 'Action|Crime|Music',
                'Action|Adventure|Sci-Fi', 'Adventure|Comedy|Crime', 'Drama|Romance|Sci-Fi',
                'Animation|Family|Musical', 'Animation|Family|Comedy', 'Animation|Family|Fantasy',
                'Animation|Action|Adventure', 'Comedy|Crime|Drama', 'Comedy|Drama|War',
                'Drama|Romance', 'Drama|Thriller|War', 'Drama|Fantasy|Horror', 'Drama|Horror|Mystery',
                'Horror|Mystery|Thriller', 'Drama|Horror|Thriller'
            ],
            'rating': [
                9.3, 9.0, 8.8, 8.8, 8.3, 7.8, 7.5, 7.6, 8.6, 8.9,
                8.7, 8.3, 8.5, 7.9, 8.0, 8.2, 8.6, 8.6, 8.6, 8.6,
                8.5, 8.5, 8.5, 9.2, 9.0, 8.8, 7.8, 8.5, 8.0, 7.4,
                8.5, 8.4, 7.7, 7.8, 7.6, 8.1, 8.1, 8.0, 7.4, 8.2,
                8.5, 8.4, 7.9, 7.9, 8.0, 8.5, 7.5, 7.7, 7.3, 7.5
            ],
            'runtime': [
                142, 152, 142, 148, 81, 123, 112, 113, 169, 154,
                136, 126, 88, 194, 143, 127, 118, 169, 189, 127,
                130, 151, 155, 175, 195, 139, 120, 106, 128, 111,
                132, 122, 104, 106, 113, 120, 99, 126, 102, 95,
                105, 117, 130, 108, 135, 119, 119, 109, 147, 90
            ],
            'complexity': [
                'medium', 'high', 'low', 'high', 'low', 'low', 'medium', 'low', 'high', 'high',
                'high', 'medium', 'low', 'low', 'medium', 'medium', 'high', 'high', 'medium', 'high',
                'high', 'high', 'medium', 'high', 'high', 'high', 'medium', 'high', 'low', 'medium',
                'high', 'high', 'high', 'high', 'medium', 'medium', 'medium', 'medium', 'low', 'low',
                'low', 'medium', 'medium', 'medium', 'medium', 'high', 'high', 'high', 'high', 'medium'
            ]
        }
        
        df = pd.DataFrame(movies_data)
        df.to_csv(MOVIES_FILE, index=False)
        return df
    
    def get_all_genres(self):
        """Get list of all unique genres"""
        all_genres = set()
        for genres_str in self.movies_df['genres']:
            genres = genres_str.split('|')
            all_genres.update(genres)
        return sorted(list(all_genres))
    
    def filter_by_genres(self, preferred_genres):
        """Filter movies by genres"""
        if not preferred_genres:
            return self.movies_df
        
        mask = self.movies_df['genres'].apply(
            lambda x: any(genre in x for genre in preferred_genres)
        )
        return self.movies_df[mask]
    
    def filter_by_complexity(self, complexity):
        """Filter by complexity level"""
        return self.movies_df[self.movies_df['complexity'] == complexity]
    
    def filter_by_runtime(self, max_runtime):
        """Filter by maximum runtime"""
        return self.movies_df[self.movies_df['runtime'] <= max_runtime]
    
    def search_by_title(self, query):
        """Search movies by title"""
        mask = self.movies_df['title'].str.contains(query, case=False, na=False)
        return self.movies_df[mask]
    
    def get_movie_by_id(self, movie_id):
        """Get movie details by ID"""
        result = self.movies_df[self.movies_df['id'] == movie_id]
        if not result.empty:
            return result.iloc[0].to_dict()
        return None
