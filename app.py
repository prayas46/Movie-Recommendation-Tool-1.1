"""
CineMatch - Complete Modern Streaming Website GUI
Full Netflix/Disney+/Prime Video Style - All Pages Functional
"""
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from data_manager import DataManager
from file_handler import FileHandler
from mood_analyzer import MoodAnalyzer
from recommendation_engine import RecommendationEngine
from poster_manager import PosterManager
from utils import format_runtime, get_match_emoji

# Netflix/Disney+ Color Scheme
COLORS = {
    'bg': '#141414',                # Netflix black
    'nav_bg': '#000000',            # Pure black nav
    'card_bg': '#2f2f2f',           # Card background
    'card_hover': '#404040',        # Hover state
    'text': '#ffffff',              # White
    'text_dim': '#b3b3b3',          # Gray
    'primary': '#e50914',           # Netflix red
    'accent': '#00d4ff',            # Cyan
    'success': '#46d369',           # Green
    'border': '#333333',            # Dark border
}

class CineMatchModern:
    """Complete Modern Streaming Website"""
    
    def __init__(self):
        # Data
        self.data_manager = DataManager()
        self.file_handler = FileHandler()
        self.mood_analyzer = MoodAnalyzer()
        self.engine = RecommendationEngine(self.data_manager, self.file_handler)
        self.poster_manager = PosterManager()
        
        # Window
        self.root = ThemedTk(theme="equilux")
        self.root.title("🎬 CineMatch - Your Movie Universe")
        self.root.state('zoomed')  # Maximized
        self.root.configure(bg=COLORS['bg'])
        
        # Fonts
        self.hero_font = tkfont.Font(family="Arial", size=56, weight="bold")
        self.title_font = tkfont.Font(family="Arial", size=32, weight="bold")
        self.section_font = tkfont.Font(family="Arial", size=20, weight="bold")
        self.card_font = tkfont.Font(family="Arial", size=11, weight="bold")
        self.body_font = tkfont.Font(family="Arial", size=10)
        
        self.current_page = "home"
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI"""
        self.create_navbar()
        
        # Main content container
        self.main_container = tk.Frame(self.root, bg=COLORS['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.show_home()
    
    def create_navbar(self):
        """Top navigation bar"""
        nav = tk.Frame(self.root, bg=COLORS['nav_bg'], height=80)
        nav.pack(fill=tk.X)
        nav.pack_propagate(False)
        
        # Logo
        logo = tk.Label(nav, text="🎬 CINEMATCH", 
                       font=('Arial', 28, 'bold'),
                       bg=COLORS['nav_bg'], fg=COLORS['primary'])
        logo.pack(side=tk.LEFT, padx=40, pady=20)
        
        # Nav links
        nav_links = tk.Frame(nav, bg=COLORS['nav_bg'])
        nav_links.pack(side=tk.LEFT, padx=60)
        
        for text, page in [("Home", "home"), ("Discover", "discover"), 
                           ("Browse", "browse"), ("My List", "mylist")]:
            btn = tk.Label(nav_links, text=text, font=('Arial', 15),
                          bg=COLORS['nav_bg'], fg=COLORS['text'],
                          cursor='hand2', padx=20)
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind('<Button-1>', lambda e, p=page: self.navigate(p))
            btn.bind('<Enter>', lambda e: e.widget.config(fg=COLORS['text_dim']))
            btn.bind('<Leave>', lambda e: e.widget.config(fg=COLORS['text']))
        
        # Search bar
        search_frame = tk.Frame(nav, bg=COLORS['card_bg'])
        search_frame.pack(side=tk.RIGHT, padx=40)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=('Arial', 12), bg=COLORS['card_bg'], 
                               fg=COLORS['text'], relief=tk.FLAT, width=25)
        search_entry.pack(side=tk.LEFT, padx=10, pady=10)
        search_entry.insert(0, "🔍 Search movies...")
        
        # Stats
        stats = tk.Label(nav, text=f"📚 {len(self.data_manager.movies_df)} Movies Available",
                        font=('Arial', 11), bg=COLORS['nav_bg'], fg=COLORS['text_dim'])
        stats.pack(side=tk.RIGHT, padx=20)
    
    def navigate(self, page):
        """Navigate to page"""
        self.current_page = page
        if page == "home":
            self.show_home()
        elif page == "discover":
            self.show_discover()
        elif page == "browse":
            self.show_browse()
        elif page == "mylist":
            self.show_mylist()
    
    def clear_main(self):
        """Clear main content"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def create_scroll_canvas(self):
        """Create scrollable canvas - FIXED"""
        canvas = tk.Canvas(self.main_container, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        # Fixed: Bind to canvas width to make scroll_frame fill the entire width
        def configure_scroll_frame(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(scroll_window, width=e.width)
        
        canvas.bind("<Configure>", configure_scroll_frame)
        
        scroll_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return scroll_frame
    
    # ==================== HOME PAGE ====================
    def show_home(self):
        """Netflix-style home - OPTIMIZED"""
        self.clear_main()
        scroll_frame = self.create_scroll_canvas()
        
        # Hero banner
        self.create_hero(scroll_frame)
        
        # Movie rows - REDUCED to 3 rows for faster loading
        self.create_row(scroll_frame, "🔥 Trending Now", 
                       self.data_manager.movies_df.nlargest(8, 'rating'))
        self.create_row(scroll_frame, "⭐ Top Rated Movies",
                       self.data_manager.movies_df.nlargest(8, 'rating'))
        self.create_row(scroll_frame, "🎬 Latest Releases",
                       self.data_manager.movies_df.nlargest(8, 'year'))
    
    def create_hero(self, parent):
        """Hero banner - FIXED"""
        hero = tk.Frame(parent, bg=COLORS['card_bg'])
        hero.pack(fill=tk.X, pady=(0, 40))
        
        # Fixed: Use pack instead of place for better layout
        content = tk.Frame(hero, bg=COLORS['card_bg'])
        content.pack(expand=True, fill=tk.BOTH, pady=80)
        
        tk.Label(content, text="Discover Your Perfect Movie",
                font=self.hero_font, bg=COLORS['card_bg'], fg=COLORS['text']).pack(pady=20)
        tk.Label(content, text="AI-powered recommendations • 3,921 movies • Personalized for you",
                font=('Arial', 18), bg=COLORS['card_bg'], fg=COLORS['text_dim']).pack(pady=15)
        
        btn_frame = tk.Frame(content, bg=COLORS['card_bg'])
        btn_frame.pack(pady=30)
        
        play_btn = tk.Button(btn_frame, text="▶ Start Discovering", 
                            command=lambda: self.navigate("discover"),
                            font=('Arial', 16, 'bold'), bg=COLORS['primary'], 
                            fg='white', relief=tk.FLAT, padx=40, pady=15, cursor='hand2')
        play_btn.pack(side=tk.LEFT, padx=10)
        
        info_btn = tk.Button(btn_frame, text="ℹ More Info",
                            font=('Arial', 16), bg=COLORS['card_hover'], 
                            fg='white', relief=tk.FLAT, padx=40, pady=15, cursor='hand2')
        info_btn.pack(side=tk.LEFT, padx=10)
    
    def create_row(self, parent, title, movies_df):
        """Horizontal scrolling row - OPTIMIZED"""
        if movies_df.empty:
            return
            
        section = tk.Frame(parent, bg=COLORS['bg'])
        section.pack(fill=tk.X, pady=25, padx=50)
        
        tk.Label(section, text=title, font=self.section_font,
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 15))
        
        # Horizontal canvas
        h_canvas = tk.Canvas(section, bg=COLORS['bg'], height=300, highlightthickness=0)
        h_canvas.pack(fill=tk.X)
        
        cards_frame = tk.Frame(h_canvas, bg=COLORS['bg'])
        h_canvas.create_window((0, 0), window=cards_frame, anchor='nw')
        
        # OPTIMIZED: Only show first 8 movies per row for faster loading
        for _, movie in movies_df.head(8).iterrows():
            self.create_poster_card(cards_frame, movie.to_dict())
        
        cards_frame.update_idletasks()
        h_canvas.configure(scrollregion=h_canvas.bbox("all"))
    
    def create_poster_card(self, parent, movie):
        """Netflix poster card with hover"""
        card_frame = tk.Frame(parent, bg=COLORS['bg'])
        card_frame.pack(side=tk.LEFT, padx=8)
        
        card = tk.Frame(card_frame, bg=COLORS['card_bg'], width=200, height=280, cursor='hand2')
        card.pack()
        card.pack_propagate(False)
        
        try:
            poster_url = movie.get('poster_url', '')
            img = self.poster_manager.get_poster(movie['id'], poster_url, size=(200, 280))
            label = tk.Label(card, image=img)
            label.image = img
            label.pack(fill=tk.BOTH, expand=True)
        except:
            tk.Label(card, text="🎬\n" + movie['title'][:20], 
                    font=self.card_font, bg=COLORS['card_bg'], 
                    fg=COLORS['text'], wraplength=180).pack(expand=True)
        
        # Hover overlay - SIMPLIFIED
        def show_hover(e):
            try:
                # Semi-transparent overlay
                overlay = tk.Frame(card, bg='black')
                overlay.place(x=0, y=0, relwidth=1, relheight=1)
                
                tk.Label(overlay, text=movie['title'][:30], font=('Arial', 11, 'bold'),
                        bg='black', fg='white', wraplength=180).pack(pady=15)
                tk.Label(overlay, text=f"⭐ {movie['rating']}/10 • {movie['year']}",
                        bg='black', fg='#FFD700').pack(pady=5)
                
                tk.Button(overlay, text="▶ Details", 
                         command=lambda: self.show_movie_details(movie),
                         bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                         font=('Arial', 10, 'bold'), padx=20, pady=8).pack(pady=10)
                
                card.overlay = overlay
            except:
                pass
        
        def hide_hover(e):
            try:
                if hasattr(card, 'overlay'):
                    card.overlay.destroy()
            except:
                pass
        
        card.bind('<Enter>', show_hover)
        card.bind('<Leave>', hide_hover)
    
    # ==================== DISCOVER PAGE ====================
    def show_discover(self):
        """Mood-based discovery"""
        self.clear_main()
        scroll_frame = self.create_scroll_canvas()
        
        # Header
        tk.Label(scroll_frame, text="🧠 Discover by Mood",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=60)
        
        # Input
        input_card = tk.Frame(scroll_frame, bg=COLORS['card_bg'])
        input_card.pack(fill=tk.X, padx=250, pady=30)
        
        tk.Label(input_card, text="How are you feeling right now?",
                font=('Arial', 18), bg=COLORS['card_bg'], fg=COLORS['text']).pack(pady=20)
        
        self.mood_input = tk.Text(input_card, height=5, font=('Arial', 14),
                                  bg=COLORS['border'], fg=COLORS['text'],
                                  relief=tk.FLAT, padx=20, pady=15, wrap=tk.WORD)
        self.mood_input.pack(fill=tk.X, padx=30, pady=10)
        self.mood_input.insert('1.0', "I'm feeling stressed from work...")
        
        tk.Button(input_card, text="🎬 Find My Movies", 
                 command=lambda: self.discover_movies(scroll_frame),
                 font=('Arial', 16, 'bold'), bg=COLORS['primary'], fg='white',
                 relief=tk.FLAT, padx=50, pady=15, cursor='hand2').pack(pady=25)
        
        # Results
        self.discover_results = tk.Frame(scroll_frame, bg=COLORS['bg'])
        self.discover_results.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
    
    def discover_movies(self, parent):
        """Discover based on mood"""
        mood_text = self.mood_input.get('1.0', tk.END).strip()
        
        if not mood_text or len(mood_text) < 5:
            messagebox.showwarning("Input Required", "Please describe your mood!")
            return
        
        # Clear previous
        for widget in self.discover_results.winfo_children():
            widget.destroy()
        
        # Analyze
        mood_profile = self.mood_analyzer.analyze(mood_text)
        recommendations = self.engine.get_mood_recommendations(mood_profile, n=12)  # Reduced for faster loading
        
        # Show profile
        profile_frame = tk.Frame(self.discover_results, bg=COLORS['card_bg'])
        profile_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(profile_frame, 
                text=f"😊 {mood_profile['primary_emotion'].title()} | Energy: {mood_profile['energy_level'].title()} | Complexity: {mood_profile['complexity'].title()}",
                font=self.section_font, bg=COLORS['card_bg'], 
                fg=COLORS['accent']).pack(pady=20)
        
        # Grid
        self.create_movie_grid(self.discover_results, recommendations)
    
    def create_movie_grid(self, parent, recommendations):
        """3-column grid - OPTIMIZED"""
        grid = tk.Frame(parent, bg=COLORS['bg'])
        grid.pack(fill=tk.BOTH, expand=True)
        
        row_frame = None
        for i, (movie, score, reason) in enumerate(recommendations):
            if i % 3 == 0:  # 3 columns instead of 4
                row_frame = tk.Frame(grid, bg=COLORS['bg'])
                row_frame.pack(fill=tk.X, pady=15)
            
            self.create_grid_card(row_frame, movie, score, reason, i+1)
    
    def create_grid_card(self, parent, movie, score, reason, rank):
        """Grid card with badges"""
        container = tk.Frame(parent, bg=COLORS['bg'])
        container.pack(side=tk.LEFT, padx=15)
        
        card = tk.Frame(container, bg=COLORS['card_bg'], width=420, height=600, cursor='hand2')
        card.pack()
        card.pack_propagate(False)
        
        # Badges
        tk.Label(card, text=f"#{rank}", font=('Arial', 14, 'bold'),
                bg=COLORS['primary'], fg='white', padx=12, pady=6).place(x=15, y=15)
        tk.Label(card, text=f"{score:.0f}%", font=('Arial', 14, 'bold'),
                bg=COLORS['accent'], fg='black', padx=12, pady=6).place(x=350, y=15)
        
        # Poster
        poster_frame = tk.Frame(card, bg=COLORS['card_bg'])
        poster_frame.pack(pady=60)
        
        try:
            poster_url = movie.get('poster_url', '')
            img = self.poster_manager.get_poster(movie['id'], poster_url, size=(300, 450))
            label = tk.Label(poster_frame, image=img, cursor='hand2')
            label.image = img
            label.pack()
        except:
            tk.Label(poster_frame, text="🎬", font=('Arial', 100),
                    bg=COLORS['card_bg'], fg=COLORS['text']).pack()
        
        # Info
        info = tk.Frame(card, bg=COLORS['card_bg'])
        info.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(info, text=movie['title'][:40], font=('Arial', 13, 'bold'),
                bg=COLORS['card_bg'], fg=COLORS['text'], wraplength=380).pack()
        tk.Label(info, text=f"⭐ {movie['rating']}/10 • {movie['year']} • {format_runtime(movie['runtime'])}",
                font=('Arial', 10), bg=COLORS['card_bg'], fg='#FFD700').pack(pady=8)
        
        # Hover
        def on_enter(e):
            card.config(bg=COLORS['card_hover'])
            info.config(bg=COLORS['card_hover'])
        def on_leave(e):
            card.config(bg=COLORS['card_bg'])
            info.config(bg=COLORS['card_bg'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        card.bind('<Button-1>', lambda e: self.show_movie_details(movie))
    
    # ==================== BROWSE PAGE ====================
    def show_browse(self):
        """Browse with filters"""
        self.clear_main()
        scroll_frame = self.create_scroll_canvas()
        
        tk.Label(scroll_frame, text="🎯 Browse All Movies",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=50)
        
        # Filters
        filter_card = tk.Frame(scroll_frame, bg=COLORS['card_bg'])
        filter_card.pack(fill=tk.X, padx=100, pady=20)
        
        tk.Label(filter_card, text="Filters", font=self.section_font,
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(pady=15)
        
        filter_row = tk.Frame(filter_card, bg=COLORS['card_bg'])
        filter_row.pack(pady=15)
        
        # Genre
        tk.Label(filter_row, text="Genre:", font=('Arial', 12),
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(side=tk.LEFT, padx=10)
        self.genre_filter = ttk.Combobox(filter_row, values=['All'] + self.data_manager.get_all_genres()[:10],
                                         state="readonly", width=15)
        self.genre_filter.set('All')
        self.genre_filter.pack(side=tk.LEFT, padx=10)
        
        # Year
        tk.Label(filter_row, text="Year:", font=('Arial', 12),
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(side=tk.LEFT, padx=10)
        years = ['All', '2024', '2023', '2022', '2021', '2020', '2010s', '2000s', '1990s']
        self.year_filter = ttk.Combobox(filter_row, values=years, state="readonly", width=12)
        self.year_filter.set('All')
        self.year_filter.pack(side=tk.LEFT, padx=10)
        
        # Apply
        tk.Button(filter_row, text="Apply Filters", command=lambda: self.apply_filters(scroll_frame),
                 bg=COLORS['primary'], fg='white', font=('Arial', 11, 'bold'),
                 relief=tk.FLAT, padx=25, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=20)
        
        # Results
        self.browse_results = tk.Frame(scroll_frame, bg=COLORS['bg'])
        self.browse_results.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Show all initially
        self.apply_filters(scroll_frame)
    
    def apply_filters(self, parent):
        """Apply filters and show grid"""
        for widget in self.browse_results.winfo_children():
            widget.destroy()
        
        df = self.data_manager.movies_df.copy()
        
        # Filter
        genre = self.genre_filter.get()
        if genre != 'All':
            df = df[df['genres'].str.contains(genre)]
        
        df = df.head(20)  # Limit for performance
        
        tk.Label(self.browse_results, text=f"Found {len(df)} movies",
                font=('Arial', 16), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=15)
        
        # Grid
        grid = tk.Frame(self.browse_results, bg=COLORS['bg'])
        grid.pack()
        
        row_frame = None
        for i, (_, movie) in enumerate(df.iterrows()):
            if i % 5 == 0:
                row_frame = tk.Frame(grid, bg=COLORS['bg'])
                row_frame.pack(fill=tk.X, pady=10)
            
            self.create_browse_card(row_frame, movie.to_dict())
    
    def create_browse_card(self, parent, movie):
        """Browse grid card"""
        container = tk.Frame(parent, bg=COLORS['bg'])
        container.pack(side=tk.LEFT, padx=10)
        
        card = tk.Frame(container, bg=COLORS['card_bg'], width=280, height=420, cursor='hand2')
        card.pack()
        card.pack_propagate(False)
        
        # Poster
        try:
            poster_url = movie.get('poster_url', '')
            img = self.poster_manager.get_poster(movie['id'], poster_url, size=(280, 380))
            label = tk.Label(card, image=img, cursor='hand2')
            label.image = img
            label.pack(pady=10)
        except:
            tk.Label(card, text="🎬", font=('Arial', 60),
                    bg=COLORS['card_bg'], fg=COLORS['text']).pack(expand=True)
        
        # Title
        tk.Label(card, text=movie['title'][:35], font=('Arial', 10, 'bold'),
                bg=COLORS['card_bg'], fg=COLORS['text'], wraplength=260).pack(pady=10)
        
        card.bind('<Button-1>', lambda e: self.show_movie_details(movie))
        card.bind('<Enter>', lambda e: card.config(bg=COLORS['card_hover']))
        card.bind('<Leave>', lambda e: card.config(bg=COLORS['card_bg']))
    
    # ==================== MY LIST PAGE ====================
    def show_mylist(self):
        """My watched movies"""
        self.clear_main()
        scroll_frame = self.create_scroll_canvas()
        
        tk.Label(scroll_frame, text="📋 My Movie List",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=50)
        
        history = self.file_handler.get_watch_history()
        
        if not history:
            tk.Label(scroll_frame, text="Your list is empty. Start watching movies!",
                    font=('Arial', 18), bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=100)
            return
        
        # Stats
        stats_frame = tk.Frame(scroll_frame, bg=COLORS['card_bg'])
        stats_frame.pack(fill=tk.X, padx=100, pady=20)
        
        tk.Label(stats_frame, text=f"{len(history)} Movies Watched",
                font=self.section_font, bg=COLORS['card_bg'], fg=COLORS['accent']).pack(pady=20)
        
        # Grid of watched
        grid = tk.Frame(scroll_frame, bg=COLORS['bg'])
        grid.pack(padx=50, pady=30)
        
        row_frame = None
        for i, entry in enumerate(reversed(history[-20:])):
            if i % 5 == 0:
                row_frame = tk.Frame(grid, bg=COLORS['bg'])
                row_frame.pack(fill=tk.X, pady=10)
            
            movie = self.data_manager.get_movie_by_id(entry['movie_id'])
            if movie:
                self.create_browse_card(row_frame, movie)
    
    # ==================== UTILITIES ====================
    def show_movie_details(self, movie):
        """Show movie details popup"""
        messagebox.showinfo(movie['title'], 
                           f"⭐ Rating: {movie['rating']}/10\n"
                           f"📅 Year: {movie['year']}\n"
                           f"⏱ Runtime: {format_runtime(movie['runtime'])}\n"
                           f"🎭 Genres: {movie['genres'].replace('|', ', ')}")
    
    def run(self):
        """Start application"""
        self.root.mainloop()


if __name__ == "__main__":
    print("🎬 Starting CineMatch with ALL features...")
    app = CineMatchModern()
    app.run()
