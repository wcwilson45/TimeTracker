import os
import sys
import logging
from pathlib import Path

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TimeTracker')

# Get application paths
APP_DIR = Path(__file__).parent
BASE_DIR = str(APP_DIR)

# Define database paths - keep it simple with the database in the ui/Databases folder
DB_DIR = APP_DIR / "ui" / "Databases"
DB_PATH = str(DB_DIR / "task_list.db")  # SQLite requires string paths

# Ensure database directory exists
DB_DIR.mkdir(parents=True, exist_ok=True)

# Log the paths for debugging
logger.info(f"App directory: {APP_DIR}")
logger.info(f"Database directory: {DB_DIR}")
logger.info(f"Database path: {DB_PATH}")

# Simple color scheme
COLORS = {
    "background_color": "#A9A9A9",
    "grey_button_color": "#d3d3d3",
    "green_button_color": "#77DD77",
    "red_button_color": "#FF7276",
    "scroll_trough_color": "#E0E0E0",
    "main_btn_color": "#b2fba5",
    "del_btn_color": "#e99e56"
}

# Simple fonts config - use system fonts
# Simple fonts config that works well on Linux
FONTS = {
    "title": ("Liberation Sans", "Ubuntu", "DejaVu Sans", "Arial"),
    "body": ("Liberation Sans", "Ubuntu", "DejaVu Sans", "Arial"),
    "description": ("Liberation Sans", "Ubuntu", "DejaVu Sans", "Arial")
}

# Use a consistent theme
THEME = 'clam'  # 'clam' works well on most platforms

# Font and padding adjustments for better display
FONT_ADJUSTMENT = 0
PADDING_ADJUSTMENT = 2

# Window sizes - slightly larger for better visibility
WINDOW_SIZE = {
    "main": "650x700",
    "completed": "650x500",
    "small": "300x180",
    "tags": "600x650",
    "analytics": "900x900",
    "archive": "650x600"
}

# In config.py, add a STYLES dictionary
STYLES = {
    # Font definitions
    "fonts": {
        "title": ("Liberation Sans", 16, "bold"),
        "header": ("Liberation Sans", 12, "bold"),
        "normal": ("Liberation Sans", 11),
        "small": ("Liberation Sans", 10)
    },
    
    # Widget style configurations
    "widgets": {
        "background": "#A9A9A9",
        "frame_bg": "#d3d3d3",
        "entry_bg": "#d3d3d3",
        "button_bg": "#b2fba5",
        "delete_button_bg": "#e99e56",
        "input_text_color": "black",
        "label_padding": 5
    }
}