"""
Poster Manager - Download and cache movie posters
"""
import os
import requests
from PIL import Image, ImageTk
from io import BytesIO
from config import DATA_DIR

class PosterManager:
    """Manage movie poster downloads and caching"""
    
    def __init__(self):
        self.poster_cache_dir = os.path.join(DATA_DIR, 'posters')
        self._ensure_cache_dir()
        self.image_cache = {}  # In-memory cache
        self.placeholder = None
    
    def _ensure_cache_dir(self):
        """Create poster cache directory"""
        if not os.path.exists(self.poster_cache_dir):
            os.makedirs(self.poster_cache_dir)
    
    def get_poster(self, movie_id, poster_url, size=(100, 150)):
        """
        Get poster image for a movie
        
        Args:
            movie_id: Movie ID
            poster_url: URL to poster image
            size: Tuple (width, height) for resizing
            
        Returns:
            ImageTk.PhotoImage object or placeholder
        """
        # Check in-memory cache
        cache_key = f"{movie_id}_{size[0]}x{size[1]}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Check disk cache
        cache_file = os.path.join(self.poster_cache_dir, f"{movie_id}.jpg")
        
        if os.path.exists(cache_file):
            # Load from disk cache
            try:
                img = Image.open(cache_file)
                img = img.resize(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[cache_key] = photo
                return photo
            except Exception as e:
                print(f"Error loading cached poster: {e}")
        
        # Download poster
        if poster_url and poster_url.strip():
            try:
                response = requests.get(poster_url, timeout=5)
                if response.status_code == 200:
                    # Save to disk cache
                    with open(cache_file, 'wb') as f:
                        f.write(response.content)
                    
                    # Load and resize
                    img = Image.open(BytesIO(response.content))
                    img = img.resize(size, Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.image_cache[cache_key] = photo
                    return photo
            except Exception as e:
                print(f"Error downloading poster for movie {movie_id}: {e}")
        
        # Return placeholder
        return self.get_placeholder(size)
    
    def get_placeholder(self, size=(100, 150)):
        """Create a placeholder image"""
        if self.placeholder and self.placeholder.width() == size[0]:
            return self.placeholder
        
        # Create a simple colored rectangle as placeholder
        img = Image.new('RGB', size, color='#0f3460')
        
        # Add text
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Simple text without font
        text = "No\nPoster"
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        draw.text((x, y), text, fill='#b8b8b8')
        
        photo = ImageTk.PhotoImage(img)
        self.placeholder = photo
        return photo
    
    def clear_cache(self):
        """Clear poster cache"""
        self.image_cache.clear()
        # Optionally clear disk cache
        for file in os.listdir(self.poster_cache_dir):
            if file.endswith('.jpg'):
                os.remove(os.path.join(self.poster_cache_dir, file))
