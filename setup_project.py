#!/usr/bin/env python
"""
setup_project.py

Creates the necessary directory structure for the Visual Nudges analysis pipeline.
Run this script once after cloning the repository.
"""

from pathlib import Path

def create_directory_structure():
    """Create all necessary directories for the project"""
    
    directories = [
        "data/raw",
        "data/clean",
        "data/features",
        "results/tables",
        "results/models"
    ]
    
    print("Setting up project directory structure...\n")
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep file to preserve empty directories in git
        gitkeep_file = path / ".gitkeep"
        gitkeep_file.touch()
        
        print(f"✓ Created: {directory}/")
    
    print("\n" + "="*50)
    print("Project structure created successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Place your raw data in data/raw/peer_review_raw.xlsx")
    print("2. Run: python 01_data_cleaning.py")
    print("3. Run: python 02_descriptive_statistics.py")
    print("4. Run: python 03_analysis.py")

if __name__ == "__main__":
    create_directory_structure()
