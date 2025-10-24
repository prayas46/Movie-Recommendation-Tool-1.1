"""
CineMatch - Modern Beautiful GUI (Streamlit-style design in Tkinter)
Recreates the beautiful Streamlit design using Tkinter
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
from data_manager import DataManager
from file_handler import FileHandler
from mood_analyzer import MoodAnalyzer
from recommendation_engine import RecommendationEngine
from poster_manager import PosterManager
from utils import format_runtime, get_match_emoji

# Color scheme - DARK & COOL THEME
COLORS = {
    'primary': '#667eea',           # Purple gradient 1
    'secondary': '#764ba2',         # Purple gradient 2  
    'bg': '#0e1117',                # Dark background (almost black)
    'sidebar_bg': '#262730',        # Dark sidebar
    'card_bg': '#1e1e2e',           # Dark card background
    'card_border': '#3a3a4a',       # Dark border
    'text': '#ffffff',              # White text
    'text_secondary': '#b8b9bf',    # Light gray text
    'hover': '#2a2b36',             # Hover - slightly lighter
    'button_green': '#00d9a3',      # Cool cyan-green
    'filter_bg': '#262730',         # Dark filter background
    'accent_cyan': '#00d9ff',       # Cool cyan accent
    'gradient_start': '#667eea',    # Gradient color 1
    'gradient_end': '#764ba2'       # Gradient color 2
}

class ModernCineMatch:
    """Modern Beautiful CineMatch GUI"""
    
    def __init__(self):
        # Initialize data
        self.data_manager = DataManager()
        self.file_handler = FileHandler()
        self.mood_analyzer = MoodAnalyzer()
        self.engine = RecommendationEngine(self.data_manager, self.file_handler)
        self.poster_manager = PosterManager()
        
        # Create main window
        self.root = ThemedTk(theme="equilux")  # Dark theme
        self.root.title("🎬 CineMatch AI - Your Emotional Movie Oracle")
        self.root.geometry("1600x900")
        self.root.configure(bg=COLORS['bg'])
        
        # Configure ttk style for dark theme
        style = ttk.Style()
        style.configure(".", background=COLORS['bg'], foreground=COLORS['text'])
        style.configure("TCombobox", fieldbackground=COLORS['card_bg'], background=COLORS['card_bg'], foreground=COLORS['text'])
        
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=32, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.subheader_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=11)
        self.small_font = font.Font(family="Helvetica", size=9)
        
        # Main layout
        self.create_main_layout()
        
    def create_main_layout(self):
        """Create main application layout"""
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=COLORS['sidebar_bg'], width=280, relief=tk.FLAT)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Sidebar content
        self.create_sidebar()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show home page
        self.show_emotional_match_page()
    
    def create_sidebar(self):
        """Create beautiful sidebar"""
        # Logo/Title
        title_frame = tk.Frame(self.sidebar, bg=COLORS['sidebar_bg'])
        title_frame.pack(pady=30, padx=20)
        
        # Gradient text effect (simulated with canvas)
        canvas = tk.Canvas(title_frame, width=220, height=80, bg=COLORS['sidebar_bg'], highlightthickness=0)
        canvas.pack()
        
        # Create gradient effect
        for i in range(40):
            # Interpolate between colors
            r1, g1, b1 = 102, 126, 234  # #667eea
            r2, g2, b2 = 118, 75, 162   # #764ba2
            ratio = i / 40
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_rectangle(i*5.5, 0, (i+1)*5.5, 80, fill=color, outline=color)
        
        canvas.create_text(110, 25, text="🎬 CineMatch", font=self.title_font, fill='white')
        canvas.create_text(110, 55, text="Emotional Movie Oracle", font=self.body_font, fill='white')
        
        tk.Label(self.sidebar, text="", bg=COLORS['sidebar_bg']).pack(pady=10)
        
        # Navigation
        nav_label = tk.Label(self.sidebar, text="🎛️ Navigation", 
                            font=self.subheader_font, bg=COLORS['sidebar_bg'], fg=COLORS['text'])
        nav_label.pack(pady=(10, 5), padx=20, anchor='w')
        
        # Navigation buttons
        self.create_nav_button("🧠 Emotional Match", self.show_emotional_match_page, selected=True)
        self.create_nav_button("🎯 Traditional Browse", self.show_browse_page)
        self.create_nav_button("📊 My Profile", self.show_profile_page)
        self.create_nav_button("ℹ️ About", self.show_about_page)
        
        # Separator
        sep = tk.Frame(self.sidebar, height=2, bg=COLORS['card_border'])
        sep.pack(fill=tk.X, padx=20, pady=20)
        
        # Quick stats
        stats_label = tk.Label(self.sidebar, text="🌟 Quick Stats", 
                              font=self.subheader_font, bg=COLORS['sidebar_bg'], fg=COLORS['text'])
        stats_label.pack(pady=(10, 15), padx=20, anchor='w')
        
        # Metrics
        self.create_metric("Movies in Database", len(self.data_manager.movies_df))
        self.create_metric("Your Watches", len(self.file_handler.watch_history))
    
    def create_nav_button(self, text, command, selected=False):
        """Create navigation button"""
        bg_color = COLORS['primary'] if selected else COLORS['sidebar_bg']
        fg_color = 'white' if selected else COLORS['text']
        
        btn = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=self.body_font,
            bg=bg_color,
            fg=fg_color,
            activebackground=COLORS['primary'],
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=12,
            anchor='w'
        )
        btn.pack(fill=tk.X, padx=15, pady=3)
        
        # Hover effect
        def on_enter(e):
            if not selected:
                btn.config(bg=COLORS['hover'])
        
        def on_leave(e):
            if not selected:
                btn.config(bg=COLORS['sidebar_bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_metric(self, label, value):
        """Create metric display"""
        frame = tk.Frame(self.sidebar, bg=COLORS['card_bg'], relief=tk.SOLID, bd=1, highlightbackground=COLORS['card_border'], highlightthickness=1)
        frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(frame, text=str(value), font=self.header_font, 
                bg=COLORS['card_bg'], fg=COLORS['accent_cyan']).pack(pady=(10, 0))
        tk.Label(frame, text=label, font=self.small_font, 
                bg=COLORS['card_bg'], fg=COLORS['text_secondary']).pack(pady=(0, 10))
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_emotional_match_page(self):
        """Emotional Match Page"""
        self.clear_content()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1300)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header
        header = tk.Label(scrollable_frame, text="🧠 Tell Me How You're Feeling",
                         font=self.header_font, bg=COLORS['bg'], fg=COLORS['text'])
        header.pack(pady=30, padx=50, anchor='w')
        
        # Mood input section
        input_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        input_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Left side - text input
        left_frame = tk.Frame(input_frame, bg=COLORS['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Label(left_frame, text="Describe your current mood or situation:",
                font=self.body_font, bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        
        self.mood_text = scrolledtext.ScrolledText(
            left_frame,
            height=5,
            font=self.body_font,
            wrap=tk.WORD,
            relief=tk.SOLID,
            bd=1
        )
        self.mood_text.pack(fill=tk.BOTH, expand=True)
        self.mood_text.insert('1.0', "e.g., 'I'm stressed from exams and need something light' or 'Feeling lonely after a breakup'")
        
        # Right side - context options
        right_frame = tk.Frame(input_frame, bg=COLORS['bg'], width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        tk.Label(right_frame, text="Context", font=self.subheader_font,
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 10))
        
        # Available time
        tk.Label(right_frame, text="Available time:", font=self.body_font,
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(5, 2))
        self.time_var = tk.StringVar(value="Any")
        time_combo = ttk.Combobox(right_frame, textvariable=self.time_var, 
                                  values=["Any", "< 90 min", "< 120 min", "< 150 min"],
                                  state="readonly", width=18)
        time_combo.pack(anchor='w')
        
        # Find button
        btn_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        btn_frame.pack(fill=tk.X, padx=50, pady=20)
        
        find_btn = tk.Button(
            btn_frame,
            text="🎬 Find My Perfect Movie",
            command=self.analyze_emotion,
            font=self.subheader_font,
            bg=COLORS['primary'],
            fg='white',
            activebackground=COLORS['secondary'],
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=40,
            pady=15
        )
        find_btn.pack()
        
        # Results frame
        self.results_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def analyze_emotion(self):
        """Analyze mood and show recommendations"""
        mood_text = self.mood_text.get('1.0', tk.END).strip()
        
        if not mood_text or mood_text.startswith("e.g.,"):
            messagebox.showwarning("Input Required", "Please describe how you're feeling!")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading = tk.Label(self.results_frame, text="Analyzing your emotional state...",
                          font=self.body_font, bg=COLORS['bg'], fg=COLORS['text_secondary'])
        loading.pack(pady=20)
        self.root.update()
        
        # Analyze
        mood_profile = self.mood_analyzer.analyze(mood_text)
        
        # Clear loading
        loading.destroy()
        
        # Show emotion profile
        profile_frame = tk.Frame(self.results_frame, bg=COLORS['filter_bg'], relief=tk.SOLID, bd=1)
        profile_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(profile_frame, text="📊 Your Emotional Profile",
                font=self.subheader_font, bg=COLORS['filter_bg'], fg=COLORS['text']).pack(pady=15)
        
        # Emotion badges
        badges_frame = tk.Frame(profile_frame, bg=COLORS['filter_bg'])
        badges_frame.pack(pady=(0, 15))
        
        self.create_emotion_badge(badges_frame, "😊 " + mood_profile['primary_emotion'].title())
        self.create_info_badge(badges_frame, "Energy: " + mood_profile['energy_level'].title())
        self.create_info_badge(badges_frame, "Complexity: " + mood_profile['complexity'].title())
        
        # Get recommendations
        recommendations = self.engine.get_mood_recommendations(mood_profile, n=8)
        
        # Show recommendations
        tk.Label(self.results_frame, text="🎯 Your Perfect Matches",
                font=self.header_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=20, anchor='w')
        
        for i, (movie, score, reason) in enumerate(recommendations, 1):
            self.create_movie_card(self.results_frame, movie, score, reason, i, mood_profile['primary_emotion'])
    
    def create_emotion_badge(self, parent, text):
        """Create emotion badge"""
        badge = tk.Label(
            parent,
            text=text,
            font=self.body_font,
            bg=COLORS['primary'],
            fg='white',
            padx=20,
            pady=8,
            relief=tk.FLAT
        )
        badge.pack(side=tk.LEFT, padx=5)
    
    def create_info_badge(self, parent, text):
        """Create info badge"""
        badge = tk.Label(
            parent,
            text=text,
            font=self.body_font,
            bg='white',
            fg=COLORS['text'],
            padx=15,
            pady=8,
            relief=tk.SOLID,
            bd=1
        )
        badge.pack(side=tk.LEFT, padx=5)
    
    def create_movie_card(self, parent, movie, score, reason, rank, mood=None):
        """Create large, impressive movie card like Netflix/IMDb"""
        # Card frame - LARGER
        card = tk.Frame(parent, bg=COLORS['card_bg'], relief=tk.SOLID, bd=2, highlightbackground=COLORS['card_border'], highlightthickness=1)
        card.pack(fill=tk.X, pady=15, padx=10)
        
        # Hover effect
        def on_enter(e):
            card.config(bg=COLORS['hover'], relief=tk.RAISED, bd=3, highlightbackground=COLORS['primary'])
        
        def on_leave(e):
            card.config(bg=COLORS['card_bg'], relief=tk.SOLID, bd=2, highlightbackground=COLORS['card_border'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        
        # Content frame - MORE PADDING
        content = tk.Frame(card, bg=COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Left - LARGER Poster
        left_frame = tk.Frame(content, bg=COLORS['card_bg'])
        left_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        try:
            poster_url = movie.get('poster_url', '')
            # MUCH LARGER POSTER - 200x300 instead of 120x180
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(200, 300))
            poster_label = tk.Label(left_frame, image=poster_img, bg=COLORS['card_bg'])
            poster_label.image = poster_img
            poster_label.pack()
        except:
            placeholder = tk.Label(left_frame, text="🎬", font=('Helvetica', 80),
                                  bg=COLORS['primary'], fg='white', width=5, height=4)
            placeholder.pack()
        
        # Middle - LARGER Match score
        middle_frame = tk.Frame(content, bg=COLORS['card_bg'], width=150)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=30)
        middle_frame.pack_propagate(False)
        
        emoji = get_match_emoji(score)
        tk.Label(middle_frame, text=emoji, font=('Helvetica', 60),
                bg=COLORS['card_bg']).pack(pady=20)
        tk.Label(middle_frame, text=f"{score:.0f}%", 
                font=('Helvetica', 36, 'bold'),
                bg=COLORS['card_bg'], fg=COLORS['accent_cyan']).pack(pady=5)
        tk.Label(middle_frame, text="Match", 
                font=('Helvetica', 14),
                bg=COLORS['card_bg'], fg=COLORS['text_secondary']).pack()
        
        # Right - Movie info with LARGER fonts
        right_frame = tk.Frame(content, bg=COLORS['card_bg'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Rank badge
        rank_label = tk.Label(right_frame, text=f"#{rank}",
                             font=('Helvetica', 16, 'bold'), 
                             bg=COLORS['primary'], fg='white',
                             padx=15, pady=5)
        rank_label.pack(anchor='w', pady=(0, 10))
        
        # Title - MUCH LARGER
        title_label = tk.Label(right_frame, text=f"{movie['title']} ({movie['year']})",
                              font=('Helvetica', 24, 'bold'), 
                              bg=COLORS['card_bg'], fg=COLORS['text'], anchor='w')
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # Info - LARGER font
        genres_text = movie['genres'].replace('|', ' • ')
        info_text = f"{genres_text} • {format_runtime(movie['runtime'])}"
        tk.Label(right_frame, text=info_text, 
                font=('Helvetica', 13),
                bg=COLORS['card_bg'], fg=COLORS['text_secondary'], anchor='w').pack(fill=tk.X, pady=8)
        
        # Rating - LARGER with star
        rating_frame = tk.Frame(right_frame, bg=COLORS['card_bg'])
        rating_frame.pack(fill=tk.X, pady=8)
        tk.Label(rating_frame, text=f"⭐ {movie['rating']}/10", 
                font=('Helvetica', 16, 'bold'),
                bg=COLORS['card_bg'], fg='#FFD700', anchor='w').pack(side=tk.LEFT)
        
        # Reason - LARGER font
        reason_label = tk.Label(right_frame, text=f"💡 {reason}", 
                               font=('Helvetica', 13, 'italic'),
                               bg=COLORS['card_bg'], fg=COLORS['accent_cyan'], 
                               anchor='w', wraplength=700, justify=tk.LEFT)
        reason_label.pack(fill=tk.X, pady=15)
        
        # Buttons - LARGER
        btn_frame = tk.Frame(right_frame, bg=COLORS['card_bg'])
        btn_frame.pack(fill=tk.X, pady=15)
        
        watched_btn = tk.Button(btn_frame, text="✅ Mark as Watched",
                               command=lambda: self.mark_watched(movie, mood),
                               font=('Helvetica', 12, 'bold'), 
                               bg=COLORS['button_green'], fg='white',
                               relief=tk.FLAT, padx=25, pady=12, cursor='hand2')
        watched_btn.pack(side=tk.LEFT, padx=10)
        
        # Button hover effects
        def btn_hover(e):
            e.widget.config(bg=COLORS['primary'])
        def btn_leave(e):
            e.widget.config(bg=COLORS['button_green'])
        watched_btn.bind('<Enter>', btn_hover)
        watched_btn.bind('<Leave>', btn_leave)
        
        similar_btn = tk.Button(btn_frame, text="🔍 Find Similar",
                               command=lambda: self.show_similar(movie['id']),
                               font=('Helvetica', 12, 'bold'), 
                               bg=COLORS['primary'], fg='white',
                               relief=tk.FLAT, padx=25, pady=12, cursor='hand2')
        similar_btn.pack(side=tk.LEFT, padx=10)
        
        def similar_hover(e):
            e.widget.config(bg=COLORS['secondary'])
        def similar_leave(e):
            e.widget.config(bg=COLORS['primary'])
        similar_btn.bind('<Enter>', similar_hover)
        similar_btn.bind('<Leave>', similar_leave)
    
    def mark_watched(self, movie, mood=None):
        """Mark movie as watched"""
        self.file_handler.add_to_watch_history(
            movie['id'],
            movie['title'],
            movie['genres'],
            mood
        )
        messagebox.showinfo("Success", f"'{movie['title']}' added to watch history!")
    
    def show_similar(self, movie_id):
        """Show similar movies in new window"""
        similar_window = tk.Toplevel(self.root)
        similar_window.title("Similar Movies")
        similar_window.geometry("900x700")
        similar_window.configure(bg=COLORS['bg'])
        
        tk.Label(similar_window, text="🎬 Similar Movies",
                font=self.header_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=20)
        
        # Get similar movies
        similar_movies = self.engine.get_similar_movies(movie_id, n=5)
        
        if similar_movies:
            for i, (movie, score, reason) in enumerate(similar_movies, 1):
                self.create_movie_card(similar_window, movie, score, reason, i)
    
    def show_browse_page(self):
        """Traditional Browse Page"""
        self.clear_content()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1300)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header
        header = tk.Label(scrollable_frame, text="🎯 Browse Movies",
                         font=self.header_font, bg=COLORS['bg'], fg=COLORS['text'])
        header.pack(pady=30, padx=50, anchor='w')
        
        # Filters Section
        filters_frame = tk.Frame(scrollable_frame, bg=COLORS['filter_bg'], relief=tk.SOLID, bd=1)
        filters_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Three columns for filters
        filter_row = tk.Frame(filters_frame, bg=COLORS['filter_bg'])
        filter_row.pack(fill=tk.X, padx=20, pady=20)
        
        # Column 1 - Genres
        col1 = tk.Frame(filter_row, bg=COLORS['filter_bg'])
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(col1, text="Genres:", font=self.subheader_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        
        # Genre checkboxes
        self.genre_vars = {}
        genre_frame = tk.Frame(col1, bg=COLORS['filter_bg'])
        genre_frame.pack(fill=tk.BOTH, expand=True)
        
        all_genres = self.data_manager.get_all_genres()
        for i, genre in enumerate(all_genres[:12]):  # Show first 12 genres
            var = tk.BooleanVar()
            self.genre_vars[genre] = var
            cb = tk.Checkbutton(genre_frame, text=genre, variable=var,
                               font=self.body_font, bg=COLORS['filter_bg'],
                               activebackground=COLORS['filter_bg'])
            cb.grid(row=i//2, column=i%2, sticky='w', padx=5, pady=2)
        
        # Column 2 - Year Range
        col2 = tk.Frame(filter_row, bg=COLORS['filter_bg'])
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(col2, text="Year Range:", font=self.subheader_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        
        min_year = int(self.data_manager.movies_df['year'].min())
        max_year = int(self.data_manager.movies_df['year'].max())
        
        self.year_min_var = tk.IntVar(value=min_year)
        self.year_max_var = tk.IntVar(value=max_year)
        
        tk.Label(col2, text=f"From: {min_year}", font=self.body_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w')
        year_min_scale = tk.Scale(col2, from_=min_year, to=max_year,
                                 variable=self.year_min_var, orient=tk.HORIZONTAL,
                                 bg=COLORS['filter_bg'], highlightthickness=0, length=200)
        year_min_scale.pack(fill=tk.X, pady=5)
        
        tk.Label(col2, text=f"To: {max_year}", font=self.body_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w')
        year_max_scale = tk.Scale(col2, from_=min_year, to=max_year,
                                 variable=self.year_max_var, orient=tk.HORIZONTAL,
                                 bg=COLORS['filter_bg'], highlightthickness=0, length=200)
        year_max_scale.pack(fill=tk.X, pady=5)
        
        # Column 3 - Rating
        col3 = tk.Frame(filter_row, bg=COLORS['filter_bg'])
        col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(col3, text="Minimum Rating:", font=self.subheader_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 5))
        
        self.rating_var = tk.DoubleVar(value=7.0)
        tk.Label(col3, text="Rating: 7.0", font=self.body_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(anchor='w')
        rating_scale = tk.Scale(col3, from_=0.0, to=10.0, resolution=0.1,
                               variable=self.rating_var, orient=tk.HORIZONTAL,
                               bg=COLORS['filter_bg'], highlightthickness=0, length=200)
        rating_scale.pack(fill=tk.X, pady=5)
        
        # Sort options
        sort_frame = tk.Frame(filters_frame, bg=COLORS['filter_bg'])
        sort_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(sort_frame, text="Sort by:", font=self.body_font,
                bg=COLORS['filter_bg'], fg=COLORS['text']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.sort_var = tk.StringVar(value="Rating (High to Low)")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var,
                                  values=["Rating (High to Low)", "Rating (Low to High)", 
                                         "Year (Newest)", "Year (Oldest)", "Title (A-Z)"],
                                  state="readonly", width=25)
        sort_combo.pack(side=tk.LEFT)
        
        # Apply filters button
        apply_btn = tk.Button(
            sort_frame,
            text="🔍 Apply Filters",
            command=lambda: self.apply_browse_filters(scrollable_frame),
            font=self.body_font,
            bg=COLORS['primary'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=8
        )
        apply_btn.pack(side=tk.LEFT, padx=20)
        
        # Results frame
        self.browse_results_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        self.browse_results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Auto-apply filters on first load
        self.apply_browse_filters(scrollable_frame)
    
    def apply_browse_filters(self, parent):
        """Apply filters and display results"""
        # Clear previous results
        for widget in self.browse_results_frame.winfo_children():
            widget.destroy()
        
        # Get selected genres
        selected_genres = [genre for genre, var in self.genre_vars.items() if var.get()]
        
        # Filter dataframe
        filtered_df = self.data_manager.movies_df.copy()
        
        if selected_genres:
            filtered_df = filtered_df[
                filtered_df['genres'].apply(lambda x: any(g in x for g in selected_genres))
            ]
        
        # Year filter
        filtered_df = filtered_df[
            (filtered_df['year'] >= self.year_min_var.get()) &
            (filtered_df['year'] <= self.year_max_var.get())
        ]
        
        # Rating filter
        filtered_df = filtered_df[filtered_df['rating'] >= self.rating_var.get()]
        
        # Sort
        sort_option = self.sort_var.get()
        if sort_option == "Rating (High to Low)":
            filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif sort_option == "Rating (Low to High)":
            filtered_df = filtered_df.sort_values('rating', ascending=True)
        elif sort_option == "Year (Newest)":
            filtered_df = filtered_df.sort_values('year', ascending=False)
        elif sort_option == "Year (Oldest)":
            filtered_df = filtered_df.sort_values('year', ascending=True)
        else:
            filtered_df = filtered_df.sort_values('title')
        
        # Display count
        count_label = tk.Label(self.browse_results_frame,
                              text=f"Found {len(filtered_df)} movies",
                              font=self.subheader_font, bg=COLORS['bg'], fg=COLORS['text'])
        count_label.pack(anchor='w', pady=(0, 20))
        
        # Display movies (limit to first 20 for performance)
        for _, movie in filtered_df.head(20).iterrows():
            self.create_browse_movie_card(self.browse_results_frame, movie.to_dict())
    
    def create_browse_movie_card(self, parent, movie):
        """Create LARGE movie card for browse mode"""
        # Card frame - LARGER
        card = tk.Frame(parent, bg=COLORS['card_bg'], relief=tk.SOLID, bd=2, highlightbackground=COLORS['card_border'], highlightthickness=1)
        card.pack(fill=tk.X, pady=15, padx=10)
        
        # Hover effect
        def on_enter(e):
            card.config(bg=COLORS['hover'], relief=tk.RAISED, bd=3, highlightbackground=COLORS['primary'])
        
        def on_leave(e):
            card.config(bg=COLORS['card_bg'], relief=tk.SOLID, bd=2, highlightbackground=COLORS['card_border'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        
        # Content - MORE PADDING
        content = tk.Frame(card, bg=COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Left - LARGER Poster
        left_frame = tk.Frame(content, bg=COLORS['card_bg'])
        left_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        try:
            poster_url = movie.get('poster_url', '')
            # LARGER POSTER
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(180, 270))
            poster_label = tk.Label(left_frame, image=poster_img, bg=COLORS['card_bg'])
            poster_label.image = poster_img
            poster_label.pack()
        except:
            placeholder = tk.Label(left_frame, text="🎬", font=('Helvetica', 70),
                                  bg=COLORS['primary'], fg='white', width=4, height=4)
            placeholder.pack()
        
        # Right - Movie info with LARGER fonts
        right_frame = tk.Frame(content, bg=COLORS['card_bg'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title - LARGER
        tk.Label(right_frame, text=f"{movie['title']} ({movie['year']})",
                font=('Helvetica', 22, 'bold'), 
                bg=COLORS['card_bg'], fg=COLORS['text'], anchor='w').pack(fill=tk.X, pady=(0, 10))
        
        # Info - LARGER
        genres_text = movie['genres'].replace('|', ' • ')
        info_text = f"{genres_text} • {format_runtime(movie['runtime'])}"
        tk.Label(right_frame, text=info_text, 
                font=('Helvetica', 13),
                bg=COLORS['card_bg'], fg=COLORS['text_secondary'], anchor='w').pack(fill=tk.X, pady=8)
        
        # Rating - LARGER with golden star
        tk.Label(right_frame, text=f"⭐ {movie['rating']}/10",
                font=('Helvetica', 16, 'bold'), 
                bg=COLORS['card_bg'], fg='#FFD700', anchor='w').pack(fill=tk.X, pady=10)
        
        # Button - LARGER
        watch_btn = tk.Button(right_frame, text="✅ Add to Watched",
                             command=lambda: self.mark_watched(movie, None),
                             font=('Helvetica', 12, 'bold'), 
                             bg=COLORS['button_green'], fg='white',
                             relief=tk.FLAT, padx=25, pady=12, cursor='hand2')
        watch_btn.pack(anchor='w', pady=15)
        
        # Button hover
        def btn_hover(e):
            e.widget.config(bg=COLORS['primary'])
        def btn_leave(e):
            e.widget.config(bg=COLORS['button_green'])
        watch_btn.bind('<Enter>', btn_hover)
        watch_btn.bind('<Leave>', btn_leave)
    
    def show_profile_page(self):
        """Profile Page with stats"""
        self.clear_content()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1300)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header = tk.Label(scrollable_frame, text="📊 Your Movie Profile",
                         font=self.header_font, bg=COLORS['bg'], fg=COLORS['text'])
        header.pack(pady=30, padx=50, anchor='w')
        
        watch_history = self.file_handler.get_watch_history()
        
        if not watch_history:
            tk.Label(scrollable_frame, text="👋 Start watching movies to build your profile!",
                    font=self.subheader_font, bg=COLORS['bg'], fg=COLORS['text_secondary']).pack(pady=50)
        else:
            # Stats metrics
            metrics_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
            metrics_frame.pack(fill=tk.X, padx=50, pady=20)
            
            # Movies watched
            col1 = tk.Frame(metrics_frame, bg=COLORS['filter_bg'], relief=tk.SOLID, bd=1)
            col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            tk.Label(col1, text=len(watch_history), font=self.header_font,
                    bg=COLORS['filter_bg'], fg=COLORS['primary']).pack(pady=(15, 5))
            tk.Label(col1, text="Movies Watched", font=self.body_font,
                    bg=COLORS['filter_bg'], fg=COLORS['text_secondary']).pack(pady=(0, 15))
            
            # Total runtime
            total_runtime = sum(self.data_manager.get_movie_by_id(entry['movie_id'])['runtime'] 
                              for entry in watch_history 
                              if self.data_manager.get_movie_by_id(entry['movie_id']))
            hours = total_runtime // 60
            
            col2 = tk.Frame(metrics_frame, bg=COLORS['filter_bg'], relief=tk.SOLID, bd=1)
            col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
            tk.Label(col2, text=f"{hours}h", font=self.header_font,
                    bg=COLORS['filter_bg'], fg=COLORS['primary']).pack(pady=(15, 5))
            tk.Label(col2, text="Total Watch Time", font=self.body_font,
                    bg=COLORS['filter_bg'], fg=COLORS['text_secondary']).pack(pady=(0, 15))
            
            # Watch history list
            tk.Label(scrollable_frame, text="📜 Watch History",
                    font=self.subheader_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=20, padx=50, anchor='w')
            
            for entry in reversed(watch_history[-10:]):
                movie = self.data_manager.get_movie_by_id(entry['movie_id'])
                if movie:
                    history_item = tk.Frame(scrollable_frame, bg=COLORS['filter_bg'], relief=tk.SOLID, bd=1)
                    history_item.pack(fill=tk.X, padx=50, pady=5)
                    
                    tk.Label(history_item, 
                            text=f"**{movie['title']}** ({movie['year']}) - {movie['genres'].replace('|', ' • ')} - ⭐ {movie['rating']}/10",
                            font=self.body_font, bg=COLORS['filter_bg'], fg=COLORS['text'], anchor='w').pack(padx=15, pady=10, fill=tk.X)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_about_page(self):
        """About Page"""
        self.clear_content()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=1300)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header = tk.Label(scrollable_frame, text="ℹ️ About CineMatch AI",
                         font=self.header_font, bg=COLORS['bg'], fg=COLORS['text'])
        header.pack(pady=30, padx=50, anchor='w')
        
        # Content
        about_text = """
