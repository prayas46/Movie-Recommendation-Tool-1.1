# 🚀 Quick Start: Fetch 5000+ Movies

## ⚡ Fastest Way to Get Movies

### Step 1: Get Your TMDb API Key (5 minutes)

**Go here NOW:** https://www.themoviedb.org/settings/api

**Don't have an account?**
1. Sign up: https://www.themoviedb.org/signup
2. Verify email
3. Go to Settings > API
4. Request API Key (Developer)
5. Copy the **32-character API Key (v3 auth)**

**Example key format:** `c6b5bd3dd8092fa01092b3d9bc78b2ba`

---

### Step 2: Run ONE of these commands

#### **Option A: Interactive Setup**
```bash
python setup_and_fetch.py
```
Then paste your API key when asked.

#### **Option B: Manual Setup**
Create `.env` file:
```bash
echo TMDB_API_KEY=your_actual_key_here > .env
```

Then fetch:
```bash
python fetch_bulk_movies.py
```

#### **Option C: Edit File**
1. Open `.env` in notepad:
   ```bash
   notepad .env
   ```

2. Add this line:
   ```
   TMDB_API_KEY=paste_your_32_char_key_here
   ```

3. Save and run:
   ```bash
   python fetch_bulk_movies.py
   ```

---

### Step 3: Choose How Many Movies

When asked, select:
- **1** = 100 movies (30 seconds) - Quick test
- **2** = 1000 movies (5 minutes) - Good size
- **3** = 5000 movies (25 minutes) - **Recommended**
- **4** = 10000 movies (50 minutes) - Maximum

---

## 🎯 What Happens During Fetch

```
🎬 Fetching movies from TMDb...
   ↓
📡 Making API calls (20 movies per page)
   ↓
⏱️  Progress updates every 10 pages
   ↓
🔄 Processing movie data
   ↓
💾 Saving to data/movies.csv
   ↓
✅ Done! Ready to use in CineMatch
```

---

## ⚙️ Fetch Details

**For 5000 movies:**
- **Pages needed:** 250 (20 movies per page)
- **API calls:** 250 requests
- **Rate limiting:** 0.25 seconds between calls
- **Total time:** ~25 minutes
- **File size:** ~1-2 MB

**What you get:**
- Movie ID, Title, Year
- Genres, Rating, Runtime
- Overview, Popularity
- Poster URLs
- And more!

---

## 🐛 Troubleshooting

### "401 Unauthorized"
- Your API key is wrong
- Make sure it's the **v3 API Key** (32 chars)
- NOT the "API Read Access Token" (long JWT)

### "No movies fetched"
- Check your internet connection
- Verify API key is correct
- Try with smaller number first (100 movies)

### Script hangs
- Press Ctrl+C to stop
- Partial data will be saved
- Re-run to continue

---

## ✅ After Fetch Complete

Run the app:
```bash
python main.py
```

Your CineMatch will now have **5000+ real movies** with:
- ✅ Real TMDb ratings
- ✅ Multiple genres per movie
- ✅ Accurate release years
- ✅ Movie descriptions
- ✅ All features working perfectly

---

## 🎉 Pro Tips

1. **Start small:** Try 100 movies first to test
2. **Be patient:** 5000 movies takes ~25 minutes
3. **Check progress:** Watch the console output
4. **Cache is smart:** Movies are saved, no re-fetch needed
5. **Refresh weekly:** Set to auto-refresh every 7 days

---

**Ready? Get your API key and run:**
```bash
python setup_and_fetch.py
```

**Or manually:**
```bash
# 1. Create .env
echo TMDB_API_KEY=your_key > .env

# 2. Fetch movies
python fetch_bulk_movies.py

# 3. Run app
python main.py
```

🎬 **Let's build that movie database!**
