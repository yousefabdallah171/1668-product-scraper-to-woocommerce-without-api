#!/usr/bin/env python3
"""
1688 Product Scraper Runner
Developed by Rakmyat (https://rakmyat.com/)
Contact: yoseabdallah866@gmail.com
"""

import sys
import os
import traceback
from datetime import datetime

def print_banner():
    """Print the application banner"""
    print("=" * 80)
    print("1688 PRODUCT SCRAPER FOR WOOCOMMERCE")
    print("=" * 80)
    print("Developed by Rakmyat (https://rakmyat.com/)")
    print("Contact: yoseabdallah866@gmail.com")
    print("=" * 80)
    print()

def check_requirements():
    """Check if all required files exist"""
    print("Checking requirements...")
    
    required_files = [
        'woocommerce_1688_scraper.py',
        'urls.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"ERROR: Missing required files: {', '.join(missing_files)}")
        return False
    
    print("OK: All required files found")
    return True

def main():
    """Main function to run the scraper"""
    try:
        # Print banner
        print_banner()
        
        # Check requirements
        if not check_requirements():
            print("\nERROR: Please ensure all required files are present.")
            return 1
        
        # Import the scraper module
        print("Importing scraper module...")
        try:
            from woocommerce_1688_scraper import run
            print("OK: Scraper module imported successfully")
        except ImportError as e:
            print(f"ERROR: Error importing scraper module: {e}")
            print("Make sure woocommerce_1688_scraper.py is in the src directory")
            return 1
        
        # Check if urls.txt has content
        print("Checking URLs file...")
        try:
            with open('urls.txt', 'r', encoding='utf-8') as f:
                urls = f.read().strip()
            
            if not urls:
                print("ERROR: urls.txt is empty. Please add some URLs.")
                return 1
            
            url_count = len([line for line in urls.split('\n') if line.strip()])
            print(f"OK: Found {url_count} URLs to process")
            
        except Exception as e:
            print(f"ERROR: Error reading urls.txt: {e}")
            return 1
        
        # Run the scraper
        print("\nStarting scraper...")
        print("=" * 50)
        
        start_time = datetime.now()
        result = run()
        end_time = datetime.now()
        
        duration = end_time - start_time
        
        print("=" * 50)
        print(f"Scraping completed in {duration}")
        
        if result == 0:
            print("SUCCESS: Scraping completed successfully!")
            print("Check the output folder for CSV files")
            return 0
        else:
            print("ERROR: Scraping completed with errors")
            return 1
            
    except KeyboardInterrupt:
        print("\nStopping: Scraping interrupted by user")
        return 1
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        print("Full error details:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())