🎬 Welcome to CineMatch AI

CineMatch AI is not just another movie recommender - it's your emotional movie oracle!

✨ What Makes Us Special

• Emotion-Driven Recommendations 🧠
  Analyzes your current emotional state, considers context (time, energy, mood),
  and recommends based on what you NEED right now

• Smart Algorithms 🤖
  Rule-based recommendation system with psychological profiling

• Context Awareness 🌤️
  Time-of-day preferences, cognitive load matching, runtime considerations

🛠️ Technology Stack

• Frontend: Tkinter with modern design
• Data: Pandas, NumPy for efficient processing
• API: TMDb integration for real movie data
• Posters: Smart caching system

👨‍💻 Project Features

• 🎯 Dual recommendation modes (Emotional + Traditional)
• 📊 User profiling and statistics
• 🔍 Similar movie discovery
• 💾 Watch history tracking
• 🎨 Beautiful, intuitive modern UI
• 🖼️ High-quality movie posters

🎓 Educational Value

This project demonstrates:
• Natural Language Processing (mood analysis)
• Rule-based algorithms
• Content-based filtering
• Emotion-to-content mapping
• Modern GUI development with Tkinter
• API integration and caching

---

Made with ❤️ for extraordinary movie recommendations
Your 3,921 movies await! 🎬
        """
        
        text_widget = tk.Text(scrollable_frame, wrap=tk.WORD, font=self.body_font,
                             bg=COLORS['bg'], fg=COLORS['text'], relief=tk.FLAT,
                             padx=50, pady=20, height=30)
        text_widget.insert('1.0', about_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernCineMatch()
    app.run()
