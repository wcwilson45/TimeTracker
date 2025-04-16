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

# Define database paths using the project's ui/Databases folder
DB_DIR = APP_DIR / "ui" / "Databases"
DB_PATH = str(DB_DIR / "task_list.db")  # SQLite requires string paths

# Ensure database directory exists
DB_DIR.mkdir(parents=True, exist_ok=True)

# Log the paths for debugging
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
    "title": ["sf pro display", "Arial", "dejavu sans", "liberation sans", "ubuntu", "noto sans", "sans-serif"],
    "body": ["sf pro display", "Arial", "dejavu sans", "liberation sans", "ubuntu", "noto sans", "sans-serif"],
    "description": ["sf pro text", "Arial", "dejavu sans", "liberation sans", "ubuntu", "noto sans", "sans-serif"]
}

# Find available fonts
available_fonts = get_available_fonts()

# Create FONTS dictionary with first available font from each preference list
FONTS = {}
for font_type, font_list in preferred_fonts.items():
    for font in font_list:
        if font.lower() in available_fonts:
            FONTS[font_type] = (font,)
            logger.info(f"Using '{font}' for {font_type}")
            break
    if font_type not in FONTS:
        FONTS[font_type] = ("TkDefaultFont",)  # Default fallback using Tk's system font
        logger.info(f"No preferred fonts available for {font_type}, using system default")

# Check if database directory is writable
if not os.access(DB_DIR, os.W_OK):
    logger.error(f"No write permission for database directory: {DB_DIR}")

# Determine the best theme based on platform
def get_best_theme():
    """Select the most appropriate ttk theme for the current platform"""
    import platform
    system = platform.system()
    
    # Import ttk to check available themes
    try:
        import tkinter.ttk as ttk
        available_themes = ttk.Style().theme_names()
        logger.info(f"Available themes: {available_themes}")
    except Exception as e:
        logger.error(f"Error getting available themes: {e}")
        return None  # Let the application use the default theme
        
    # Select best theme by platform
    if system == 'Linux':
        # For Linux, prefer these themes in order - clam works best on most distros
        preferred_themes = ['clam', 'alt', 'default']
    elif system == 'Windows':
        preferred_themes = ['vista', 'winnative', 'xpnative', 'default']
    elif system == 'Darwin':  # macOS
        preferred_themes = ['aqua', 'clam', 'default']
    else:
        preferred_themes = ['default', 'clam', 'alt']
    
    # Return the first preferred theme that's available
    for theme in preferred_themes:
        if theme in available_themes:
            logger.info(f"Selected theme: {theme} for {system}")
            return theme
            
    # If none of the preferred themes are available, return None
    # to let the application use the default theme
    return None

# Get the best theme
THEME = get_best_theme()

# Platform-specific adjustments
import platform
system = platform.system()

if system == 'Linux':
    # Linux-specific adjustments
    FONT_ADJUSTMENT = -1  # Make fonts slightly smaller on Linux for better appearance
    PADDING_ADJUSTMENT = 2  # Extra padding for widgets on Linux
    
    # Improved window sizes for Linux - slightly larger with better proportions
    WINDOW_SIZE = {
        "main": "650x700",          # Increased width and height for main window
        "completed": "700x500",     # Larger for completed tasks view
        "small": "300x180",         # Wider small overlay
        "tags": "600x650",          # Slightly larger tags window
        "analytics": "1050x1050",   # Slightly larger analytics
        "archive": "700x650"        # Larger archive view
    }
    
    # Detect desktop environment for potential additional customizations
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    logger.info(f"Linux desktop environment: {desktop_env}")
    
    # GNOME-specific adjustments
    if 'gnome' in desktop_env:
        PADDING_ADJUSTMENT = 3  # GNOME often needs more padding
    
    # KDE-specific adjustments
    elif 'kde' in desktop_env:
        PADDING_ADJUSTMENT = 2  # KDE works well with moderate padding
    
elif system == 'Windows':
    FONT_ADJUSTMENT = 0
    PADDING_ADJUSTMENT = 0
    WINDOW_SIZE = {
        "main": "488x650",
        "completed": "600x400",
        "small": "230x160",
        "tags": "530x610",
        "analytics": "1000x1000",
        "archive": "650x600"
    }
    
elif system == 'Darwin':  # macOS
    FONT_ADJUSTMENT = 0
    PADDING_ADJUSTMENT = 1
    WINDOW_SIZE = {
        "main": "500x660",
        "completed": "620x420",
        "small": "240x170",
        "tags": "550x620",
        "analytics": "1020x1020",
        "archive": "670x620"
    }
    
else:
    # Default fallback for other platforms
    FONT_ADJUSTMENT = 0
    PADDING_ADJUSTMENT = 0
    WINDOW_SIZE = {
        "main": "500x650",
        "completed": "600x400",
        "small": "250x160",
        "tags": "530x610",
        "analytics": "1000x1000",
        "archive": "650x600"
    }

# Additional configuration specifically for high-DPI displays
try:
    # Create temporary window to check screen DPI
    temp_root = tk.Tk()
    screen_dpi = temp_root.winfo_fpixels('1i')
    temp_root.destroy()
    
    # Adjust for high-DPI screens (approximately 150+ DPI)
    if screen_dpi > 150:
        logger.info(f"High-DPI display detected ({screen_dpi} DPI)")
        
        # Increase font size for high-DPI
        FONT_ADJUSTMENT += 2
        
        # Increase window sizes for high-DPI
        for key in WINDOW_SIZE:
            # Parse dimensions
            width, height = map(int, WINDOW_SIZE[key].split('x'))
            # Increase by 20%
            width = int(width * 1.2)
            height = int(height * 1.2)
            WINDOW_SIZE[key] = f"{width}x{height}"
except Exception as e:
    logger.error(f"Error detecting screen DPI: {e}")