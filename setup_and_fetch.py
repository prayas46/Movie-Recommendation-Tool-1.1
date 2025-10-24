"""
Interactive Setup and Fetch Script
This will guide you through setting up TMDb API and fetching 5000+ movies
"""
import os

print("=" * 70)
print("🎬 CineMatch - Bulk Movie Fetcher Setup")
print("=" * 70)

print("\n📋 To fetch 5000+ movies from TMDb, you need an API key.")
print("\n🔑 How to get your FREE TMDb API Key (takes 5 minutes):")
print("\n   1. Go to: https://www.themoviedb.org/signup")
print("   2. Create a free account and verify email")
print("   3. Go to Settings > API")
print("   4. Click 'Request an API Key' > Choose 'Developer'")
print("   5. Fill the form:")
print("      - Name: CineMatch")
print("      - URL: http://localhost")
print("      - Summary: Educational movie recommendation project")
print("   6. Copy your 'API Key (v3 auth)' - 32 characters")
print("      Example: c6b5bd3dd8092fa01092b3d9bc78b2ba")

print("\n" + "=" * 70)

# Check if .env exists
if os.path.exists('.env'):
    print("\n✅ Found existing .env file")
    with open('.env', 'r') as f:
        content = f.read()
        if 'TMDB_API_KEY=' in content:
            print("   API key is configured")
else:
    print("\n⚠️  No .env file found")

print("\n" + "=" * 70)
print("📝 Enter your TMDb API Key (32 characters)")
print("   Or press Enter to skip and use sample data")
print("=" * 70)

api_key = input("\nAPI Key: ").strip()

if api_key and len(api_key) > 20:
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"TMDB_API_KEY={api_key}\n")
    
    print("\n✅ API key saved to .env file!")
    
    # Ask how many movies to fetch
    print("\n" + "=" * 70)
    print("📊 How many movies do you want to fetch?")
    print("=" * 70)
    print("   1. Quick Test (100 movies, ~30 seconds)")
    print("   2. Medium (1000 movies, ~5 minutes)")
    print("   3. Large (5000 movies, ~25 minutes)")
    print("   4. Maximum (10000 movies, ~50 minutes)")
    
    choice = input("\nChoice (1-4): ").strip()
    
    movie_counts = {
        '1': 100,
        '2': 1000,
        '3': 5000,
        '4': 10000
    }
    
    target = movie_counts.get(choice, 5000)
    
    print(f"\n🚀 Starting fetch for {target} movies...")
    print("   This will take approximately {:.1f} minutes".format(target * 0.3 / 60))
    
    # Run the bulk fetcher
    import subprocess
    print("\n" + "=" * 70)
    
    # Modify fetch_bulk_movies.py to accept target as argument
    with open('fetch_bulk_movies.py', 'r') as f:
        content = f.read()
    
    # Run it
    os.system(f'python fetch_bulk_movies.py {target}')
    
else:
    print("\n⚠️  No API key provided")
    print("   CineMatch will use 50 sample movies")
    print("\n   To fetch real movies later:")
    print("   1. Get API key from: https://www.themoviedb.org/settings/api")
    print("   2. Run: python setup_and_fetch.py")

print("\n" + "=" * 70)
print("✅ Setup Complete!")
print("=" * 70)
print("\nNext steps:")
print("   • Run: python main.py")
print("   • Or fetch more: python fetch_bulk_movies.py")
print("\n")
