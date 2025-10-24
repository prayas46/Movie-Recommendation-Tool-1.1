# 🚀 CineMatch Installation Guide

## Prerequisites

Before installing CineMatch, ensure you have:
- **Python 3.8 or higher** installed
- **pip** package manager
- **tkinter** (usually comes pre-installed with Python)

### Check Python Version
```bash
python --version
```
Should show Python 3.8 or higher.

---

## Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd Movie-Recommendation-Tool-1.1
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- pandas==2.1.0
- numpy==1.24.3
- matplotlib==3.7.2
- pillow==10.0.0

### Step 3: Verify Installation
```bash
python test_setup.py
```

You should see:
```
✅ ALL TESTS PASSED!
🎬 CineMatch is ready to run!
```

---

## Running CineMatch

### Start the Application
```bash
python main.py
```

The GUI window should open automatically!

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**On Fedora:**
```bash
sudo dnf install python3-tkinter
```

**On macOS:**
tkinter should be pre-installed. If not:
```bash
brew install python-tk
```

**On Windows:**
tkinter is usually included. Reinstall Python with "tcl/tk" option checked.

---

### Issue: "pip install fails"

**Try upgrading pip:**
```bash
python -m pip install --upgrade pip
```

**Then retry:**
```bash
pip install -r requirements.txt
```

---

### Issue: "Permission denied"

**On Linux/Mac:**
```bash
pip install --user -r requirements.txt
```

**Or use a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## First Run

### What Happens on First Run?

1. **Data folder created** - `data/` directory with CSV and JSON files
2. **Movie database generated** - 50 movies with metadata
3. **GUI opens** - Main window with navigation sidebar

### Initial Setup Complete When You See:
- 🎬 CineMatch logo in sidebar
- Home page with feature cards
- "50 Movies Available" in stats

---

## Using CineMatch

### Quick Start Guide

1. **Home Page** 🏠
   - Overview of features
   - Quick statistics

2. **Mood Match** 🧠
   - Describe your mood in the text box
   - Click "Find Perfect Movies"
   - Get personalized recommendations

3. **Browse** 🎯
   - Select your favorite genres
   - Click "Find Movies"
   - See filtered results

4. **My Stats** 📊
   - View watch history
   - See beautiful visualizations
   - Track your preferences

5. **About** ℹ️
   - Learn about the technology
   - See feature list

---

## Data Storage

### Where is data stored?

```
Movie-Recommendation-Tool-1.1/
└── data/
    ├── movies.csv           # Movie database
    ├── watch_history.json   # Your watch history
    └── user_profile.json    # Your preferences
```

### Backing Up Your Data

Simply copy the `data/` folder to backup your:
- Watch history
- User preferences
- Custom movie database (if modified)

### Resetting the App

To start fresh:
1. Delete the `data/` folder
2. Run `python main.py` again
3. Fresh database will be created

---

## Performance Tips

### For Best Performance:

1. **Keep watch history manageable**
   - Clear old history periodically
   - Use "Clear Watch History" button in Stats page

2. **Close unused visualization windows**
   - Each "Find Similar" opens a new window
   - Close when done viewing

3. **Restart if sluggish**
   - Close and reopen the application
   - Matplotlib caching will be cleared

---

## Development Mode

### Running Tests
```bash
python test_setup.py
```

### Checking Data Files
```bash
# View movies database
python -c "import pandas as pd; print(pd.read_csv('data/movies.csv').head())"

# View watch history
python -c "import json; print(json.load(open('data/watch_history.json')))"
```

---

## System Requirements

### Minimum Requirements:
- **OS**: Windows 10, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 512 MB
- **Storage**: 50 MB
- **Display**: 1024x768 resolution

### Recommended:
- **RAM**: 2 GB
- **Display**: 1920x1080 resolution
- **Storage**: 100 MB (for growth)

---

## Support

### Common Issues Solved

**Q: GUI window is too small/large**
A: The window is set to 1200x800. Resize manually or modify in `gui_manager.py` line 24.

**Q: Can I add more movies?**
A: Yes! Edit `data/movies.csv` following the same format.

**Q: Can I customize colors?**
A: Yes! Edit color values in `config.py` COLORS dictionary.

**Q: How accurate is mood detection?**
A: ~80% for common moods. Works best with descriptive text.

---

## Next Steps

1. ✅ **Installation complete** - Application is ready
2. 📖 **Read README.md** - Understand features
3. 🎬 **Watch DEMO_GUIDE.md** - Presentation tips
4. 🚀 **Launch the app** - `python main.py`
5. 🧠 **Try Mood Match** - Experience the magic!

---

## Quick Reference

```bash
# Install
pip install -r requirements.txt

# Test
python test_setup.py

# Run
python main.py

# Reset data
rm -rf data/

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

**🎬 Enjoy CineMatch! Happy movie discovering!**
