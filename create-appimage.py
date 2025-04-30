import os
import subprocess
import sys
import shutil
import tempfile
import urllib.request

def check_requirements():
    """Check if required tools are installed"""
    # Check for PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
    
    # Check for Pillow (for icon conversion)
    try:
        import PIL
        print("✓ Pillow is installed")
    except ImportError:
        print("Installing Pillow for icon conversion...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("✓ Pillow installed successfully")
    
    # Check for AppImageTool, download if not present
    appimage_tool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "appimagetool-x86_64.AppImage")
    
    if not os.path.exists(appimage_tool_path):
        print("Downloading AppImageTool...")
        urllib.request.urlretrieve(
            "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage",
            appimage_tool_path
        )
        # Make the tool executable
        os.chmod(appimage_tool_path, 0o755)
        print("✓ AppImageTool downloaded successfully")
    else:
        print("✓ AppImageTool is available")
    
    return appimage_tool_path

def build_executable():
    """Build executable with PyInstaller"""
    print("\n1. Building executable with PyInstaller...")
    # Use the existing build_linux.py to build the executable
    build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_linux.py")
    
    if not os.path.exists(build_script):
        # Create the build_linux.py script if it doesn't exist
        print(f"Creating build script at: {build_script}")
        with open(build_script, 'w') as f:
            f.write("""import PyInstaller.__main__
import os
import sys

# Get the directory where this script is located
app_path = os.path.dirname(os.path.abspath(__file__))
app_icon = os.path.join(app_path, 'app', 'image.png')

# Convert icon to .xpm format if needed for Linux
icon_path = os.path.join(app_path, 'app_icon.xpm')
if not os.path.exists(icon_path) and app_icon.lower().endswith('.png'):
    try:
        from PIL import Image
        img = Image.open(app_icon)
        img.save(icon_path, format='XPM')
        print(f"Converted PNG to XPM: {icon_path}")
    except ImportError:
        print("Warning: PIL/Pillow not installed. Using PNG icon instead.")
        icon_path = app_icon
    except Exception as e:
        print(f"Warning: Could not convert icon: {e}")
        icon_path = app_icon
else:
    icon_path = app_icon

# PyInstaller arguments for Linux
args = [
    'app/MainPage.py',  # Your main script
    '--name=TimeTracker',
    '--onedir',  # Create a directory containing the executable
    f'--icon={icon_path}',  # Use your app icon
    '--noconfirm',  # Replace output directory without asking
    '--add-data=app/ui:app/ui',  # Include UI modules - colon separator on Linux
    '--add-data=app/ui/Databases:app/ui/Databases',  # Include database folder
    '--add-data=app/image.png:app/',  # Include the icon
    '--windowed',  # No terminal window on Linux
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
PyInstaller.__main__.run(args)
""")
    
    # Run the build script
    subprocess.check_call([sys.executable, build_script])
    
    # Check if the build was successful
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "TimeTracker")
    if not os.path.exists(dist_dir):
        print("\n❌ Error: PyInstaller build failed. The output directory doesn't exist.")
        sys.exit(1)
    
    return dist_dir

def create_appimage(appimage_tool_path, pyinstaller_dist_dir):
    """Create AppImage from PyInstaller output"""
    print("\n2. Creating AppImage...")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a temporary directory for AppDir structure
    with tempfile.TemporaryDirectory() as temp_dir:
        appdir = os.path.join(temp_dir, "TimeTracker.AppDir")
        os.makedirs(appdir, exist_ok=True)
        
        # Copy PyInstaller output to AppDir/usr
        usr_dir = os.path.join(appdir, "usr")
        bin_dir = os.path.join(usr_dir, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        
        # Copy executable and dependencies
        for item in os.listdir(pyinstaller_dist_dir):
            src = os.path.join(pyinstaller_dist_dir, item)
            dst = os.path.join(bin_dir, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        
        # Make the main executable script executable
        executable_path = os.path.join(bin_dir, "TimeTracker")
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
        
        # Create the AppRun script (entry point for the AppImage)
        apprun_path = os.path.join(appdir, "AppRun")
        with open(apprun_path, 'w') as f:
            f.write("""#!/bin/bash
# Get the directory where this script is located
HERE="$(dirname "$(readlink -f "${0}")")"
# Run the application
exec "${HERE}/usr/bin/TimeTracker" "$@"
""")
        os.chmod(apprun_path, 0o755)
        
        # Copy or create icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "image.png")
        icon_dest = os.path.join(appdir, "timetracker.png")
        if os.path.exists(icon_path):
            shutil.copy2(icon_path, icon_dest)
        else:
            print("Warning: Icon not found at expected location. Using a placeholder icon.")
            # Create a simple placeholder icon
            try:
                from PIL import Image, ImageDraw
                img = Image.new('RGB', (256, 256), color=(73, 109, 137))
                d = ImageDraw.Draw(img)
                d.text((128, 128), "TT", fill=(255, 255, 0))
                img.save(icon_dest)
            except:
                print("Could not create placeholder icon.")
        
        # Create the desktop file
        desktop_path = os.path.join(appdir, "timetracker.desktop")
        with open(desktop_path, 'w') as f:
            f.write("""[Desktop Entry]
Type=Application
Name=TimeTracker
Comment=Task management application with time tracking capabilities
Exec=TimeTracker
Icon=timetracker
Terminal=false
Categories=Utility;Office;
""")
        
        # Run AppImageTool to create the AppImage
        appimage_output = os.path.join(output_dir, "TimeTracker-x86_64.AppImage")
        try:
            # Clean up any existing AppImage
            if os.path.exists(appimage_output):
                os.remove(appimage_output)
                
            # Run the AppImageTool
            subprocess.check_call([appimage_tool_path, appdir, appimage_output])
            print(f"\n✅ Success! AppImage created at: {appimage_output}")
            
            # Make the AppImage executable
            os.chmod(appimage_output, 0o755)
            
            print("\nTo use TimeTracker:")
            print(f"1. Make the AppImage executable: chmod +x {appimage_output}")
            print(f"2. Run it directly: {appimage_output}")
            
            return appimage_output
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error: AppImageTool failed with error code: {e.returncode}")
            print(f"Error details: {e}")
            return None

def main():
    print("=== Building TimeTracker AppImage ===")
    
    # Check requirements and get AppImageTool path
    appimage_tool_path = check_requirements()
    
    # Build the executable
    pyinstaller_dist_dir = build_executable()
    
    # Create the AppImage
    create_appimage(appimage_tool_path, pyinstaller_dist_dir)

if __name__ == "__main__":
    main()
