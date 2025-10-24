"""
CineMatch - Modern Netflix/IMDb Style GUI
Modern streaming website design with grid layouts and hero sections
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

# Netflix/IMDb Inspired Color Scheme
COLORS = {
    'bg': '#141414',                # Netflix dark background
    'nav_bg': '#0a0a0a',           # Darker navigation
    'card_bg': '#2a2a2a',          # Card background
    'card_hover': '#3a3a3a',       # Hover state
    'text': '#ffffff',             # White text
    'text_dim': '#b3b3b3',         # Dimmed text
    'text_muted': '#808080',       # Muted text
    'primary': '#e50914',          # Netflix red
    'secondary': '#f5c518',        # IMDb yellow
    'accent': '#00d4ff',           # Cyan accent
    'success': '#46d369',          # Green
    'hero_gradient': '#1a1a1a',    # Hero section
}

class ModernCineMatch:
    """Modern Netflix/IMDb Style CineMatch GUI"""
    
    def __init__(self):
        # Initialize data
        self.data_manager = DataManager()
        self.file_handler = FileHandler()
        self.mood_analyzer = MoodAnalyzer()
        self.engine = RecommendationEngine(self.data_manager, self.file_handler)
        self.poster_manager = PosterManager()
        
        # Create main window
        self.root = ThemedTk(theme="equilux")
        self.root.title("🎬 CineMatch - Discover Your Perfect Movie")
        self.root.geometry("1600x900")
        self.root.configure(bg=COLORS['bg'])
        
        # Custom fonts
        self.hero_font = font.Font(family="Arial", size=54, weight="bold")
        self.title_font = font.Font(family="Arial", size=28, weight="bold")
        self.section_font = font.Font(family="Arial", size=20, weight="bold")
        self.header_font = font.Font(family="Arial", size=16, weight="bold")
        self.body_font = font.Font(family="Arial", size=11)
        self.small_font = font.Font(family="Arial", size=9)
        
        # Current page
        self.current_page = None
        
        # Pagination settings
        self.reco_page_size = 24
        self.browse_page_size = 24
        
        # Main layout
        self.create_main_layout()
        
    def _attach_mousewheel(self, canvas, scrollable_widget):
        """Attach mousewheel to canvas only when hovering scrollable_widget (Windows)."""
        def _on_mousewheel(event):
            delta = int(-1 * (event.delta / 120))
            canvas.yview_scroll(delta, "units")
            return "break"
        def _bind(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind(_):
            canvas.unbind_all("<MouseWheel>")
        scrollable_widget.bind("<Enter>", _bind)
        scrollable_widget.bind("<Leave>", _unbind)
        
    def create_main_layout(self):
        """Create main application layout with top navigation"""
        # Top Navigation Bar
        self.create_top_nav()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show home page
        self.show_home_page()
    
    def create_top_nav(self):
        """Create modern top navigation bar"""
        nav = tk.Frame(self.root, bg=COLORS['nav_bg'], height=70)
        nav.pack(fill=tk.X, side=tk.TOP)
        nav.pack_propagate(False)
        
        # Logo
        logo = tk.Label(nav, text="🎬 CINEMATCH", 
                       font=('Arial', 26, 'bold'),
                       bg=COLORS['nav_bg'], fg=COLORS['primary'])
        logo.pack(side=tk.LEFT, padx=40)
        
        # Navigation Links
        nav_links = tk.Frame(nav, bg=COLORS['nav_bg'])
        nav_links.pack(side=tk.LEFT, padx=60)
        
        self.nav_buttons = {}
        for text, cmd in [("Home", self.show_home_page),
                          ("Discover", self.show_emotional_match_page),
                          ("Browse", self.show_browse_page),
                          ("My Profile", self.show_profile_page),
                          ("About", self.show_about_page)]:
            btn = tk.Label(nav_links, text=text, 
                          font=('Arial', 14, 'bold'),
                          bg=COLORS['nav_bg'], fg=COLORS['text'], 
                          cursor='hand2', padx=18)
            btn.pack(side=tk.LEFT)
            btn.bind('<Button-1>', lambda e, c=cmd, t=text: self.nav_click(c, t))
            btn.bind('<Enter>', lambda e: e.widget.config(fg=COLORS['text_dim']))
            btn.bind('<Leave>', lambda e: self.update_nav_colors())
            self.nav_buttons[text] = btn
        
        # Stats badge
        stats = tk.Label(nav, 
                        text=f"📚 {len(self.data_manager.movies_df)} Movies",
                        font=('Arial', 12), 
                        bg=COLORS['nav_bg'], fg=COLORS['text_dim'])
        stats.pack(side=tk.RIGHT, padx=40)
    
    def nav_click(self, command, text):
        """Handle navigation click"""
        self.current_page = text
        self.update_nav_colors()
        command()
    
    def update_nav_colors(self):
        """Update navigation button colors based on current page"""
        for text, btn in self.nav_buttons.items():
            if text == self.current_page:
                btn.config(fg=COLORS['primary'])
            else:
                btn.config(fg=COLORS['text'])
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home_page(self):
        """Netflix-style home page with hero and movie rows"""
        self.clear_content()
        self.current_page = "Home"
        self.update_nav_colors()
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        # Ensure the inner frame always matches canvas width
        def _resize_scroll_frame(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window, width=canvas.winfo_width())
        canvas.bind("<Configure>", _resize_scroll_frame)
        window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        self._attach_mousewheel(canvas, scroll_frame)
        
        # HERO SECTION (compact and fully visible)
        hero = tk.Frame(scroll_frame, bg=COLORS['hero_gradient'])
        hero.pack(fill=tk.X, pady=(0, 20))
        
        hero_inner = tk.Frame(hero, bg=COLORS['hero_gradient'])
        hero_inner.pack(fill=tk.X, padx=50, pady=30)
        
        title_label = tk.Label(hero_inner, text="Discover Your Perfect Movie",
                              font=self.hero_font, bg=COLORS['hero_gradient'], fg=COLORS['text'],
                              wraplength=1200, anchor='w', justify='left')
        title_label.pack(pady=(0, 10), anchor='w')
        subtitle_label = tk.Label(hero_inner, text="AI-powered recommendations based on your emotional state",
                                 font=('Arial', 20), bg=COLORS['hero_gradient'], fg=COLORS['text_dim'],
                                 wraplength=1000, anchor='w', justify='left')
        subtitle_label.pack(pady=(0, 20), anchor='w')
        
        btn_frame = tk.Frame(hero_inner, bg=COLORS['hero_gradient'])
        btn_frame.pack(pady=10, anchor='w')
        
        discover_btn = tk.Button(btn_frame, text="🧠 Discover by Mood", 
                                command=self.show_emotional_match_page,
                                font=('Arial', 16, 'bold'), 
                                bg=COLORS['primary'], fg='white',
                                relief=tk.FLAT, padx=45, pady=18, cursor='hand2')
        discover_btn.pack(side=tk.LEFT, padx=10)
        discover_btn.bind('<Enter>', lambda e: e.widget.config(bg='#c40812'))
        discover_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['primary']))
        
        browse_btn = tk.Button(btn_frame, text="🎯 Browse Movies", 
                              command=self.show_browse_page,
                              font=('Arial', 16, 'bold'), 
                              bg=COLORS['card_bg'], fg='white',
                              relief=tk.FLAT, padx=45, pady=18, cursor='hand2')
        browse_btn.pack(side=tk.LEFT, padx=10)
        browse_btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['card_hover']))
        browse_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['card_bg']))
        
        # Separator below hero
        tk.Frame(scroll_frame, height=1, bg='#222222').pack(fill=tk.X, padx=50, pady=10)
        
        # MOVIE ROWS (ensure distinct content and spacing)
        self.create_movie_row(scroll_frame, "🔥 Trending Now", 
                             self.data_manager.movies_df.sample(min(12, len(self.data_manager.movies_df))))
        self.create_movie_row(scroll_frame, "⭐ Top Rated", 
                             self.data_manager.movies_df.nlargest(12, 'rating'))
        self.create_movie_row(scroll_frame, "🎬 Recently Added",
                             self.data_manager.movies_df.sort_values('year', ascending=False).head(12))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_movie_row(self, parent, title, movies_df):
        """Create horizontal scrolling movie row (Netflix style)"""
        section = tk.Frame(parent, bg=COLORS['bg'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Section title
        tk.Label(section, text=title, font=self.section_font,
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 15))
        
        # Horizontal scroll container (fixed height large enough for cards)
        h_canvas = tk.Canvas(section, bg=COLORS['bg'], height=360, highlightthickness=0)
        h_canvas.pack(fill=tk.X)
        
        cards_frame = tk.Frame(h_canvas, bg=COLORS['bg'])
        h_canvas.create_window((0, 0), window=cards_frame, anchor='nw')
        
        # Add movie cards
        for _, movie in movies_df.iterrows():
            self.create_netflix_card(cards_frame, movie.to_dict())
        
        cards_frame.update_idletasks()
        h_canvas.configure(scrollregion=h_canvas.bbox("all"))
        
        # Horizontal scroll: only when SHIFT is pressed; otherwise allow page to scroll
        def on_hwheel(event):
            if event.state & 0x0001:  # SHIFT pressed
                h_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
                return "break"
            return None
        h_canvas.bind('<MouseWheel>', on_hwheel)
    
    def create_netflix_card(self, parent, movie):
        """Create Netflix-style movie card with hover effect"""
        card_container = tk.Frame(parent, bg=COLORS['bg'])
        card_container.pack(side=tk.LEFT, padx=12)
        
        # Card
        card = tk.Frame(card_container, bg=COLORS['card_bg'], width=240, height=360, cursor='hand2')
        card.pack()
        card.pack_propagate(False)
        
        # Poster
        poster_container = tk.Frame(card, bg=COLORS['card_bg'])
        poster_container.pack(fill=tk.BOTH, expand=True)
        
        try:
            poster_url = movie.get('poster_url', '')
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(240, 360))
            poster_label = tk.Label(poster_container, image=poster_img, bg=COLORS['card_bg'])
            poster_label.image = poster_img
            poster_label.pack(fill=tk.BOTH, expand=True)
        except:
            tk.Label(poster_container, text="🎬\n" + movie['title'][:25], 
                    font=('Arial', 12, 'bold'),
                    bg=COLORS['card_bg'], fg=COLORS['text'],
                    wraplength=220, justify='center').pack(expand=True)
        
        # Hover overlay
        overlay = None
        
        def show_overlay(e):
            nonlocal overlay
            overlay = tk.Frame(card, bg='#000000')
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            
            content = tk.Frame(overlay, bg='#000000')
            content.place(relx=0.5, rely=0.5, anchor='center')
            
            tk.Label(content, text=movie['title'][:35], 
                    font=('Arial', 13, 'bold'),
                    bg='#000000', fg='white', 
                    wraplength=220).pack(pady=10)
            
            tk.Label(content, text=f"⭐ {movie['rating']}/10", 
                    font=('Arial', 12),
                    bg='#000000', fg='#FFD700').pack(pady=5)
            
            tk.Label(content, text=f"{movie['year']} • {format_runtime(movie['runtime'])}", 
                    font=('Arial', 10),
                    bg='#000000', fg=COLORS['text_dim']).pack(pady=3)
            
            genres = movie['genres'].replace('|', ' • ')[:30]
            tk.Label(content, text=genres, 
                    font=('Arial', 9),
                    bg='#000000', fg=COLORS['text_dim']).pack(pady=5)
            
            tk.Button(overlay, text="✅ Add to Watched",
                     command=lambda: self.mark_watched(movie, None),
                     font=('Arial', 10, 'bold'),
                     bg=COLORS['success'], fg='white',
                     relief=tk.FLAT, padx=20, pady=8, cursor='hand2').place(relx=0.5, rely=0.85, anchor='center')
        
        def hide_overlay(e):
            nonlocal overlay
            if overlay:
                overlay.destroy()
                overlay = None
        
        card.bind('<Enter>', show_overlay)
        card.bind('<Leave>', hide_overlay)
    
    def show_emotional_match_page(self):
        """Emotional Match Page - Modern Layout"""
        self.clear_content()
        self.current_page = "Discover"
        self.update_nav_colors()
        
        # Ensure previous global mousewheel binds don't interfere
        try:
            self.root.unbind_all("<MouseWheel>")
        except Exception:
            pass
        
        # Scrollable container
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        def configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window, width=canvas.winfo_width())
        
        canvas.bind("<Configure>", configure)
        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Update scrollregion whenever inner content changes (e.g., after results render)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Attach wheel only when hovering the inner content
        self._attach_mousewheel(canvas, scrollable_frame)
        
        # Hero Section
        hero = tk.Frame(scrollable_frame, bg=COLORS['hero_gradient'])
        hero.pack(fill=tk.BOTH, pady=(0, 50))
        
        # Add spacer at top
        tk.Frame(hero, bg=COLORS['hero_gradient'], height=100).pack()
        
        hero_content = tk.Frame(hero, bg=COLORS['hero_gradient'])
        hero_content.pack(pady=20)
        
        tk.Label(hero_content, text="🧠 Discover by Mood",
                font=self.hero_font, bg=COLORS['hero_gradient'], fg=COLORS['text'],
                wraplength=1200).pack(pady=20)
        tk.Label(hero_content, text="Tell us how you're feeling and we'll find your perfect movies",
                font=('Arial', 18), bg=COLORS['hero_gradient'], fg=COLORS['text_dim'],
                wraplength=1000).pack(pady=10)
        
        # Add spacer at bottom
        tk.Frame(hero, bg=COLORS['hero_gradient'], height=100).pack()
        
        # Input Section
        input_container = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        input_container.pack(fill=tk.X, padx=150, pady=30)
        
        # Input box with modern styling
        input_box = tk.Frame(input_container, bg=COLORS['card_bg'], relief=tk.FLAT)
        input_box.pack(fill=tk.X, pady=20)
        
        tk.Label(input_box, text="How are you feeling?",
                font=self.header_font, bg=COLORS['card_bg'], fg=COLORS['text']).pack(anchor='w', padx=30, pady=(20, 10))
        
        self.mood_text = scrolledtext.ScrolledText(
            input_box,
            height=4,
            font=('Arial', 13),
            wrap=tk.WORD,
            bg='#1a1a1a',
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.mood_text.pack(fill=tk.X, padx=30, pady=(0, 20))
        self.mood_text.insert('1.0', "e.g., 'I'm stressed from work and need something light' or 'Feeling adventurous and want action'")
        
        # Context options
        context_frame = tk.Frame(input_box, bg=COLORS['card_bg'])
        context_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        tk.Label(context_frame, text="Available time:", 
                font=self.body_font,
                bg=COLORS['card_bg'], fg=COLORS['text_dim']).pack(side=tk.LEFT, padx=(0, 15))
        
        self.time_var = tk.StringVar(value="Any")
        time_combo = ttk.Combobox(context_frame, textvariable=self.time_var,
                                  values=["Any", "< 90 min", "< 120 min", "< 150 min"],
                                  state="readonly", width=15, font=self.body_font)
        time_combo.pack(side=tk.LEFT)
        
        # Find button
        find_btn = tk.Button(
            input_container,
            text="🎬 Find My Perfect Movies",
            command=self.analyze_emotion,
            font=('Arial', 16, 'bold'),
            bg=COLORS['primary'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=50,
            pady=18
        )
        find_btn.pack(pady=30)
        find_btn.bind('<Enter>', lambda e: e.widget.config(bg='#c40812'))
        find_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['primary']))
        
        # Results frame
        self.results_frame = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def analyze_emotion(self):
        """Analyze mood and show recommendations in grid layout with pagination"""
        mood_text = self.mood_text.get('1.0', tk.END).strip()
        
        if not mood_text or mood_text.startswith("e.g.,"):
            messagebox.showwarning("Input Required", "Please describe how you're feeling!")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading = tk.Label(self.results_frame, text="🔮 Analyzing your emotional state...",
                          font=self.header_font, bg=COLORS['bg'], fg=COLORS['text_dim'])
        loading.pack(pady=40)
        self.root.update()
        
        # Analyze
        self.mood_profile = self.mood_analyzer.analyze(mood_text)
        # Fetch a larger pool once for smooth "Load more" (keeps UI responsive)
        self.all_recommendations = self.engine.get_mood_recommendations(self.mood_profile, n=100)
        self.reco_rendered = 0
        
        # Clear loading
        loading.destroy()
        
        # Show emotion profile badge
        profile_badge = tk.Frame(self.results_frame, bg=COLORS['card_bg'])
        profile_badge.pack(pady=20)
        
        badge_content = tk.Frame(profile_badge, bg=COLORS['card_bg'])
        badge_content.pack(padx=40, pady=20)
        
        tk.Label(badge_content, text=f"😊 {self.mood_profile['primary_emotion'].title()}", 
                font=('Arial', 14, 'bold'),
                bg=COLORS['primary'], fg='white', padx=25, pady=10).pack(side=tk.LEFT, padx=5)
        tk.Label(badge_content, text=f"Energy: {self.mood_profile['energy_level'].title()}", 
                font=('Arial', 14),
                bg=COLORS['card_hover'], fg='white', padx=25, pady=10).pack(side=tk.LEFT, padx=5)
        tk.Label(badge_content, text=f"Complexity: {self.mood_profile['complexity'].title()}", 
                font=('Arial', 14),
                bg=COLORS['card_hover'], fg='white', padx=25, pady=10).pack(side=tk.LEFT, padx=5)
        
        # Header
        tk.Label(self.results_frame, text="🎯 Your Perfect Matches",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=30, anchor='w', padx=20)
        
        # Grid container
        self.reco_grid = tk.Frame(self.results_frame, bg=COLORS['bg'])
        self.reco_grid.pack(fill=tk.BOTH, expand=True)
        self._reco_last_row = None
        
        # Load more frame
        self.reco_more_frame = tk.Frame(self.results_frame, bg=COLORS['bg'])
        self.reco_more_frame.pack(pady=10)
        
        # Render first batch
        self.render_more_recommendations()
        
    
    def render_more_recommendations(self):
        """Render next batch of recommendations into the grid"""
        # Remove previous button (if any)
        for w in self.reco_more_frame.winfo_children():
            w.destroy()
        
        start = self.reco_rendered
        end = min(start + self.reco_page_size, len(self.all_recommendations))
        
        for idx in range(start, end):
            movie, score, reason = self.all_recommendations[idx]
            # Create a new row frame every 3 cards
            if self.reco_rendered % 3 == 0:
                self._reco_last_row = tk.Frame(self.reco_grid, bg=COLORS['bg'])
                self._reco_last_row.pack(fill=tk.X, pady=15)
            self.create_result_card(self._reco_last_row, movie, score, reason, self.reco_rendered + 1, self.mood_profile['primary_emotion'])
            self.reco_rendered += 1
        
        # Add load more if items remain
        if self.reco_rendered < len(self.all_recommendations):
            remaining = len(self.all_recommendations) - self.reco_rendered
            tk.Button(self.reco_more_frame, text=f"⬇ Load more ({min(self.reco_page_size, remaining)} of {remaining} remaining)",
                     command=self.render_more_recommendations,
                     font=('Arial', 11, 'bold'), bg=COLORS['card_bg'], fg='white',
                     relief=tk.FLAT, padx=20, pady=10, cursor='hand2').pack()
        
    
    def create_result_card(self, parent, movie, score, reason, rank, mood):
        """Create modern result card for grid"""
        card_container = tk.Frame(parent, bg=COLORS['bg'])
        card_container.pack(side=tk.LEFT, padx=20, expand=True)
        
        # Card
        card = tk.Frame(card_container, bg=COLORS['card_bg'], width=450, height=340)
        card.pack()
        card.pack_propagate(False)
        
        # Rank badge
        rank_badge = tk.Label(card, text=f"#{rank}", 
                             font=('Arial', 16, 'bold'),
                             bg=COLORS['primary'], fg='white', padx=15, pady=8)
        rank_badge.place(x=15, y=15)
        
        # Match score badge
        emoji = get_match_emoji(score)
        match_badge = tk.Label(card, text=f"{emoji} {score:.0f}%", 
                              font=('Arial', 16, 'bold'),
                              bg=COLORS['secondary'], fg='#000', padx=15, pady=8)
        match_badge.place(x=340, y=15)
        
        # Content
        content = tk.Frame(card, bg=COLORS['card_bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Poster (left side)
        poster_frame = tk.Frame(content, bg=COLORS['card_bg'])
        poster_frame.pack(side=tk.LEFT, padx=(0, 15), pady=10)
        
        try:
            poster_url = movie.get('poster_url', '')
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(120, 180))
            poster_label = tk.Label(poster_frame, image=poster_img, bg=COLORS['card_bg'])
            poster_label.image = poster_img
            poster_label.pack()
        except:
            tk.Label(poster_frame, text="🎬", font=('Arial', 40),
                    bg='#1a1a1a', fg='white', width=4, height=4).pack()
        
        # Info (right side)
        info_frame = tk.Frame(content, bg=COLORS['card_bg'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        # Title
        tk.Label(info_frame, text=movie['title'][:40], 
                font=('Arial', 14, 'bold'),
                bg=COLORS['card_bg'], fg=COLORS['text'], 
                anchor='w', wraplength=260).pack(fill=tk.X, pady=(0, 5))
        
        # Rating & Year
        tk.Label(info_frame, text=f"⭐ {movie['rating']}/10  •  {movie['year']}", 
                font=('Arial', 11),
                bg=COLORS['card_bg'], fg='#FFD700', anchor='w').pack(fill=tk.X, pady=3)
        
        # Genres
        genres = movie['genres'].replace('|', ' • ')
        tk.Label(info_frame, text=genres[:35], 
                font=('Arial', 9),
                bg=COLORS['card_bg'], fg=COLORS['text_dim'], anchor='w').pack(fill=tk.X, pady=3)
        
        # Reason
        tk.Label(info_frame, text=f"💡 {reason}", 
                font=('Arial', 9, 'italic'),
                bg=COLORS['card_bg'], fg=COLORS['accent'], 
                anchor='w', wraplength=260).pack(fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        
        watch_btn = tk.Button(btn_frame, text="✅ Watched",
                             command=lambda: self.mark_watched(movie, mood),
                             font=('Arial', 9, 'bold'),
                             bg=COLORS['success'], fg='white',
                             relief=tk.FLAT, padx=15, pady=6, cursor='hand2')
        watch_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        similar_btn = tk.Button(btn_frame, text="🔍 Similar",
                               command=lambda: self.show_similar(movie['id']),
                               font=('Arial', 9, 'bold'),
                               bg=COLORS['card_hover'], fg='white',
                               relief=tk.FLAT, padx=15, pady=6, cursor='hand2')
        similar_btn.pack(side=tk.LEFT)
        
        # Hover effect
        def on_enter(e):
            card.config(bg=COLORS['card_hover'])
            content.config(bg=COLORS['card_hover'])
            poster_frame.config(bg=COLORS['card_hover'])
            info_frame.config(bg=COLORS['card_hover'])
            btn_frame.config(bg=COLORS['card_hover'])
        
        def on_leave(e):
            card.config(bg=COLORS['card_bg'])
            content.config(bg=COLORS['card_bg'])
            poster_frame.config(bg=COLORS['card_bg'])
            info_frame.config(bg=COLORS['card_bg'])
            btn_frame.config(bg=COLORS['card_bg'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
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
        """Show similar movies"""
        similar_window = tk.Toplevel(self.root)
        similar_window.title("Similar Movies")
        similar_window.geometry("1200x800")
        similar_window.configure(bg=COLORS['bg'])
        
        tk.Label(similar_window, text="🎬 Similar Movies",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=30)
        
        similar_movies = self.engine.get_similar_movies(movie_id, n=6)
        
        if similar_movies:
            # Grid layout
            grid = tk.Frame(similar_window, bg=COLORS['bg'])
            grid.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)
            
            row_frame = None
            for i, (movie, score, reason) in enumerate(similar_movies):
                if i % 3 == 0:
                    row_frame = tk.Frame(grid, bg=COLORS['bg'])
                    row_frame.pack(fill=tk.X, pady=15)
                
                self.create_result_card(row_frame, movie, score, reason, i+1, None)
    
    def render_more_browse_results(self):
        """Render the next batch of browse results"""
        # Remove old button
        for w in self.browse_more_frame.winfo_children():
            w.destroy()
        
        start = self.browse_rendered
        end = min(start + self.browse_page_size, len(self.browse_movies_list))
        
        for idx in range(start, end):
            movie = self.browse_movies_list[idx]
            if self.browse_rendered % 3 == 0:
                self._browse_last_row = tk.Frame(self.browse_grid, bg=COLORS['bg'])
                self._browse_last_row.pack(fill=tk.X, pady=15)
            self.create_browse_card(self._browse_last_row, movie)
            self.browse_rendered += 1
        
        # Force canvas scroll region update
        self.browse_grid.update_idletasks()
        
        if self.browse_rendered < len(self.browse_movies_list):
            remaining = len(self.browse_movies_list) - self.browse_rendered
            tk.Button(self.browse_more_frame, text=f"⬇ Load more ({min(self.browse_page_size, remaining)} of {remaining} remaining)",
                     command=self.render_more_browse_results,
                     font=('Arial', 11, 'bold'), bg=COLORS['card_bg'], fg='white',
                     relief=tk.FLAT, padx=20, pady=10, cursor='hand2').pack()
        
    def show_browse_page(self):
        """Browse Page with filters and grid"""
        self.clear_content()
        self.current_page = "Browse"
        self.update_nav_colors()
        
        # Scrollable container
        self.browse_canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.browse_canvas.yview)
        scrollable_frame = tk.Frame(self.browse_canvas, bg=COLORS['bg'])
        
        def configure(e):
            self.browse_canvas.configure(scrollregion=self.browse_canvas.bbox("all"))
            self.browse_canvas.itemconfig(window, width=self.browse_canvas.winfo_width())
        
        self.browse_canvas.bind("<Configure>", configure)
        # Also update when inner content changes
        scrollable_frame.bind("<Configure>", lambda e: self.browse_canvas.configure(scrollregion=self.browse_canvas.bbox("all")))
        window = self.browse_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.browse_canvas.configure(yscrollcommand=scrollbar.set)
        self._attach_mousewheel(self.browse_canvas, scrollable_frame)
        
        # Header
        tk.Label(scrollable_frame, text="🎯 Browse All Movies",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=40, padx=50, anchor='w')
        
        # Filters
        filters_container = tk.Frame(scrollable_frame, bg=COLORS['card_bg'])
        filters_container.pack(fill=tk.X, padx=50, pady=(0, 30))
        
        filter_content = tk.Frame(filters_container, bg=COLORS['card_bg'])
        filter_content.pack(padx=30, pady=25)
        
        # Genre filters
        genre_frame = tk.Frame(filter_content, bg=COLORS['card_bg'])
        genre_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        
        tk.Label(genre_frame, text="Genres", font=self.header_font,
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 10))
        
        self.genre_vars = {}
        genre_grid = tk.Frame(genre_frame, bg=COLORS['card_bg'])
        genre_grid.pack()
        
        all_genres = self.data_manager.get_all_genres()
        for i, genre in enumerate(all_genres[:12]):
            var = tk.BooleanVar()
            self.genre_vars[genre] = var
            cb = tk.Checkbutton(genre_grid, text=genre, variable=var,
                               font=self.body_font, bg=COLORS['card_bg'],
                               fg=COLORS['text'], selectcolor=COLORS['bg'],
                               activebackground=COLORS['card_bg'])
            cb.grid(row=i//2, column=i%2, sticky='w', padx=5, pady=3)
        
        # Year & Rating filters
        filters_right = tk.Frame(filter_content, bg=COLORS['card_bg'])
        filters_right.pack(side=tk.LEFT, padx=40)
        
        min_year = int(self.data_manager.movies_df['year'].min())
        max_year = int(self.data_manager.movies_df['year'].max())
        
        self.year_min_var = tk.IntVar(value=min_year)
        self.year_max_var = tk.IntVar(value=max_year)
        self.rating_var = tk.DoubleVar(value=7.0)
        
        tk.Label(filters_right, text="Year Range", font=self.header_font,
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 10))
        
        tk.Scale(filters_right, from_=min_year, to=max_year, variable=self.year_min_var,
                orient=tk.HORIZONTAL, bg=COLORS['card_bg'], fg=COLORS['text'],
                highlightthickness=0, length=200, label="From").pack(pady=5)
        
        tk.Scale(filters_right, from_=min_year, to=max_year, variable=self.year_max_var,
                orient=tk.HORIZONTAL, bg=COLORS['card_bg'], fg=COLORS['text'],
                highlightthickness=0, length=200, label="To").pack(pady=5)
        
        tk.Label(filters_right, text="Min Rating", font=self.header_font,
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(anchor='w', pady=(15, 10))
        
        tk.Scale(filters_right, from_=0, to=10, resolution=0.1, variable=self.rating_var,
                orient=tk.HORIZONTAL, bg=COLORS['card_bg'], fg=COLORS['text'],
                highlightthickness=0, length=200).pack(pady=5)
        
        # Sort options
        sort_frame = tk.Frame(filter_content, bg=COLORS['card_bg'])
        sort_frame.pack(side=tk.LEFT, padx=40)
        
        tk.Label(sort_frame, text="Sort by", font=self.header_font,
                bg=COLORS['card_bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 10))
        
        self.sort_var = tk.StringVar(value="Rating (High to Low)")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var,
                                  values=["Rating (High to Low)", "Rating (Low to High)",
                                         "Year (Newest)", "Year (Oldest)", "Title (A-Z)"],
                                  state="readonly", width=20, font=self.body_font)
        sort_combo.pack(pady=5)
        
        # Apply button
        apply_btn = tk.Button(sort_frame, text="🔍 Apply Filters",
                             command=lambda: self.apply_browse_filters(scrollable_frame),
                             font=('Arial', 12, 'bold'),
                             bg=COLORS['primary'], fg='white',
                             relief=tk.FLAT, padx=30, pady=12, cursor='hand2')
        apply_btn.pack(pady=20)
        apply_btn.bind('<Enter>', lambda e: e.widget.config(bg='#c40812'))
        apply_btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['primary']))
        
        # Results
        self.browse_results = tk.Frame(scrollable_frame, bg=COLORS['bg'])
        self.browse_results.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        self.browse_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Auto-apply on first load
        self.apply_browse_filters(scrollable_frame)
    
    def apply_browse_filters(self, parent):
        """Apply filters and show results with pagination (smooth and responsive)"""
        # Clear previous results
        for widget in self.browse_results.winfo_children():
            widget.destroy()
        
        # Get selected genres
        selected_genres = [g for g, v in self.genre_vars.items() if v.get()]
        
        # Filter
        filtered_df = self.data_manager.movies_df.copy()
        
        if selected_genres:
            filtered_df = filtered_df[
                filtered_df['genres'].apply(lambda x: any(g in x for g in selected_genres))
            ]
        
        filtered_df = filtered_df[
            (filtered_df['year'] >= self.year_min_var.get()) &
            (filtered_df['year'] <= self.year_max_var.get()) &
            (filtered_df['rating'] >= self.rating_var.get())
        ]
        
        # Sort
        sort_opt = self.sort_var.get()
        if "Rating (High" in sort_opt:
            filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif "Rating (Low" in sort_opt:
            filtered_df = filtered_df.sort_values('rating', ascending=True)
        elif "Year (Newest)" in sort_opt:
            filtered_df = filtered_df.sort_values('year', ascending=False)
        elif "Year (Oldest)" in sort_opt:
            filtered_df = filtered_df.sort_values('year', ascending=True)
        else:
            filtered_df = filtered_df.sort_values('title')
        
        # Save list for pagination
        self.browse_movies_list = [row.to_dict() for _, row in filtered_df.iterrows()]
        self.browse_rendered = 0
        
        # Count
        tk.Label(self.browse_results, text=f"Found {len(self.browse_movies_list)} movies",
                font=self.section_font, bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 15))
        
        # Grid container
        self.browse_grid = tk.Frame(self.browse_results, bg=COLORS['bg'])
        self.browse_grid.pack(fill=tk.BOTH, expand=True)
        self._browse_last_row = None
        
        # Load more frame
        self.browse_more_frame = tk.Frame(self.browse_results, bg=COLORS['bg'])
        self.browse_more_frame.pack(pady=10)
        
        # Render first batch
        self.render_more_browse_results()
        
        # Force scroll region update after initial render
        parent.update_idletasks()
        self.browse_canvas.configure(scrollregion=self.browse_canvas.bbox("all"))
        
    
    def create_browse_card(self, parent, movie):
        """Create browse card"""
        self.create_result_card(parent, movie, movie.get('rating', 0)*10, 
                               f"{movie.get('genres','').split('|')[0]} movie", 0, None)
    
    def show_profile_page(self):
        """User profile page"""
        self.clear_content()
        self.current_page = "My Profile"
        self.update_nav_colors()
        
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        tk.Label(scroll_frame, text="📊 Your Movie Profile",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=40, padx=50, anchor='w')
        
        watch_history = self.file_handler.get_watch_history()
        
        if not watch_history:
            tk.Label(scroll_frame, text="👋 Start watching movies to build your profile!",
                    font=self.section_font, bg=COLORS['bg'], fg=COLORS['text_dim']).pack(pady=100)
        else:
            # Stats
            stats_frame = tk.Frame(scroll_frame, bg=COLORS['bg'])
            stats_frame.pack(fill=tk.X, padx=50, pady=30)
            
            stat1 = tk.Frame(stats_frame, bg=COLORS['card_bg'], width=200, height=150)
            stat1.pack(side=tk.LEFT, padx=20)
            stat1.pack_propagate(False)
            
            tk.Label(stat1, text=len(watch_history), font=('Arial', 48, 'bold'),
                    bg=COLORS['card_bg'], fg=COLORS['primary']).pack(pady=(30, 5))
            tk.Label(stat1, text="Movies Watched", font=self.body_font,
                    bg=COLORS['card_bg'], fg=COLORS['text_dim']).pack()
            
            total_runtime = sum(self.data_manager.get_movie_by_id(e['movie_id'])['runtime']
                              for e in watch_history if self.data_manager.get_movie_by_id(e['movie_id']))
            hours = total_runtime // 60
            
            stat2 = tk.Frame(stats_frame, bg=COLORS['card_bg'], width=200, height=150)
            stat2.pack(side=tk.LEFT, padx=20)
            stat2.pack_propagate(False)
            
            tk.Label(stat2, text=f"{hours}h", font=('Arial', 48, 'bold'),
                    bg=COLORS['card_bg'], fg=COLORS['secondary']).pack(pady=(30, 5))
            tk.Label(stat2, text="Watch Time", font=self.body_font,
                    bg=COLORS['card_bg'], fg=COLORS['text_dim']).pack()
            
            # History
            tk.Label(scroll_frame, text="📜 Watch History",
                    font=self.section_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=30, padx=50, anchor='w')
            
            for entry in reversed(watch_history[-10:]):
                movie = self.data_manager.get_movie_by_id(entry['movie_id'])
                if movie:
                    item = tk.Frame(scroll_frame, bg=COLORS['card_bg'], height=80)
                    item.pack(fill=tk.X, padx=50, pady=8)
                    
                    content = tk.Frame(item, bg=COLORS['card_bg'])
                    content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
                    
                    tk.Label(content, text=f"{movie['title']} ({movie['year']})",
                            font=('Arial', 13, 'bold'), bg=COLORS['card_bg'], fg=COLORS['text'],
                            anchor='w').pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    tk.Label(content, text=f"⭐ {movie['rating']}/10",
                            font=self.body_font, bg=COLORS['card_bg'], fg='#FFD700').pack(side=tk.RIGHT, padx=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_about_page(self):
        """About page"""
        self.clear_content()
        self.current_page = "About"
        self.update_nav_colors()
        
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1500)
        
        tk.Label(scroll_frame, text="ℹ️ About CineMatch",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=40, padx=50, anchor='w')
        
        about = f"""
