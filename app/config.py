import os
import sys
import logging
from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TimeTracker')

def get_app_directory():
    """Get the application directory regardless of how the app is run."""
    # If running as frozen executable (like PyInstaller)
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    
    # If running as script
    return Path(__file__).parent

# Get application paths
APP_DIR = get_app_directory()
# Define BASE_DIR for compatibility with existing code
BASE_DIR = str(APP_DIR)
logger.info(f"App directory: {APP_DIR}")
logger.info(f"Base directory: {BASE_DIR}")

# Define database paths - use user's home directory to avoid permission issues
# For Linux: ~/.timetracker
# For Windows: C:\Users\username\.timetracker
USER_DATA_DIR = Path.home() / '.timetracker'
DB_DIR = USER_DATA_DIR / 'data'
DB_PATH = str(DB_DIR / 'task_list.db')  # SQLite requires string paths

# Ensure directories exist
DB_DIR.mkdir(parents=True, exist_ok=True)

# Log the paths for debugging
logger.info(f"User data directory: {USER_DATA_DIR}")
logger.info(f"Database directory: {DB_DIR}")
logger.info(f"Database path: {DB_PATH}")

# Define color scheme - keep the same as original
COLORS = {
    "background_color": "#A9A9A9",
    "grey_button_color": "#d3d3d3",
    "green_button_color": "#77DD77",
    "red_button_color": "#FF7276",
    "scroll_trough_color": "#E0E0E0",
    "main_btn_color": "#b2fba5",
    "del_btn_color": "#e99e56"
}

# Function to determine available fonts
def get_available_fonts():
    """Check which fonts are available on the system."""
    try:
        # Create a hidden root to query fonts
        root = tk.Tk()
        root.withdraw()
        available_fonts = set(f.lower() for f in tkfont.families())
        root.destroy()
        
        logger.info(f"Found {len(available_fonts)} fonts on the system")
        return available_fonts
    except Exception as e:
        logger.error(f"Error detecting fonts: {e}")
        return set()

# Define cross-platform fonts based on availability
preferred_fonts = {
    "title": ["sf pro display", "arial", "dejavu sans", "liberation sans", "sans-serif"],
    "body": ["sf pro display", "arial", "dejavu sans", "liberation sans", "sans-serif"],
    "description": ["sf pro text", "arial", "dejavu sans", "liberation sans", "sans-serif"]
}

# Find available fonts
available_fonts = get_available_fonts()

# Create FONTS dictionary with first available font from each preference list
FONTS = {}
for font_type, font_list in preferred_fonts.items():
    for font in font_list:
        if font in available_fonts:
            FONTS[font_type] = (font,)
            logger.info(f"Using '{font}' for {font_type}")
            break
    if font_type not in FONTS:
        FONTS[font_type] = ("sans-serif",)  # Default fallback
        logger.info(f"No preferred fonts available for {font_type}, using system default")

# Check if database directory is writable
if not os.access(DB_DIR, os.W_OK):
    logger.error(f"No write permission for database directory: {DB_DIR}")