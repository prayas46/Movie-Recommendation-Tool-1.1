"""
GUI Manager - Beautiful Tkinter interface with posters
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from config import COLORS, FONTS
from utils import format_runtime, get_match_emoji
from mood_analyzer import MoodAnalyzer
from recommendation_engine import RecommendationEngine
from visualizer import Visualizer
from poster_manager import PosterManager

class CineMatchGUI:
    """Main GUI application"""
    
    def __init__(self, data_manager, file_handler):
        self.data_manager = data_manager
        self.file_handler = file_handler
        self.mood_analyzer = MoodAnalyzer()
        self.engine = RecommendationEngine(data_manager, file_handler)
        self.visualizer = Visualizer()
        self.poster_manager = PosterManager()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🎬 CineMatch - Your Movie Discovery Tool")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Configure style
        self.setup_styles()
        
        # Create main layout
        self.create_main_layout()
        
        # Show home page
        self.show_home_page()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background=COLORS['bg_dark'])
        style.configure('TLabel', background=COLORS['bg_dark'], foreground=COLORS['text_primary'])
        style.configure('TButton', background=COLORS['accent'], foreground='white')
        style.map('TButton', background=[('active', COLORS['accent_light'])])
        
        # Custom button style
        style.configure('Accent.TButton', 
                       background=COLORS['accent'],
                       foreground='white',
                       padding=10,
                       font=FONTS['subheading'])
    
    def create_main_layout(self):
        """Create main application layout"""
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=COLORS['bg_medium'], width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(self.sidebar, bg=COLORS['bg_medium'])
        title_frame.pack(pady=30)
        
        tk.Label(title_frame, text="🎬", font=('Helvetica', 40), 
                bg=COLORS['bg_medium'], fg=COLORS['accent']).pack()
        tk.Label(title_frame, text="CineMatch", font=FONTS['title'],
                bg=COLORS['bg_medium'], fg=COLORS['text_primary']).pack()
        tk.Label(title_frame, text="Movie Discovery Tool", font=FONTS['small'],
                bg=COLORS['bg_medium'], fg=COLORS['text_secondary']).pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(self.sidebar, bg=COLORS['bg_medium'])
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.create_nav_button(nav_frame, "🏠 Home", self.show_home_page)
        self.create_nav_button(nav_frame, "🧠 Mood Match", self.show_mood_page)
        self.create_nav_button(nav_frame, "🎯 Browse", self.show_browse_page)
        self.create_nav_button(nav_frame, "📊 My Stats", self.show_stats_page)
        self.create_nav_button(nav_frame, "ℹ️ About", self.show_about_page)
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg_dark'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def create_nav_button(self, parent, text, command):
        """Create navigation button"""
        btn = tk.Button(parent, text=text, command=command,
                       font=FONTS['body'], bg=COLORS['bg_light'],
                       fg=COLORS['text_primary'], relief=tk.FLAT,
                       padx=20, pady=15, anchor='w',
                       activebackground=COLORS['accent'],
                       activeforeground='white',
                       cursor='hand2')
        btn.pack(fill=tk.X, pady=5)
        return btn
    
    def clear_content(self):
        """Clear main content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home_page(self):
        """Display home page"""
        self.clear_content()
        
        # Hero section
        hero = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        hero.pack(fill=tk.X, padx=50, pady=50)
        
        tk.Label(hero, text="Welcome to CineMatch! 🎬",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack()
        
        tk.Label(hero, text="Your intelligent movie discovery companion",
                font=FONTS['heading'], bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary']).pack(pady=10)
        
        # Feature cards
        features_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        features_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        features = [
            ("🧠 Mood Matching", "Tell us how you feel, get perfect recommendations", self.show_mood_page),
            ("🎯 Smart Browse", "Filter by genres, ratings, and more", self.show_browse_page),
            ("📊 Your Stats", "Beautiful visualizations of your watch history", self.show_stats_page)
        ]
        
        for i, (title, desc, cmd) in enumerate(features):
            self.create_feature_card(features_frame, title, desc, cmd, row=i)
        
        # Quick stats
        stats_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'])
        stats_frame.pack(fill=tk.X, padx=50, pady=20)
        
        total_movies = len(self.data_manager.movies_df)
        watched_movies = len(self.file_handler.watch_history)
        
        tk.Label(stats_frame, text=f"📚 {total_movies} Movies Available",
                font=FONTS['subheading'], bg=COLORS['bg_medium'],
                fg=COLORS['text_primary']).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Label(stats_frame, text=f"✅ {watched_movies} Movies Watched",
                font=FONTS['subheading'], bg=COLORS['bg_medium'],
                fg=COLORS['success']).pack(side=tk.LEFT, padx=20, pady=15)
    
    def create_feature_card(self, parent, title, description, command, row):
        """Create feature card"""
        card = tk.Frame(parent, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
        card.grid(row=row, column=0, sticky='ew', pady=10)
        parent.grid_columnconfigure(0, weight=1)
        
        tk.Label(card, text=title, font=FONTS['heading'],
                bg=COLORS['bg_medium'], fg=COLORS['accent']).pack(anchor='w', padx=20, pady=(15, 5))
        
        tk.Label(card, text=description, font=FONTS['body'],
                bg=COLORS['bg_medium'], fg=COLORS['text_secondary'],
                wraplength=500).pack(anchor='w', padx=20, pady=(0, 10))
        
        tk.Button(card, text="Explore →", command=command,
                 font=FONTS['body'], bg=COLORS['accent'],
                 fg='white', relief=tk.FLAT, padx=15, pady=8,
                 cursor='hand2').pack(anchor='w', padx=20, pady=(0, 15))
    
    def show_mood_page(self):
        """Display mood-based recommendation page"""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        header.pack(fill=tk.X, padx=50, pady=30)
        
        tk.Label(header, text="🧠 Mood-Based Recommendations",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack()
        
        tk.Label(header, text="Tell me how you're feeling right now...",
                font=FONTS['subheading'], bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary']).pack(pady=5)
        
        # Mood input
        input_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'])
        input_frame.pack(fill=tk.X, padx=50, pady=20)
        
        tk.Label(input_frame, text="How are you feeling?",
                font=FONTS['subheading'], bg=COLORS['bg_medium'],
                fg=COLORS['text_primary']).pack(anchor='w', padx=20, pady=(20, 5))
        
        self.mood_text = scrolledtext.ScrolledText(input_frame, height=4, width=80,
                                                    font=FONTS['body'], bg=COLORS['bg_light'],
                                                    fg=COLORS['text_primary'], insertbackground='white',
                                                    relief=tk.FLAT)
        self.mood_text.pack(padx=20, pady=10)
        self.mood_text.insert('1.0', "Example: I'm stressed from exams and need something light...")
        
        tk.Button(input_frame, text="🎬 Find Perfect Movies", command=self.analyze_mood,
                 font=FONTS['subheading'], bg=COLORS['accent'], fg='white',
                 relief=tk.FLAT, padx=30, pady=15, cursor='hand2').pack(pady=20)
        
        # Results frame (initially empty)
        self.mood_results_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        self.mood_results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
    
    def analyze_mood(self):
        """Analyze mood and show recommendations"""
        mood_text = self.mood_text.get('1.0', tk.END).strip()
        
        if not mood_text or mood_text.startswith("Example:"):
            messagebox.showwarning("Input Required", "Please describe how you're feeling!")
            return
        
        # Clear previous results
        for widget in self.mood_results_frame.winfo_children():
            widget.destroy()
        
        # Analyze mood
        mood_profile = self.mood_analyzer.analyze(mood_text)
        
        # Show mood analysis
        analysis_frame = tk.Frame(self.mood_results_frame, bg=COLORS['bg_medium'])
        analysis_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(analysis_frame, text="📊 Your Mood Profile",
                font=FONTS['heading'], bg=COLORS['bg_medium'],
                fg=COLORS['accent']).pack(pady=10)
        
        info_frame = tk.Frame(analysis_frame, bg=COLORS['bg_medium'])
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text=f"Primary Emotion: {mood_profile['primary_emotion'].title()}",
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['success']).pack(side=tk.LEFT, padx=20)
        
        tk.Label(info_frame, text=f"Energy: {mood_profile['energy_level'].title()}",
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['warning']).pack(side=tk.LEFT, padx=20)
        
        tk.Label(info_frame, text=f"Complexity: {mood_profile['complexity'].title()}",
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['success']).pack(side=tk.LEFT, padx=20)
        
        # Get recommendations
        recommendations = self.engine.get_mood_recommendations(mood_profile, n=5)
        
        # Display recommendations
        tk.Label(self.mood_results_frame, text="🎯 Your Perfect Matches",
                font=FONTS['heading'], bg=COLORS['bg_dark'],
                fg=COLORS['text_primary']).pack(pady=20)
        
        for i, (movie, score, reason) in enumerate(recommendations, 1):
            self.create_movie_card(self.mood_results_frame, movie, score, reason, i, mood_profile['primary_emotion'])
    
    def create_movie_card(self, parent, movie, score, reason, rank, mood=None):
        """Create beautiful movie recommendation card"""
        card = tk.Frame(parent, bg=COLORS['bg_medium'], relief=tk.RAISED, bd=2)
        card.pack(fill=tk.X, pady=10)
        
        # Left side - Rank and Score
        left_frame = tk.Frame(card, bg=COLORS['bg_medium'], width=150)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text=f"#{rank}",
                font=('Helvetica', 24, 'bold'), bg=COLORS['bg_medium'],
                fg=COLORS['text_secondary']).pack(pady=5)
        
        emoji = get_match_emoji(score)
        tk.Label(left_frame, text=emoji,
                font=('Helvetica', 30), bg=COLORS['bg_medium']).pack()
        
        tk.Label(left_frame, text=f"{score:.0f}%",
                font=FONTS['heading'], bg=COLORS['bg_medium'],
                fg=COLORS['accent']).pack()
        tk.Label(left_frame, text="Match",
                font=FONTS['small'], bg=COLORS['bg_medium'],
                fg=COLORS['text_secondary']).pack()
        
        # Right side - Movie info
        right_frame = tk.Frame(card, bg=COLORS['bg_medium'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and year
        title_text = f"{movie['title']} ({movie['year']})"
        tk.Label(right_frame, text=title_text,
                font=FONTS['heading'], bg=COLORS['bg_medium'],
                fg=COLORS['text_primary'], anchor='w').pack(fill=tk.X)
        
        # Genres and runtime
        genres_text = movie['genres'].replace('|', ' • ')
        info_text = f"{genres_text} • {format_runtime(movie['runtime'])}"
        tk.Label(right_frame, text=info_text,
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['text_secondary'], anchor='w').pack(fill=tk.X, pady=5)
        
        # Rating
        tk.Label(right_frame, text=f"⭐ {movie['rating']}/10",
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['warning'], anchor='w').pack(fill=tk.X)
        
        # Reason
        tk.Label(right_frame, text=f"💡 {reason}",
                font=FONTS['body'], bg=COLORS['bg_medium'],
                fg=COLORS['success'], anchor='w', wraplength=600).pack(fill=tk.X, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(right_frame, bg=COLORS['bg_medium'])
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(btn_frame, text="✅ Mark as Watched",
                 command=lambda: self.mark_watched(movie, mood),
                 font=FONTS['body'], bg=COLORS['success'], fg='white',
                 relief=tk.FLAT, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔍 Find Similar",
                 command=lambda: self.find_similar(movie['id']),
                 font=FONTS['body'], bg=COLORS['accent'], fg='white',
                 relief=tk.FLAT, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def mark_watched(self, movie, mood=None):
        """Mark movie as watched"""
        self.file_handler.add_to_watch_history(
            movie['id'], 
            movie['title'], 
            movie['genres'],
            mood
        )
        messagebox.showinfo("Success", f"'{movie['title']}' added to watch history!")
    
    def find_similar(self, movie_id):
        """Find and display similar movies"""
        similar_movies = self.engine.get_similar_movies(movie_id, n=5)
        
        if not similar_movies:
            messagebox.showinfo("No Results", "No similar movies found!")
            return
        
        # Create new window for similar movies
        similar_window = tk.Toplevel(self.root)
        similar_window.title("Similar Movies")
        similar_window.geometry("800x600")
        similar_window.configure(bg=COLORS['bg_dark'])
        
        tk.Label(similar_window, text="🎬 Similar Movies",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack(pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(similar_window, bg=COLORS['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(similar_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, (movie, score, reason) in enumerate(similar_movies, 1):
            self.create_movie_card(scrollable_frame, movie, score, reason, i)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
    
    def show_browse_page(self):
        """Display browse page"""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        header.pack(fill=tk.X, padx=50, pady=30)
        
        tk.Label(header, text="🎯 Browse Movies",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack()
        
        tk.Label(header, text="Filter by your favorite genres",
                font=FONTS['subheading'], bg=COLORS['bg_dark'],
                fg=COLORS['text_secondary']).pack(pady=5)
        
        # Filter frame
        filter_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'])
        filter_frame.pack(fill=tk.X, padx=50, pady=20)
        
        tk.Label(filter_frame, text="Select Your Favorite Genres:",
                font=FONTS['subheading'], bg=COLORS['bg_medium'],
                fg=COLORS['text_primary']).pack(anchor='w', padx=20, pady=(20, 10))
        
        # Genre checkboxes
        self.genre_vars = {}
        genres_frame = tk.Frame(filter_frame, bg=COLORS['bg_medium'])
        genres_frame.pack(padx=20, pady=10)
        
        all_genres = self.data_manager.get_all_genres()
        for i, genre in enumerate(all_genres):
            var = tk.BooleanVar()
            self.genre_vars[genre] = var
            
            cb = tk.Checkbutton(genres_frame, text=genre, variable=var,
                               font=FONTS['body'], bg=COLORS['bg_medium'],
                               fg=COLORS['text_primary'], selectcolor=COLORS['bg_light'],
                               activebackground=COLORS['bg_medium'],
                               activeforeground=COLORS['text_primary'])
            cb.grid(row=i//4, column=i%4, sticky='w', padx=15, pady=5)
        
        tk.Button(filter_frame, text="🔍 Find Movies", command=self.browse_movies,
                 font=FONTS['subheading'], bg=COLORS['accent'], fg='white',
                 relief=tk.FLAT, padx=30, pady=15, cursor='hand2').pack(pady=20)
        
        # Results frame
        self.browse_results_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        self.browse_results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
    
    def browse_movies(self):
        """Browse movies based on genre selection"""
        # Get selected genres
        selected_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        
        if not selected_genres:
            messagebox.showwarning("No Selection", "Please select at least one genre!")
            return
        
        # Clear previous results
        for widget in self.browse_results_frame.winfo_children():
            widget.destroy()
        
        # Get recommendations
        recommendations = self.engine.get_genre_based_recommendations(selected_genres, n=10)
        
        tk.Label(self.browse_results_frame, text=f"🎬 Found {len(recommendations)} Movies",
                font=FONTS['heading'], bg=COLORS['bg_dark'],
                fg=COLORS['text_primary']).pack(pady=10)
        
        # Scrollable results
        canvas = tk.Canvas(self.browse_results_frame, bg=COLORS['bg_dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.browse_results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, (movie, score, reason) in enumerate(recommendations, 1):
            self.create_movie_card(scrollable_frame, movie, score, reason, i)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_stats_page(self):
        """Display statistics and visualizations"""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        header.pack(fill=tk.X, padx=50, pady=30)
        
        tk.Label(header, text="📊 Your Movie Statistics",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack()
        
        watch_history = self.file_handler.get_watch_history()
        
        if not watch_history:
            tk.Label(self.content_frame, text="No watch history yet! Start watching movies to see stats.",
                    font=FONTS['heading'], bg=COLORS['bg_dark'],
                    fg=COLORS['text_secondary']).pack(pady=50)
            return
        
        # Summary stats
        summary_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        summary_frame.pack(fill=tk.X, padx=50, pady=20)
        
        stats_widget = self.visualizer.create_stats_summary(
            summary_frame, watch_history, self.data_manager
        )
        if stats_widget:
            stats_widget.pack()
        
        # Visualizations
        viz_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        # Genre distribution
        genre_counts = self.file_handler.get_genre_frequency()
        
        left_viz = tk.Frame(viz_frame, bg=COLORS['bg_dark'])
        left_viz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        pie_chart = self.visualizer.create_genre_pie_chart(left_viz, genre_counts)
        if pie_chart:
            pie_chart.pack()
        
        # Bar chart
        right_viz = tk.Frame(viz_frame, bg=COLORS['bg_dark'])
        right_viz.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        bar_chart = self.visualizer.create_genre_bar_chart(right_viz, genre_counts)
        if bar_chart:
            bar_chart.pack()
        
        # Timeline
        timeline_frame = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        timeline_frame.pack(fill=tk.X, padx=50, pady=20)
        
        timeline = self.visualizer.create_watch_timeline(timeline_frame, watch_history)
        if timeline:
            timeline.pack()
        
        # Clear history button
        tk.Button(self.content_frame, text="🗑️ Clear Watch History",
                 command=self.clear_history,
                 font=FONTS['body'], bg=COLORS['accent'], fg='white',
                 relief=tk.FLAT, padx=20, pady=10, cursor='hand2').pack(pady=20)
    
    def clear_history(self):
        """Clear watch history with confirmation"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear your watch history?"):
            self.file_handler.clear_watch_history()
            messagebox.showinfo("Success", "Watch history cleared!")
            self.show_stats_page()
    
    def show_about_page(self):
        """Display about page"""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=COLORS['bg_dark'])
        header.pack(fill=tk.X, padx=50, pady=30)
        
        tk.Label(header, text="ℹ️ About CineMatch",
                font=FONTS['title'], bg=COLORS['bg_dark'],
                fg=COLORS['accent']).pack()
        
        # Content
        content_frame = tk.Frame(self.content_frame, bg=COLORS['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        about_text = """
🎬 CineMatch - Your Intelligent Movie Discovery Tool

✨ What Makes CineMatch Special:

• 🧠 Mood-Based Recommendations
  Smart rule-based algorithms analyze your emotional state and recommend 
  the perfect movies for THIS moment.

• 🎯 Intelligent Filtering
  Browse movies by your favorite genres with smart similarity scoring 
  using NumPy algorithms.

• 📊 Beautiful Visualizations
  Track your watch history with stunning Matplotlib charts - see your 
  genre preferences evolve over time.

• 💾 Persistent History
  Your watch history is saved locally and persists across sessions.

🛠️ Technology Stack:

• Tkinter - Modern, beautiful GUI
• Pandas - Efficient movie database management
• NumPy - Smart similarity calculations
• Matplotlib - Stunning data visualizations
• File Handling - JSON-based persistent storage

🎓 Features:

✅ Rule-based mood analysis (no AI/ML needed!)
✅ Multi-factor recommendation scoring
✅ Genre similarity calculations
✅ Real-time filtering and search
✅ Watch history tracking
✅ Interactive visualizations
✅ Dark mode UI design

💡 The Magic Behind It:

CineMatch proves that you don't need complex AI to create extraordinary 
recommendations. Through clever rule-based algorithms, psychological 
profiling, and smart scoring systems, we deliver personalized movie 
suggestions that feel magical!

---

Made with ❤️ and Python
Version 1.0
        """
        
        text_widget = scrolledtext.ScrolledText(content_frame, height=25, width=80,
                                                font=FONTS['body'], bg=COLORS['bg_light'],
                                                fg=COLORS['text_primary'], relief=tk.FLAT,
                                                wrap=tk.WORD)
        text_widget.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', about_text)
        text_widget.config(state=tk.DISABLED)
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
