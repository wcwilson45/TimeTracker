#!/bin/bash

# TimeTracker AppImage Installer
# This script is embedded inside the AppImage and will run when the user
# chooses to install the application

# Text formatting
bold=$(tput bold)
normal=$(tput sgr0)
green=$(tput setaf 2)
red=$(tput setaf 1)
blue=$(tput setaf 4)

# Get the directory where this script is located (the mounted AppImage)
HERE="$(dirname "$(readlink -f "${0}")")"

# Configuration
APP_NAME="TimeTracker"
APPIMAGE_PATH="$(readlink -f "${0}")"
DESKTOP_DIR="$HOME/.local/share/applications"
APPLICATIONS_DIR="$HOME/.local/share/applications"
ICONS_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
BIN_DIR="$HOME/.local/bin"

# Print header
echo "${blue}${bold}===== TimeTracker Installation =====${normal}"
echo 

# Ask user if they want to install
echo "This will install TimeTracker to your user applications."
read -p "Would you like to proceed with installation? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 1
fi

# Create directories
echo "${bold}Creating directories...${normal}"
mkdir -p "$APPLICATIONS_DIR"
mkdir -p "$ICONS_DIR"
mkdir -p "$BIN_DIR"

# Copy AppImage to applications directory
echo "${bold}Installing TimeTracker...${normal}"
cp "$APPIMAGE_PATH" "$BIN_DIR/timetracker"
chmod +x "$BIN_DIR/timetracker"

# Extract icon
echo "${bold}Setting up application icon...${normal}"
cp "$HERE/timetracker.png" "$ICONS_DIR/timetracker.png"

# Create desktop file
echo "${bold}Creating desktop shortcut...${normal}"
cat > "$DESKTOP_DIR/timetracker.desktop" << EOF
[Desktop Entry]
Type=Application
Name=TimeTracker
Comment=Task management application with time tracking capabilities
Exec=$BIN_DIR/timetracker
Icon=timetracker
Terminal=false
Categories=Utility;Office;
EOF

# Check if PATH includes ~/.local/bin
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo "${blue}Note: You may need to add '$HOME/.local/bin' to your PATH.${normal}"
    echo "Add the following line to your ~/.bashrc or ~/.profile:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    
    # Ask if user wants to add it now
    read -p "Would you like to add it to your ~/.bashrc now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo "${green}Added to ~/.bashrc. You'll need to restart your terminal or run 'source ~/.bashrc'.${normal}"
    fi
fi

echo
echo "${green}${bold}TimeTracker has been successfully installed!${normal}"
echo
echo "You can now launch TimeTracker by:"
echo "1. Clicking on the TimeTracker icon in your applications menu"
echo "2. Running 'timetracker' in the terminal"
echo
echo "Thank you for installing TimeTracker!"
