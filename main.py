"""
Main entry point for Augment VIP GUI (MVC Version)
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.application import run_gui_application

if __name__ == "__main__":
    sys.exit(run_gui_application())
