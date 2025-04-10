import sqlite3
import os
import shutil
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller compatibility) """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_writable_db_path(relative_path):
    """Get a writable path for database files"""
    # For PyInstaller bundles, we need to write to a different location
    if hasattr(sys, '_MEIPASS'):
        # Get user data directory
        if os.name == 'nt':  # Windows
            data_dir = os.path.join(os.environ['APPDATA'], 'TimeTracker')
        
        # Ensure directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Get the filename from the relative path
        filename = os.path.basename(relative_path)
        writable_path = os.path.join(data_dir, filename)
        
        # If the file doesn't exist in the writable location, copy from resources
        if not os.path.exists(writable_path):
            source_path = resource_path(relative_path)
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, writable_path)
                except (IOError, shutil.Error):
                    # Create an empty database file if copy fails
                    conn = sqlite3.connect(writable_path)
                    conn.close()
            else:
                # Create an empty database file
                conn = sqlite3.connect(writable_path)
                conn.close()
        
        return writable_path
    else:
        # In development mode, use the normal path
        return resource_path(relative_path)