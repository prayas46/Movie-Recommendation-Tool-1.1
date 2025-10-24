"""
CineMatch - Main Entry Point
Run this file to start the application
"""
from data_manager import DataManager
from file_handler import FileHandler
from gui_manager import CineMatchGUI

def main():
    """Initialize and run the application"""
    print("🎬 Starting CineMatch...")
    
    # Initialize components
    data_manager = DataManager()
    file_handler = FileHandler()
    
    # Create and run GUI
    app = CineMatchGUI(data_manager, file_handler)
    app.run()

if __name__ == "__main__":
    main()
