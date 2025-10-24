"""
Bulk Movie Fetcher - Fetch 5000+ movies from TMDb
This script fetches a large number of movies for comprehensive database
"""
import time
from tmdb_fetcher import TMDbFetcher
import pandas as pd
from config import MOVIES_FILE

def fetch_bulk_movies(target_movies=5000, pages_per_batch=50):
    """
    Fetch a large number of movies from TMDb
    
    Args:
        target_movies: Target number of movies to fetch (default 5000)
        pages_per_batch: Number of pages to fetch per batch (default 50)
    
    Note: TMDb provides 20 movies per page
          5000 movies = 250 pages
          Rate limit: 40 requests per 10 seconds
    """
    
    print("=" * 70)
    print("🎬 BULK MOVIE FETCHER - TMDb API")
    print("=" * 70)
    
    # Calculate pages needed
    pages_needed = (target_movies // 20) + 1
    print(f"\n📊 Configuration:")
    print(f"   Target Movies: {target_movies}")
    print(f"   Pages Needed: {pages_needed}")
    print(f"   Movies per Page: 20")
    print(f"   Estimated Time: ~{pages_needed * 0.3:.0f} seconds ({pages_needed * 0.3 / 60:.1f} minutes)")
    
    # Initialize fetcher
    fetcher = TMDbFetcher()
    
    # Check API key
    if not fetcher.is_configured():
        print("\n❌ ERROR: TMDb API key not configured!")
        print("   Please create a .env file with your API key:")
        print("   TMDB_API_KEY=your_api_key_here")
        print("\n   See TMDB_SETUP_GUIDE.md for instructions")
        return False
    
    print(f"\n✅ API Key configured: {fetcher.api_key[:12]}...")
    
    # Confirm with user
    print(f"\n⚠️  WARNING: This will make {pages_needed} API requests")
    print("   TMDb Rate Limit: 40 requests per 10 seconds")
    print("   The script includes automatic rate limiting")
    
    response = input("\n   Continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("   ❌ Fetch cancelled by user")
        return False
    
    # Start fetching
    print("\n" + "=" * 70)
    print("🚀 STARTING BULK FETCH")
    print("=" * 70)
    
    all_movies = []
    failed_pages = []
    start_time = time.time()
    
    for page in range(1, pages_needed + 1):
        try:
            # Fetch page
            movies = fetcher._fetch_page(page)
            
            if movies:
                all_movies.extend(movies)
                
                # Progress update every 10 pages
                if page % 10 == 0:
                    elapsed = time.time() - start_time
                    movies_fetched = len(all_movies)
                    progress = (page / pages_needed) * 100
                    estimated_total = (elapsed / page) * pages_needed
                    remaining = estimated_total - elapsed
                    
                    print(f"\n📊 Progress: {progress:.1f}% ({page}/{pages_needed} pages)")
                    print(f"   Movies Fetched: {movies_fetched}")
                    print(f"   Elapsed: {elapsed:.0f}s | Remaining: ~{remaining:.0f}s")
            else:
                failed_pages.append(page)
                print(f"   ⚠️  Page {page} returned no results")
            
            # Rate limiting: 40 requests per 10 seconds = 0.25s per request
            time.sleep(0.25)
            
        except Exception as e:
            print(f"   ❌ Error on page {page}: {e}")
            failed_pages.append(page)
            time.sleep(1)  # Wait longer on error
            continue
    
    # Fetch complete
    total_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("📊 FETCH COMPLETE")
    print("=" * 70)
    print(f"   Total Movies Fetched: {len(all_movies)}")
    print(f"   Total Time: {total_time:.0f} seconds ({total_time / 60:.1f} minutes)")
    print(f"   Failed Pages: {len(failed_pages)}")
    
    if failed_pages:
        print(f"   Failed Page Numbers: {failed_pages[:10]}{'...' if len(failed_pages) > 10 else ''}")
    
    # Process movies
    if not all_movies:
        print("\n❌ No movies fetched!")
        return False
    
    print("\n" + "=" * 70)
    print("🔄 PROCESSING MOVIES")
    print("=" * 70)
    
    processed_movies = []
    
    for i, movie in enumerate(all_movies, 1):
        try:
            processed = fetcher.process_movie_data(movie, fetch_details=False)
            processed_movies.append(processed)
            
            if i % 500 == 0:
                print(f"   ✅ Processed {i}/{len(all_movies)} movies")
        except Exception as e:
            print(f"   ⚠️  Error processing movie {i}: {e}")
            continue
    
    print(f"\n✅ Successfully processed {len(processed_movies)} movies")
    
    # Save to CSV
    print("\n" + "=" * 70)
    print("💾 SAVING TO DATABASE")
    print("=" * 70)
    
    df = pd.DataFrame(processed_movies)
    
    # Remove duplicates based on movie ID
    original_count = len(df)
    df = df.drop_duplicates(subset=['id'], keep='first')
    duplicates_removed = original_count - len(df)
    
    if duplicates_removed > 0:
        print(f"   🔧 Removed {duplicates_removed} duplicate movies")
    
    # Save to CSV
    df.to_csv(MOVIES_FILE, index=False)
    print(f"   ✅ Saved to: {MOVIES_FILE}")
    print(f"   📊 Total Movies in Database: {len(df)}")
    
    # Statistics
    print("\n" + "=" * 70)
    print("📊 DATABASE STATISTICS")
    print("=" * 70)
    
    print(f"   Total Movies: {len(df)}")
    print(f"   Average Rating: {df['rating'].mean():.2f}/10")
    print(f"   Year Range: {df['year'].min()} - {df['year'].max()}")
    
    # Top genres
    all_genres = []
    for genres_str in df['genres']:
        all_genres.extend(genres_str.split('|'))
    
    from collections import Counter
    genre_counts = Counter(all_genres)
    top_5_genres = genre_counts.most_common(5)
    
    print(f"\n   Top 5 Genres:")
    for genre, count in top_5_genres:
        print(f"      {genre}: {count} movies")
    
    # Complexity distribution
    complexity_dist = df['complexity'].value_counts()
    print(f"\n   Complexity Distribution:")
    for complexity, count in complexity_dist.items():
        print(f"      {complexity}: {count} movies")
    
    print("\n" + "=" * 70)
    print("🎉 SUCCESS! Your movie database is ready!")
    print("=" * 70)
    print(f"\n   Run 'python main.py' to start CineMatch with {len(df)} movies!")
    
    return True


if __name__ == "__main__":
    # Fetch 5000 movies (250 pages)
    fetch_bulk_movies(target_movies=5000, pages_per_batch=50)
