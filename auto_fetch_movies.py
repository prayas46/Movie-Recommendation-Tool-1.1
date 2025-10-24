"""
Automated Movie Fetcher - Uses demo API key
Fetches movies automatically without manual setup
"""
import os

# Create .env with demo key (you should replace this with your own)
demo_key = "c6b5bd3dd8092fa01092b3d9bc78b2ba"  # Replace with your actual key

print("🎬 Automated Movie Fetcher")
print("=" * 70)

# Create .env file
with open('.env', 'w') as f:
    f.write(f"TMDB_API_KEY={demo_key}\n")

print("✅ Created .env file with API key")
print("\n📡 Testing TMDb connection...")

# Test connection
import subprocess
result = subprocess.run(['python', 'tmdb_fetcher.py'], capture_output=True, text=True)

if "Successfully fetched" in result.stdout:
    print("✅ Connection successful!")
    
    print("\n" + "=" * 70)
    print("🚀 Starting bulk fetch for 5000 movies...")
    print("=" * 70)
    print("⏱️  Estimated time: ~25 minutes")
    print("📊 Progress will be shown every 10 pages\n")
    
    # Import and run bulk fetcher
    try:
        from fetch_bulk_movies import fetch_bulk_movies
        fetch_bulk_movies(target_movies=5000)
    except KeyboardInterrupt:
        print("\n\n⚠️  Fetch interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTip: Make sure you have a valid TMDb API key")
        print("Get one at: https://www.themoviedb.org/settings/api")
else:
    print("❌ Connection failed")
    print("Error output:", result.stdout)
    print("\n⚠️  The demo API key might be invalid or expired")
    print("\n📝 To fix this:")
    print("   1. Go to: https://www.themoviedb.org/settings/api")
    print("   2. Get your free API key (32 characters)")
    print("   3. Edit .env file and replace the key")
    print("   4. Run this script again")
