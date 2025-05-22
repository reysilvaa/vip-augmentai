#!/usr/bin/env bash
#
# install.sh
#
# Description: Installation script for the Augment VIP project
# This script sets up the necessary dependencies and configurations

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error

# Text formatting
BOLD="\033[1m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RESET="\033[0m"

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${RESET} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $1"
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Check for required system dependencies
check_dependencies() {
    log_info "Checking system dependencies..."
    
    local missing_deps=()
    
    # Check for common dependencies
    for cmd in sqlite3 curl jq; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_warning "Missing dependencies: ${missing_deps[*]}"
        
        # Detect OS for installation instructions
        if [[ "$OSTYPE" == "darwin"* ]]; then
            log_info "To install on macOS, run: brew install ${missing_deps[*]}"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            log_info "To install on Ubuntu/Debian, run: sudo apt install ${missing_deps[*]}"
            log_info "To install on Fedora/RHEL, run: sudo dnf install ${missing_deps[*]}"
        elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
            log_info "To install on Windows, we recommend using Chocolatey: choco install ${missing_deps[*]}"
        fi
        
        read -p "Do you want to continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_error "Installation aborted due to missing dependencies"
            exit 1
        fi
    else
        log_success "All system dependencies are installed"
    fi
}

# Make scripts executable
make_scripts_executable() {
    log_info "Making scripts executable..."
    
    find "$SCRIPT_DIR" -name "*.sh" -type f -exec chmod +x {} \;
    
    log_success "All scripts are now executable"
}

# Setup project configuration
setup_configuration() {
    log_info "Setting up project configuration..."
    
    # Create config directory if it doesn't exist
    mkdir -p "$PROJECT_ROOT/config"
    
    # Create default configuration file if it doesn't exist
    if [ ! -f "$PROJECT_ROOT/config/config.json" ]; then
        cat > "$PROJECT_ROOT/config/config.json" << EOF
{
    "version": "1.0.0",
    "environment": "development",
    "features": {
        "cleanCodeDb": true
    }
}
EOF
        log_success "Created default configuration file"
    else
        log_info "Configuration file already exists, skipping"
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating project directories..."
    
    # Create common directories
    mkdir -p "$PROJECT_ROOT/logs"
    mkdir -p "$PROJECT_ROOT/data"
    mkdir -p "$PROJECT_ROOT/temp"
    
    log_success "Project directories created"
}

# Main installation function
main() {
    log_info "Starting installation process for Augment VIP"
    
    # Check dependencies
    check_dependencies
    
    # Make scripts executable
    make_scripts_executable
    
    # Setup configuration
    setup_configuration
    
    # Create directories
    create_directories
    
    log_success "Installation completed successfully!"
    log_info "You can now use the scripts in the scripts directory"
    log_info "For example, to clean VS Code databases, run: $SCRIPT_DIR/clean_code_db.sh"
}

# Execute main function
main "$@"
