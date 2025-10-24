"""
Visualizer - Create beautiful charts with Matplotlib
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
from config import COLORS

class Visualizer:
    """Create stunning visualizations for movie data"""
    
    def __init__(self):
        # Set dark theme
        plt.style.use('dark_background')
    
    def create_genre_pie_chart(self, parent, genre_counts):
        """Create pie chart of watched genres"""
        if not genre_counts:
            return None
        
        fig, ax = plt.subplots(figsize=(6, 5), facecolor=COLORS['bg_dark'])
        ax.set_facecolor(COLORS['bg_dark'])
        
        # Prepare data
        genres = list(genre_counts.keys())
        counts = list(genre_counts.values())
        
        # Create custom colors
        colors_list = plt.cm.Set3(np.linspace(0, 1, len(genres)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            counts, 
            labels=genres, 
            autopct='%1.1f%%',
            colors=colors_list,
            startangle=90,
            textprops={'color': 'white', 'fontsize': 9}
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title('Your Genre Distribution', color='white', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def create_watch_timeline(self, parent, watch_history):
        """Create timeline of movies watched"""
        if not watch_history:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=COLORS['bg_dark'])
        ax.set_facecolor(COLORS['bg_dark'])
        
        # Extract dates
        dates = []
        for entry in watch_history:
            try:
                date = datetime.fromisoformat(entry['timestamp']).date()
                dates.append(date)
            except:
                pass
        
        if not dates:
            return None
        
        # Count movies per day
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.keys())
        counts = [date_counts[d] for d in sorted_dates]
        
        # Create bar chart
        bars = ax.bar(range(len(sorted_dates)), counts, color=COLORS['accent'], alpha=0.8)
        
        # Customize
        ax.set_xlabel('Date', color='white', fontsize=11, fontweight='bold')
        ax.set_ylabel('Movies Watched', color='white', fontsize=11, fontweight='bold')
        ax.set_title('Your Watch Timeline', color='white', fontsize=14, fontweight='bold', pad=20)
        
        # Format x-axis
        if len(sorted_dates) <= 10:
            ax.set_xticks(range(len(sorted_dates)))
            ax.set_xticklabels([d.strftime('%m/%d') for d in sorted_dates], 
                              rotation=45, ha='right', color='white')
        else:
            ax.set_xticks([])
            ax.set_xlabel('Time Period', color='white', fontsize=11)
        
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def create_genre_bar_chart(self, parent, genre_counts):
        """Create horizontal bar chart of genre frequency"""
        if not genre_counts:
            return None
        
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=COLORS['bg_dark'])
        ax.set_facecolor(COLORS['bg_dark'])
        
        # Sort by count
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        genres = [g[0] for g in sorted_genres]
        counts = [g[1] for g in sorted_genres]
        
        # Create gradient colors
        colors_list = plt.cm.plasma(np.linspace(0.3, 0.9, len(genres)))
        
        # Create horizontal bar chart
        bars = ax.barh(genres, counts, color=colors_list)
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{int(count)}',
                   ha='left', va='center', color='white', fontweight='bold')
        
        ax.set_xlabel('Number of Movies', color='white', fontsize=11, fontweight='bold')
        ax.set_title('Top Genres You Watch', color='white', fontsize=14, fontweight='bold', pad=20)
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas.get_tk_widget()
    
    def create_stats_summary(self, parent, watch_history, data_manager):
        """Create summary statistics visualization"""
        if not watch_history:
            return None
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6), facecolor=COLORS['bg_dark'])
        
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor(COLORS['bg_dark'])
        
        # 1. Total movies watched
        total_movies = len(watch_history)
        ax1.text(0.5, 0.5, str(total_movies), 
                ha='center', va='center', 
                fontsize=60, fontweight='bold', 
                color=COLORS['accent'])
        ax1.text(0.5, 0.2, 'Movies Watched', 
                ha='center', va='center',
                fontsize=16, color='white')
        ax1.axis('off')
        
        # 2. Total watch time
        total_minutes = 0
        for entry in watch_history:
            movie = data_manager.get_movie_by_id(entry['movie_id'])
            if movie:
                total_minutes += movie['runtime']
        total_hours = total_minutes // 60
        ax2.text(0.5, 0.5, f"{total_hours}h", 
                ha='center', va='center',
                fontsize=60, fontweight='bold',
                color=COLORS['success'])
        ax2.text(0.5, 0.2, 'Watch Time',
                ha='center', va='center',
                fontsize=16, color='white')
        ax2.axis('off')
        
        # 3. Average rating
        ratings = []
        for entry in watch_history:
            movie = data_manager.get_movie_by_id(entry['movie_id'])
            if movie:
                ratings.append(movie['rating'])
        avg_rating = np.mean(ratings) if ratings else 0
        ax3.text(0.5, 0.5, f"{avg_rating:.1f}", 
                ha='center', va='center',
                fontsize=60, fontweight='bold',
                color=COLORS['warning'])
        ax3.text(0.5, 0.2, 'Avg Rating',
                ha='center', va='center',
                fontsize=16, color='white')
        ax3.axis('off')
        
        # 4. Favorite genre
        genre_counts = {}
        for entry in watch_history:
            genres = entry['genres'].split('|')
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        if genre_counts:
            fav_genre = max(genre_counts, key=genre_counts.get)
            ax4.text(0.5, 0.5, fav_genre, 
                    ha='center', va='center',
                    fontsize=30, fontweight='bold',
                    color=COLORS['accent_light'])
            ax4.text(0.5, 0.2, 'Favorite Genre',
                    ha='center', va='center',
                    fontsize=16, color='white')
        ax4.axis('off')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas.get_tk_widget()
