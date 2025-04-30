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
    
    # Check for dependencies specific to Linux
    missing_deps = []
    
    # Check for tkinter by trying to import it
    try:
        import tkinter
        print("✓ tkinter is installed")
    except ImportError:
        missing_deps.append("python3-tk")
        
    # Check for matplotlib
    try:
        import matplotlib
        print("✓ matplotlib is installed")
    except ImportError:
        missing_deps.append("python3-matplotlib")
    
    # Report missing dependencies if any
    if missing_deps:
        print(f"❌ The following dependencies are missing: {', '.join(missing_deps)}")
        print(f"Please install them using your distribution's package manager:")
        print(f"For Debian/Ubuntu: sudo apt-get install {' '.join(missing_deps)}")
        print(f"For Fedora: sudo dnf install {' '.join(missing_deps)}")
        print(f"For Arch Linux: sudo pacman -S {' '.join(missing_deps)}")
        
        # Ask if user wants to continue anyway
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    return True

def main():
    print("=== Building TimeTracker Linux Package ===")
    
    # Check requirements
    check_requirements()
    
    # Build with PyInstaller
    print("\n1. Building executable with PyInstaller...")
    build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_linux.py")
    subprocess.check_call([sys.executable, build_script])
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy the install script to the dist directory
    print("\n2. Preparing Linux installer...")
    installer_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "install_timetracker.sh")
    
    # Make sure installer script exists
    if not os.path.exists(installer_script):
        print(f"Creating installer script at: {installer_script}")
        with open(installer_script, 'w') as f:
            f.write("""#!/bin/bash
# TimeTracker Linux Installer Script
# This script installs the TimeTracker application into the user's local applications

# Configuration variables
APP_NAME="TimeTracker"
INSTALL_DIR="$HOME/.local/share/TimeTracker"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_PATH="$INSTALL_DIR/app_icon.png"
EXECUTABLE_PATH="$INSTALL_DIR/TimeTracker"
SOURCE_DIR="$(dirname "$(readlink -f "$0")")/dist/TimeTracker"

# Text formatting
bold=$(tput bold)
normal=$(tput sgr0)
green=$(tput setaf 2)
red=$(tput setaf 1)
blue=$(tput setaf 4)

# Print header
echo "${blue}${bold}===== TimeTracker Installation =====${normal}"
echo 

# Function to check dependencies
check_dependencies() {
    echo "${bold}Checking dependencies...${normal}"
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "${red}Error: Python 3 is not installed.${normal}"
        echo "Please install Python 3 using your distribution's package manager."
        exit 1
    fi
    
    # Check if tkinter is installed by attempting to import it
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "${red}Error: tkinter is not installed.${normal}"
        echo "Please install tkinter using your distribution's package manager (usually python3-tk)."
        exit 1
    fi
    
    echo "${green}✓ All dependencies satisfied${normal}"
}

# Function to create installation directory
create_install_dir() {
    echo "${bold}Creating installation directory...${normal}"
    mkdir -p "$INSTALL_DIR"
    
    if [ $? -ne 0 ]; then
        echo "${red}Error: Could not create installation directory.${normal}"
        exit 1
    fi
    
    echo "${green}✓ Installation directory created${normal}"
}

# Function to copy files
copy_files() {
    echo "${bold}Copying application files...${normal}"
    
    # Check if source directory exists
    if [ ! -d "$SOURCE_DIR" ]; then
        echo "${red}Error: Source directory not found: $SOURCE_DIR${normal}"
        echo "Make sure to run build_linux.py before running this installer."
        exit 1
    fi
    
    # Copy all files from the PyInstaller directory
    cp -r "$SOURCE_DIR"/* "$INSTALL_DIR"
    
    if [ $? -ne 0 ]; then
        echo "${red}Error: Failed to copy application files.${normal}"
        exit 1
    fi
    
    # Copy icon separately if it exists at the project root
    if [ -f "app/image.png" ]; then
        cp "app/image.png" "$ICON_PATH"
    fi
    
    echo "${green}✓ Application files copied${normal}"
}

# Function to create desktop file
create_desktop_file() {
    echo "${bold}Creating desktop shortcut...${normal}"
    
    mkdir -p "$DESKTOP_DIR"
    
    # Create .desktop file
    cat > "$DESKTOP_DIR/timetracker.desktop" << EOF
[Desktop Entry]
Type=Application
Name=TimeTracker
Comment=Task management application with time tracking capabilities
Exec="$EXECUTABLE_PATH"
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Office;
EOF
    
    # Make desktop file executable
    chmod +x "$DESKTOP_DIR/timetracker.desktop"
    
    echo "${green}✓ Desktop shortcut created${normal}"
}

# Function to create symlink to executable in PATH
create_symlink() {
    echo "${bold}Creating executable symlink...${normal}"
    
    mkdir -p "$HOME/.local/bin"
    ln -sf "$EXECUTABLE_PATH" "$HOME/.local/bin/timetracker"
    
    # Check if ~/.local/bin is in PATH
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        echo "${blue}Note: You may need to add '$HOME/.local/bin' to your PATH.${normal}"
        echo "Add the following line to your ~/.bashrc or ~/.profile:"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
    
    echo "${green}✓ Executable symlink created${normal}"
}

# Main installation process
check_dependencies
create_install_dir
copy_files
create_desktop_file
create_symlink

echo
echo "${green}${bold}TimeTracker has been successfully installed!${normal}"
echo
echo "You can now launch TimeTracker by:"
echo "1. Clicking on the TimeTracker icon in your applications menu"
echo "2. Running 'timetracker' in the terminal"
echo
echo "Thank you for installing TimeTracker!"
""")
    
    # Make the script executable
    os.chmod(installer_script, 0o755)
    
    # Create tarball with the installer and the PyInstaller output
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
    output_tarball = os.path.join(output_dir, "TimeTracker-Linux-Installer.tar.gz")
    
    print(f"\n3. Creating distribution tarball at: {output_tarball}")
    
    # Create a temporary directory to organize files for the tarball
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy the installer script
        shutil.copy2(installer_script, os.path.join(temp_dir, os.path.basename(installer_script)))
        
        # Create README file
        readme_path = os.path.join(temp_dir, "README.txt")
        with open(readme_path, 'w') as f:
            f.write("""TimeTracker for Linux
===================

Thank you for downloading TimeTracker!

Installation Instructions:
1. Extract this tarball: tar -xzf TimeTracker-Linux-Installer.tar.gz
2. Navigate to the extracted directory: cd TimeTracker-Linux-Installer
3. Run the installer script: ./install_timetracker.sh

Requirements:
- Python 3.6 or later
- Tkinter (python3-tk package)
- Matplotlib

If you encounter any issues during installation, please see the troubleshooting
section at the end of this README or contact support.

Enjoy using TimeTracker!
""")
        
        # Copy the dist directory (PyInstaller output)
        if os.path.exists(dist_dir):
            dist_dest = os.path.join(temp_dir, "dist")
            shutil.copytree(dist_dir, dist_dest)
        else:
            print(f"\n❌ Error: PyInstaller output directory not found: {dist_dir}")
            print("Make sure the build process completed successfully.")
            sys.exit(1)
            
        # Create the tarball
        shutil.make_archive(
            os.path.splitext(output_tarball)[0],  # Remove .gz extension
            'gztar',  # Format
            root_dir=os.path.dirname(temp_dir),
            base_dir=os.path.basename(temp_dir)
        )
        
        # Rename the created tarball if needed
        created_tarball = f"{os.path.splitext(output_tarball)[0]}.tar.gz"
        if created_tarball != output_tarball:
            shutil.move(created_tarball, output_tarball)
    
    if os.path.exists(output_tarball):
        print(f"\n✅ Success! Linux installer package created at: {output_tarball}")
        print("\nTo use the installer package:")
        print("1. Extract it: tar -xzf TimeTracker-Linux-Installer.tar.gz")
        print("2. Run the installer: ./install_timetracker.sh")
    else:
        print("\n❌ Error: Failed to create installer package")

if __name__ == "__main__":
    main()
