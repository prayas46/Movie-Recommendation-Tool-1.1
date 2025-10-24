"""
CineMatch - Modern Streaming Website Style GUI (Netflix/Disney+/Prime Video)
Grid layout with hover cards, image-first design
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageDraw
from data_manager import DataManager
from file_handler import FileHandler
from mood_analyzer import MoodAnalyzer
from recommendation_engine import RecommendationEngine
from poster_manager import PosterManager
from utils import format_runtime, get_match_emoji

# Modern Streaming Website Colors
COLORS = {
    'bg': '#141414',                # Netflix dark
    'sidebar_bg': '#1f1f1f',        # Slightly lighter
    'card_bg': '#2f2f2f',           # Card background
    'card_hover': '#3f3f3f',        # Hover state
    'text': '#ffffff',              # White text
    'text_dim': '#b3b3b3',          # Dimmed text
    'primary': '#e50914',           # Netflix red
    'accent': '#00d4ff',            # Cyan accent
    'success': '#46d369',           # Green
}

class ModernStreamingGUI:
    """Netflix/Disney+ Style Movie GUI"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.file_handler = FileHandler()
        self.mood_analyzer = MoodAnalyzer()
        self.engine = RecommendationEngine(self.data_manager, self.file_handler)
        self.poster_manager = PosterManager()
        
        # Main window
        self.root = ThemedTk(theme="equilux")
        self.root.title("🎬 CineMatch - Discover Movies")
        self.root.geometry("1920x1080")
        self.root.configure(bg=COLORS['bg'])
        
        # Fonts
        self.title_font = font.Font(family="Arial", size=48, weight="bold")
        self.section_font = font.Font(family="Arial", size=20, weight="bold")
        self.card_title_font = font.Font(family="Arial", size=12, weight="bold")
        self.body_font = font.Font(family="Arial", size=10)
        
        self.create_layout()
    
    def create_layout(self):
        """Create modern layout"""
        # Top bar
        self.create_top_bar()
        
        # Main content
        self.content_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show home
        self.show_home()
    
    def create_top_bar(self):
        """Modern top navigation bar"""
        top_bar = tk.Frame(self.root, bg=COLORS['sidebar_bg'], height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo
        tk.Label(top_bar, text="🎬 CINEMATCH", 
                font=('Arial', 24, 'bold'),
                bg=COLORS['sidebar_bg'], fg=COLORS['primary']).pack(side=tk.LEFT, padx=30)
        
        # Nav buttons
        nav_frame = tk.Frame(top_bar, bg=COLORS['sidebar_bg'])
        nav_frame.pack(side=tk.LEFT, padx=50)
        
        for text, cmd in [("Home", self.show_home), 
                          ("Mood Match", self.show_mood_match),
                          ("Browse", self.show_browse),
                          ("My List", self.show_my_list)]:
            btn = tk.Label(nav_frame, text=text, font=('Arial', 14),
                          bg=COLORS['sidebar_bg'], fg=COLORS['text'],
                          cursor='hand2', padx=20)
            btn.pack(side=tk.LEFT)
            btn.bind('<Button-1>', lambda e, c=cmd: c())
            btn.bind('<Enter>', lambda e: e.widget.config(fg=COLORS['text_dim']))
            btn.bind('<Leave>', lambda e: e.widget.config(fg=COLORS['text']))
        
        # Stats
        stats = tk.Label(top_bar, text=f"📚 {len(self.data_manager.movies_df)} Movies",
                        font=('Arial', 12), bg=COLORS['sidebar_bg'], fg=COLORS['text_dim'])
        stats.pack(side=tk.RIGHT, padx=30)
    
    def clear_content(self):
        """Clear main content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Netflix-style home page"""
        self.clear_content()
        
        # Scrollable canvas
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Hero section
        hero = tk.Frame(scroll_frame, bg=COLORS['sidebar_bg'], height=400)
        hero.pack(fill=tk.X, pady=(0, 50))
        
        hero_content = tk.Frame(hero, bg=COLORS['sidebar_bg'])
        hero_content.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(hero_content, text="Discover Your Perfect Movie",
                font=self.title_font, bg=COLORS['sidebar_bg'], fg=COLORS['text']).pack(pady=20)
        tk.Label(hero_content, text="AI-powered recommendations based on your mood",
                font=('Arial', 18), bg=COLORS['sidebar_bg'], fg=COLORS['text_dim']).pack(pady=10)
        
        tk.Button(hero_content, text="🎬 Find Movies Now", command=self.show_mood_match,
                 font=('Arial', 16, 'bold'), bg=COLORS['primary'], fg='white',
                 relief=tk.FLAT, padx=40, pady=15, cursor='hand2').pack(pady=30)
        
        # Sections
        self.create_movie_row(scroll_frame, "🔥 Trending Now", 
                             self.data_manager.movies_df.nlargest(10, 'rating'))
        self.create_movie_row(scroll_frame, "⭐ Top Rated", 
                             self.data_manager.movies_df.nlargest(10, 'rating'))
        self.create_movie_row(scroll_frame, "🎬 Recently Added",
                             self.data_manager.movies_df.nlargest(10, 'year'))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_movie_row(self, parent, title, movies_df):
        """Create horizontal scrolling movie row (Netflix style)"""
        section = tk.Frame(parent, bg=COLORS['bg'])
        section.pack(fill=tk.X, pady=30, padx=50)
        
        # Section title
        tk.Label(section, text=title, font=self.section_font,
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(0, 20))
        
        # Horizontal scroll frame
        h_canvas = tk.Canvas(section, bg=COLORS['bg'], height=350, highlightthickness=0)
        h_canvas.pack(fill=tk.X)
        
        cards_frame = tk.Frame(h_canvas, bg=COLORS['bg'])
        h_canvas.create_window((0, 0), window=cards_frame, anchor='nw')
        
        # Add movie cards horizontally
        for _, movie in movies_df.iterrows():
            self.create_netflix_card(cards_frame, movie.to_dict())
        
        cards_frame.update_idletasks()
        h_canvas.configure(scrollregion=h_canvas.bbox("all"))
    
    def create_netflix_card(self, parent, movie):
        """Create Netflix-style hover card"""
        card_frame = tk.Frame(parent, bg=COLORS['bg'])
        card_frame.pack(side=tk.LEFT, padx=10)
        
        # Card container
        card = tk.Frame(card_frame, bg=COLORS['card_bg'], width=220, height=320)
        card.pack()
        card.pack_propagate(False)
        
        # Poster
        try:
            poster_url = movie.get('poster_url', '')
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(220, 320))
            poster_label = tk.Label(card, image=poster_img, bg=COLORS['card_bg'])
            poster_label.image = poster_img
            poster_label.pack(fill=tk.BOTH, expand=True)
        except:
            tk.Label(card, text="🎬\n" + movie['title'][:20], 
                    font=self.card_title_font,
                    bg=COLORS['card_bg'], fg=COLORS['text'],
                    wraplength=200).pack(expand=True)
        
        # Hover info overlay
        def show_info(e):
            info = tk.Frame(card, bg='#000000cc')  # Semi-transparent
            info.place(x=0, y=0, relwidth=1, relheight=1)
            
            tk.Label(info, text=movie['title'][:30], font=self.card_title_font,
                    bg='#000000cc', fg='white', wraplength=200).pack(pady=10)
            tk.Label(info, text=f"⭐ {movie['rating']}/10", font=self.body_font,
                    bg='#000000cc', fg='#FFD700').pack()
            tk.Label(info, text=movie['year'], font=self.body_font,
                    bg='#000000cc', fg=COLORS['text_dim']).pack(pady=5)
            
            tk.Button(info, text="▶ Watch", command=lambda: self.mark_watched(movie),
                     bg=COLORS['primary'], fg='white', relief=tk.FLAT,
                     font=self.body_font, padx=20, pady=8, cursor='hand2').pack(pady=10)
            
            card.info_overlay = info
        
        def hide_info(e):
            if hasattr(card, 'info_overlay'):
                card.info_overlay.destroy()
        
        card.bind('<Enter>', show_info)
        card.bind('<Leave>', hide_info)
    
    def show_mood_match(self):
        """Mood match page with grid results"""
        self.clear_content()
        
        # Scrollable
        canvas = tk.Canvas(self.content_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=1800)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Header
        tk.Label(scroll_frame, text="🧠 How are you feeling?",
                font=self.title_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=50)
        
        # Input area
        input_frame = tk.Frame(scroll_frame, bg=COLORS['sidebar_bg'])
        input_frame.pack(fill=tk.X, padx=200, pady=30)
        
        self.mood_entry = tk.Text(input_frame, height=4, font=('Arial', 14),
                                  bg=COLORS['card_bg'], fg=COLORS['text'],
                                  relief=tk.FLAT, padx=20, pady=20, wrap=tk.WORD)
        self.mood_entry.pack(fill=tk.X, padx=30, pady=30)
        self.mood_entry.insert('1.0', "I'm feeling...")
        
        tk.Button(input_frame, text="🎬 Find My Movies", command=lambda: self.find_mood_movies(scroll_frame),
                 font=('Arial', 16, 'bold'), bg=COLORS['primary'], fg='white',
                 relief=tk.FLAT, padx=50, pady=15, cursor='hand2').pack(pady=20)
        
        # Results area
        self.mood_results = tk.Frame(scroll_frame, bg=COLORS['bg'])
        self.mood_results.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def find_mood_movies(self, parent):
        """Find movies based on mood and show in grid"""
        mood_text = self.mood_entry.get('1.0', tk.END).strip()
        
        if not mood_text or mood_text == "I'm feeling...":
            messagebox.showwarning("Input Required", "Please describe your mood!")
            return
        
        # Clear previous
        for widget in self.mood_results.winfo_children():
            widget.destroy()
        
        # Analyze
        mood_profile = self.mood_analyzer.analyze(mood_text)
        recommendations = self.engine.get_mood_recommendations(mood_profile, n=12)
        
        # Show mood
        mood_label = tk.Label(self.mood_results, 
                             text=f"😊 {mood_profile['primary_emotion'].title()} | Energy: {mood_profile['energy_level'].title()}",
                             font=self.section_font, bg=COLORS['bg'], fg=COLORS['accent'])
        mood_label.pack(pady=20)
        
        # Grid of results
        self.create_movie_grid(self.mood_results, recommendations)
    
    def create_movie_grid(self, parent, recommendations):
        """Create grid layout for movies (4 per row)"""
        grid_frame = tk.Frame(parent, bg=COLORS['bg'])
        grid_frame.pack(fill=tk.BOTH, expand=True)
        
        row_frame = None
        for i, (movie, score, reason) in enumerate(recommendations):
            if i % 4 == 0:  # New row every 4 cards
                row_frame = tk.Frame(grid_frame, bg=COLORS['bg'])
                row_frame.pack(fill=tk.X, pady=10)
            
            self.create_grid_card(row_frame, movie, score, reason, i+1)
    
    def create_grid_card(self, parent, movie, score, reason, rank):
        """Create card for grid layout"""
        card_container = tk.Frame(parent, bg=COLORS['bg'])
        card_container.pack(side=tk.LEFT, padx=15)
        
        # Card
        card = tk.Frame(card_container, bg=COLORS['card_bg'], width=380, height=550)
        card.pack()
        card.pack_propagate(False)
        
        # Rank badge
        rank_badge = tk.Label(card, text=f"#{rank}", font=('Arial', 14, 'bold'),
                             bg=COLORS['primary'], fg='white', padx=12, pady=5)
        rank_badge.place(x=10, y=10)
        
        # Match badge
        match_badge = tk.Label(card, text=f"{score:.0f}%", font=('Arial', 14, 'bold'),
                              bg=COLORS['accent'], fg='black', padx=12, pady=5)
        match_badge.place(x=320, y=10)
        
        # Poster
        poster_frame = tk.Frame(card, bg=COLORS['card_bg'])
        poster_frame.pack(pady=50)
        
        try:
            poster_url = movie.get('poster_url', '')
            poster_img = self.poster_manager.get_poster(movie['id'], poster_url, size=(260, 390))
            poster_label = tk.Label(poster_frame, image=poster_img)
            poster_label.image = poster_img
            poster_label.pack()
        except:
            tk.Label(poster_frame, text="🎬", font=('Arial', 80),
                    bg=COLORS['card_bg'], fg=COLORS['text']).pack()
        
        # Info
        info_frame = tk.Frame(card, bg=COLORS['card_bg'])
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(info_frame, text=movie['title'][:35], font=('Arial', 13, 'bold'),
                bg=COLORS['card_bg'], fg=COLORS['text'], wraplength=350).pack()
        tk.Label(info_frame, text=f"⭐ {movie['rating']}/10 • {movie['year']}",
                font=('Arial', 11), bg=COLORS['card_bg'], fg='#FFD700').pack(pady=5)
        
        # Hover effect
        def on_enter(e):
            card.config(bg=COLORS['card_hover'])
            info_frame.config(bg=COLORS['card_hover'])
        def on_leave(e):
            card.config(bg=COLORS['card_bg'])
            info_frame.config(bg=COLORS['card_bg'])
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
    
    def show_browse(self):
        """Browse page"""
        self.clear_content()
        tk.Label(self.content_frame, text="🎯 Browse - Coming Soon",
                font=self.section_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=100)
    
    def show_my_list(self):
        """My list page"""
        self.clear_content()
        tk.Label(self.content_frame, text="📋 My List - Coming Soon",
                font=self.section_font, bg=COLORS['bg'], fg=COLORS['text']).pack(pady=100)
    
    def mark_watched(self, movie):
        """Mark movie as watched"""
        self.file_handler.add_to_watch_history(movie['id'], movie['title'], movie['genres'])
        messagebox.showinfo("Success", f"Added '{movie['title']}' to your list!")
    
    def run(self):
        """Start app"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernStreamingGUI()
    app.run()
