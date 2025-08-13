"""
CLI entry point for backward compatibility
"""

import sys
from pathlib import Path

# Add src directory to Python path  
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import from old augment_vip module for CLI compatibility
try:
    from augment_vip.cli import cli
    cli()
except ImportError:
    print(r"""________      _______        ___    ___  ________       ___      ___           ___      ___  ________      ________          
|\   __  \    |\  ___ \      |\  \  /  /||\   ____\     |\  \    |\  \         |\  \    /  /||\   __  \    |\   __  \         
\ \  \|\  \   \ \   __/|     \ \  \/  / /\ \  \___|_    \ \  \   \ \  \        \ \  \  /  / /\ \  \|\  \   \ \  \|\  \        
 \ \   _  _\   \ \  \_|/__    \ \    / /  \ \_____  \    \ \  \   \ \  \        \ \  \/  / /  \ \   __  \   \ \   __  \       
  \ \  \\  \|   \ \  \_|\ \    \/  /  /    \|____|\  \    \ \  \   \ \  \____    \ \    / /    \ \  \ \  \   \ \  \ \  \  ___ 
   \ \__\\ _\    \ \_______\ __/  / /        ____\_\  \    \ \__\   \ \_______\   \ \__/ /      \ \__\ \__\   \ \__\ \__\|\__\
    \|__|\|__|    \|_______||\___/ /        |\_________\    \|__|    \|_______|    \|__|/        \|__|\|__|    \|__|\|__|\|__|
                            \|___|/         \|_________|""")
    print("CLI module not available. Please use the GUI version:")
    print("python main.py")
    sys.exit(1)
