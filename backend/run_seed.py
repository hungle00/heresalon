#!/usr/bin/env python3
"""
Helper script to run database seeding with proper Flask app context.
"""

import os
import sys

# Set Flask app environment
os.environ['FLASK_APP'] = 'src.entry:flask_app'

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Import and run the seeding script from prepare_data directory
from prepare_data.seed_db import main

if __name__ == "__main__":
    main()
