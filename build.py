import PyInstaller.__main__
import os
import sys
import shutil
import time

# Get the directory where this script is located
app_path = os.path.dirname(os.path.abspath(__file__))
app_icon = os.path.join(app_path, 'app', 'image.png')
dist_dir = os.path.join(app_path, 'dist', 'TimeTracker')
build_dir = os.path.join(app_path, 'build')

# Clean up previous build artifacts with better error handling
def safe_remove_directory(directory):
    if os.path.exists(directory):
        print(f"Attempting to remove directory: {directory}")
        try:
            shutil.rmtree(directory)
            print(f"Successfully removed {directory}")
        except PermissionError:
            print(f"Permission error when removing {directory}. Waiting for resources to be released...")
            # Wait a bit and try again
            time.sleep(3)
            try:
                shutil.rmtree(directory)
                print(f"Successfully removed {directory} after waiting")
            except Exception as e:
                print(f"Could not remove directory after waiting: {e}")
                print("Please close any applications using the files and try again.")
                user_input = input("Continue anyway? (y/n): ")
                if user_input.lower() != 'y':
                    sys.exit(1)

# Clean up previous build artifacts
print("Cleaning up previous build artifacts...")
safe_remove_directory(dist_dir)
safe_remove_directory(build_dir)

# Convert icon to .ico format if it's not already
icon_path = os.path.join(app_path, 'app_icon.ico')
if not os.path.exists(icon_path) and app_icon.lower().endswith('.png'):
    try:
        from PIL import Image
        img = Image.open(app_icon)
        img.save(icon_path, format='ICO')
        print(f"Converted PNG to ICO: {icon_path}")
    except ImportError:
        print("Warning: PIL/Pillow not installed. Using PNG icon instead.")
        icon_path = app_icon
    except Exception as e:
        print(f"Warning: Could not convert icon: {e}")
        icon_path = app_icon
else:
    icon_path = app_icon

# PyInstaller arguments for Windows
args = [
    'app/MainPage.py',  # Your main script
    '--name=TimeTracker',
    '--onedir',  # Create a directory containing the executable
    f'--icon={icon_path}',  # Use your app icon
    '--noconfirm',  # Replace output directory without asking
    '--add-data=app/ui;app/ui',  # Include UI modules
    '--add-data=app/ui/Databases;app/ui/Databases',  # Include database folder
    '--add-data=app/image.png;app/',  # Include the icon
    '--windowed',  # No console window on Windows
    '--clean',  # Clean PyInstaller cache
    
    # Required imports based on your code
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter.font',
    '--hidden-import=sqlite3',
    '--hidden-import=datetime',
    '--hidden-import=pathlib',
    '--hidden-import=csv',
    '--hidden-import=threading',
    '--hidden-import=re',
    '--hidden-import=shutil',
    '--hidden-import=matplotlib',
    '--hidden-import=matplotlib.figure',
    '--hidden-import=matplotlib.backends.backend_tkagg',
    '--hidden-import=typing',
]

# Run PyInstaller
print("Starting PyInstaller build process...")
try:
    PyInstaller.__main__.run(args)
    print("Build completed successfully!")
except Exception as e:
    print(f"Build failed with error: {e}")
    sys.exit(1)