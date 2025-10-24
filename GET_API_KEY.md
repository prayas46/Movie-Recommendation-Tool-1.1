# 🔑 How to Get Your TMDb API Key (5 Minutes)

## Step 1: Create TMDb Account

1. Go to: **https://www.themoviedb.org/signup**
2. Fill in:
   - Username
   - Password  
   - Email
3. Click **"Sign Up"**
4. Check your email and **verify your account**

## Step 2: Request API Key

1. **Log in** to TMDb
2. Click your **avatar** (top right corner)
3. Click **"Settings"**
4. In the left sidebar, click **"API"**
5. Click **"Request an API Key"**

## Step 3: Fill Application Form

Choose **"Developer"** option, then fill:

- **Application Name**: CineMatch Movie Recommender
- **Application URL**: http://localhost:8000
- **Application Summary**: Educational Python project for movie recommendations using Tkinter, Pandas, and NumPy

Click **"Submit"**

## Step 4: Get Your API Key

You'll see two keys:
- ❌ **API Read Access Token (v4 auth)** - DON'T use this (it's a long JWT)
- ✅ **API Key (v3 auth)** - USE THIS ONE (32 characters like: `a1b2c3d4e5f6g7h8...`)

## Step 5: Configure CineMatch

1. Open your project folder
2. Create a file named `.env` (not .env.txt)
3. Add this line:
   ```
   TMDB_API_KEY=paste_your_32_character_key_here
   ```
4. Save the file

## Done! Now run:

```bash
python fetch_bulk_movies.py
```

This will fetch **5000+ movies** from TMDb!

---

## Alternative: Use Notepad

```bash
notepad .env
```

Paste:
```
TMDB_API_KEY=your_actual_32_char_key_here
```

Save and close.

---

**Need help? The API key should look like:**
`c6b5bd3dd8092fa01092b3d9bc78b2ba` (32 characters, letters and numbers)

**NOT like:**
`eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJj...` (this is a JWT token, wrong type!)
