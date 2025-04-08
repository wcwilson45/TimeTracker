import os
import subprocess
import sys
import tempfile
import shutil

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
    
    # Check for Inno Setup
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe"
    ]
    
    for path in inno_paths:
        if os.path.exists(path):
            print(f"✓ Inno Setup found at: {path}")
            return path
    
    print("❌ Inno Setup not found!")
    print("Please download and install Inno Setup from: https://jrsoftware.org/isdl.php")
    print("After installation, run this script again.")
    sys.exit(1)

def main():
    print("=== Building TimeTracker Windows Installer ===")
    
    # Check requirements
    inno_setup_path = check_requirements()
    
    # Build with PyInstaller
    print("\n1. Building executable with PyInstaller...")
    build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py")
    subprocess.check_call([sys.executable, build_script])
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Build installer with Inno Setup
    print("\n2. Creating Windows installer with Inno Setup...")
    iss_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "installer.iss")
    subprocess.check_call([inno_setup_path, iss_script])
    
    installer_path = os.path.join(output_dir, "TimeTracker_Setup.exe")
    if os.path.exists(installer_path):
        print(f"\n✅ Success! Installer created at: {installer_path}")
    else:
        print("\n❌ Error: Installer creation failed")

if __name__ == "__main__":
    main()