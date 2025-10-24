# 🎬 TMDb API Setup Guide

## Overview

CineMatch now supports **real movie data** from The Movie Database (TMDb)! This guide will help you set up the TMDb API integration.

---

## ⚡ Quick Start

### Option 1: Use Sample Data (No Setup Required)
CineMatch works out of the box with **50 curated sample movies**. No API key needed!

### Option 2: Use TMDb API (200+ Real Movies)
Follow the steps below to fetch **200+ real movies** with ratings, posters, and metadata.

---

## 🔑 Getting Your TMDb API Key

### Step 1: Create TMDb Account
1. Visit [https://www.themoviedb.org/signup](https://www.themoviedb.org/signup)
2. Sign up for a **free account**
3. Verify your email

### Step 2: Request API Key
1. Log in to your TMDb account
2. Navigate to **Settings** (click your avatar → Settings)
3. Click on **API** in the left sidebar
4. Click **"Request an API Key"**
5. Choose **"Developer"** option
6. Fill in the application form:
   - **Type of Use**: Educational / Personal Project
   - **Application Name**: CineMatch Movie Recommender
   - **Application URL**: http://localhost (or your website)
   - **Application Summary**: A Python-based movie recommendation system for learning purposes

### Step 3: Copy Your API Key
1. Once approved (instant for educational use), copy your **API Key (v3 auth)**
2. Keep it secure - don't share it publicly!

---

## 🛠️ Configuring CineMatch

### Method 1: Using .env File (Recommended)

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```
   
   Or on Windows:
   ```bash
   copy .env.example .env
   ```

2. **Edit .env file**:
   Open `.env` in a text editor and replace `your_api_key_here`:
   ```
   TMDB_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

3. **Save the file**

### Method 2: Environment Variable

Set the environment variable in your terminal:

**Windows (PowerShell):**
```powershell
$env:TMDB_API_KEY="your_api_key_here"
```

**Windows (CMD):**
```cmd
set TMDB_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export TMDB_API_KEY=your_api_key_here
```

### Method 3: Edit config.py Directly (Not Recommended)

Open `config.py` and find line 91:
```python
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
```

Replace with:
```python
TMDB_API_KEY = 'your_api_key_here'
```

⚠️ **Warning**: Don't commit this change to Git if your repo is public!

---

## 🧪 Testing Your Setup

### Test TMDb Connection
```bash
python tmdb_fetcher.py
```

**Expected Output:**
```
🧪 Testing TMDb API Connection...

✅ API key configured: a1b2c3d4...

📡 Fetching first page of popular movies...
✅ Successfully fetched 20 movies

🎬 Sample movie: The Shawshank Redemption
   Rating: 9.3/10
   Genres: [18, 80]
```

### Run Full Application
```bash
python main.py
```

On first run, CineMatch will:
1. Check for TMDb API key
2. Fetch 10 pages (200 movies) from TMDb
3. Cache data in `data/movies.csv`
4. Display the GUI with real movie data

---

## 📊 What Data is Fetched?

From TMDb, CineMatch fetches:
- ✅ Movie Title
- ✅ Release Year
- ✅ User Rating (0-10)
- ✅ Genres
- ✅ Estimated Runtime
- ✅ Overview/Description
- ✅ Popularity Score
- ✅ Poster URL (for future use)
- ✅ Vote Count
- ✅ Original Language

### Data Processing

CineMatch automatically:
- Maps TMDb genre IDs to genre names
- Determines complexity based on genres
- Estimates runtime by genre (or fetches exact runtime if configured)
- Caches data for 7 days (configurable)

---

## ⚙️ Configuration Options

Edit `config.py` to customize TMDb integration:

```python
TMDB_CONFIG = {
    'pages_to_fetch': 10,      # Number of pages (20 movies per page)
    'total_movies': 200,       # Total movies to fetch
    'request_timeout': 10,     # Timeout in seconds
    'retry_attempts': 3,       # Retry on failure
    'cache_expiry_days': 7     # Days before refreshing data
}
```

### Fetching More Movies

To fetch more movies, increase `pages_to_fetch`:
```python
'pages_to_fetch': 20,  # Fetches 400 movies
```

### Refresh Data Sooner

To refresh data more frequently:
```python
'cache_expiry_days': 1  # Refresh daily
```

---

## 🔄 Data Management

### Cache Location
Movies are cached in: `data/movies.csv`

### Manual Refresh
To force a data refresh:
1. Delete `data/movies.csv`
2. Restart CineMatch
3. New data will be fetched from TMDb

### View Cached Data
```bash
python -c "import pandas as pd; print(pd.read_csv('data/movies.csv').head())"
```

---

## 🐛 Troubleshooting

### Issue: "TMDb API key not configured"

**Solution:**
1. Verify your `.env` file exists and contains the API key
2. Check that `python-dotenv` is installed: `pip install python-dotenv`
3. Restart your terminal/IDE after setting the environment variable

### Issue: "Error fetching from TMDb: 401 Unauthorized"

**Solution:**
1. Your API key is invalid or expired
2. Generate a new API key from TMDb
3. Update your `.env` file

### Issue: "Error fetching from TMDb: 429 Rate Limit"

**Solution:**
1. TMDb has rate limits (40 requests per 10 seconds)
2. CineMatch includes automatic rate limiting
3. Wait a few minutes and try again
4. Reduce `pages_to_fetch` in config

### Issue: "No movies fetched from TMDb"

**Solution:**
1. Check your internet connection
2. Verify TMDb API is online: [https://status.themoviedb.org/](https://status.themoviedb.org/)
3. Check terminal output for specific error messages
4. CineMatch will automatically fallback to sample data

---

## 🎯 Best Practices

### Security
- ✅ Use `.env` file for API keys
- ✅ Never commit `.env` to Git
- ✅ Add `.env` to `.gitignore`
- ❌ Don't hardcode API keys in source files

### Performance
- ✅ Let CineMatch cache data for 7 days
- ✅ Use `fetch_details=False` for faster loading
- ✅ Fetch 10-20 pages for good movie variety
- ❌ Don't fetch 100+ pages (slow and unnecessary)

### Data Quality
- ✅ Popular movies have more ratings
- ✅ TMDb ratings are community-driven
- ✅ Data is updated regularly by TMDb
- ✅ Refresh cache weekly for latest ratings

---

## 📈 API Limits

### TMDb Free Tier
- **Requests**: 40 per 10 seconds
- **Daily Limit**: Unlimited (fair use)
- **Cost**: Free forever
- **Attribution**: Required (already included in About page)

### CineMatch Usage
- **Initial Fetch**: ~10 requests (10 pages)
- **Refresh**: ~10 requests (every 7 days)
- **Monthly**: ~40 requests (very low)

---

## 🌟 Advanced Usage

### Fetch Exact Runtimes
Edit `data_manager.py` line 77:
```python
fetch_details=True  # Fetches exact runtime for each movie
```

⚠️ **Warning**: This makes 200+ additional API calls (slower)

### Search for Specific Movies
```python
from tmdb_fetcher import TMDbFetcher

fetcher = TMDbFetcher()
results = fetcher.search_movies("Inception")
print(results[0]['title'])
```

### Get Movie Details
```python
from tmdb_fetcher import TMDbFetcher

fetcher = TMDbFetcher()
details = fetcher.fetch_movie_details(27205)  # Inception
print(details['runtime'])  # 148 minutes
```

---

## 🎓 Learning Resources

- **TMDb API Docs**: [https://developers.themoviedb.org/3](https://developers.themoviedb.org/3)
- **Getting Started**: [https://www.themoviedb.org/documentation/api](https://www.themoviedb.org/documentation/api)
- **API Reference**: [https://developers.themoviedb.org/3/getting-started/introduction](https://developers.themoviedb.org/3/getting-started/introduction)

---

## ✅ Verification Checklist

Before presenting your project:
- [ ] TMDb API key obtained
- [ ] `.env` file configured
- [ ] Test script runs successfully (`python tmdb_fetcher.py`)
- [ ] Main app fetches real data (`python main.py`)
- [ ] Data cached in `data/movies.csv`
- [ ] GUI displays 200+ movies
- [ ] Can explain API integration in demo

---

## 🎬 Without API Key

CineMatch works perfectly without an API key!

**What you get:**
- ✅ 50 curated classic and modern movies
- ✅ All features work identically
- ✅ Perfect for development and testing
- ✅ No setup required

**What you gain with API key:**
- ⭐ 200+ popular movies
- ⭐ Real-time TMDb ratings
- ⭐ Latest movie data
- ⭐ Automatic updates
- ⭐ More variety

---

## 📞 Support

### Common Questions

**Q: Is TMDb API free?**  
A: Yes! 100% free for educational and personal projects.

**Q: Do I need a credit card?**  
A: No. TMDb API is completely free, no card required.

**Q: Will CineMatch work without an API key?**  
A: Yes! It uses 50 sample movies automatically.

**Q: How often should I refresh data?**  
A: Weekly (7 days) is recommended. Monthly is fine too.

**Q: Can I use this for a commercial project?**  
A: TMDb requires attribution for commercial use. Check their terms.

---

**🎬 Happy movie fetching!**

For issues, check the error messages - CineMatch provides helpful troubleshooting info!
