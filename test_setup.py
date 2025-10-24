"""
Quick test to verify all modules are working correctly
Run this AFTER installing dependencies with: pip install -r requirements.txt
"""

print("🧪 Testing CineMatch Setup...\n")

# Test imports
print("1. Testing imports...")
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    print("   ✅ Core libraries imported successfully")
except ImportError as e:
    print(f"   ❌ Error importing libraries: {e}")
    print("   Please run: pip install -r requirements.txt")
    exit(1)

# Test custom modules
print("\n2. Testing custom modules...")
try:
    from config import COLORS, FONTS, EMOTION_GENRE_MAP
    from utils import format_runtime, calculate_similarity_score, get_time_of_day
    from mood_analyzer import MoodAnalyzer
    from data_manager import DataManager
    from file_handler import FileHandler
    from recommendation_engine import RecommendationEngine
    from visualizer import Visualizer
    print("   ✅ All custom modules imported successfully")
except ImportError as e:
    print(f"   ❌ Error importing custom modules: {e}")
    exit(1)

# Test data manager
print("\n3. Testing DataManager...")
try:
    dm = DataManager()
    print(f"   ✅ Loaded {len(dm.movies_df)} movies")
    print(f"   ✅ Found {len(dm.get_all_genres())} unique genres")
except Exception as e:
    print(f"   ❌ Error with DataManager: {e}")
    exit(1)

# Test mood analyzer
print("\n4. Testing MoodAnalyzer...")
try:
    analyzer = MoodAnalyzer()
    test_mood = "I'm stressed from exams and tired"
    result = analyzer.analyze(test_mood)
    print(f"   ✅ Detected emotion: {result['primary_emotion']}")
    print(f"   ✅ Energy level: {result['energy_level']}")
    print(f"   ✅ Complexity: {result['complexity']}")
except Exception as e:
    print(f"   ❌ Error with MoodAnalyzer: {e}")
    exit(1)

# Test recommendation engine
print("\n5. Testing RecommendationEngine...")
try:
    fh = FileHandler()
    engine = RecommendationEngine(dm, fh)
    recommendations = engine.get_mood_recommendations(result, n=3)
    print(f"   ✅ Generated {len(recommendations)} recommendations")
    if recommendations:
        top_movie = recommendations[0]
        print(f"   ✅ Top recommendation: {top_movie[0]['title']} (Score: {top_movie[1]:.1f})")
except Exception as e:
    print(f"   ❌ Error with RecommendationEngine: {e}")
    exit(1)

# Test utils
print("\n6. Testing utility functions...")
try:
    runtime = format_runtime(125)
    print(f"   ✅ format_runtime(125) = {runtime}")
    
    similarity = calculate_similarity_score(['Action', 'Drama'], ['Drama', 'Thriller'])
    print(f"   ✅ Genre similarity = {similarity:.1f}%")
    
    time_of_day = get_time_of_day()
    print(f"   ✅ Current time of day: {time_of_day}")
except Exception as e:
    print(f"   ❌ Error with utilities: {e}")
    exit(1)

# Final summary
print("\n" + "="*50)
print("✅ ALL TESTS PASSED!")
print("="*50)
print("\n🎬 CineMatch is ready to run!")
print("   Execute: python main.py")
print("\nNote: GUI will require tkinter (usually pre-installed with Python)")