🎬 Welcome to CineMatch AI

CineMatch AI is your emotional movie oracle - a modern streaming-style interface
that helps you discover perfect movies based on your current mood and emotional state.

✨ What Makes Us Special

• Emotion-Driven Recommendations 🧠
  Advanced mood analysis that considers your emotional state, energy levels, 
  and context to find movies that match exactly what you need right now

• Modern Streaming Interface 🎨
  Beautiful Netflix/IMDb-inspired design with grid layouts, hover cards,
  and smooth scrolling for the best browsing experience

• Smart Algorithms 🤖
  Intelligent rule-based recommendation system with psychological profiling
  and content-based filtering

• Context Awareness 🌤️
  Considers time-of-day preferences, cognitive load, and runtime to make
  perfect recommendations for any situation

🛠️ Technology Stack

• Frontend: Tkinter with modern streaming design
• Data: Pandas, NumPy for efficient processing  
• API: TMDb integration for real movie data
• Design: Netflix/IMDb-inspired UI/UX

👨‍💻 Features

• 🎯 Dual recommendation modes (Emotional + Traditional)
• 📊 User profiling and watch statistics
• 🔍 Similar movie discovery
• 💾 Watch history tracking
• 🎨 Beautiful, intuitive modern UI
• 🖼️ High-quality movie posters

Made with ❤️ for extraordinary movie recommendations
Your {len(self.data_manager.movies_df)} movies await! 🎬
        """
        
        text_widget = tk.Text(scroll_frame, wrap=tk.WORD, font=('Arial', 12),
                             bg=COLORS['bg'], fg=COLORS['text'], relief=tk.FLAT,
                             padx=50, pady=20, height=35)
        text_widget.insert('1.0', about)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernCineMatch()
    app.run()
