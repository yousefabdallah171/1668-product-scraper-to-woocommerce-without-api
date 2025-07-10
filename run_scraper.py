#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main runner for the improved 1688.com scraper
"""
import os
import sys

def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("IMPROVED 1688 SCRAPER FOR WOOCOMMERCE")
    print("=" * 80)
    
    # Check for URLs file
    if not os.path.exists('urls.txt'):
        print("\n❌ Error: urls.txt not found")
        print("Please create urls.txt with one URL per line")
        print("\nExample urls.txt content:")
        print("https://detail.1688.com/offer/667101935579.html")
        print("https://detail.1688.com/offer/614189122649.html")
        sys.exit(1)
    
    print(f"✅ Found urls.txt")
    
    # Import and run the improved scraper
    try:
        from woocommerce_1688_scraper import run
        print("🚀 Starting scraper...")
        result = run()
        
        if result == 0:
            print("\n✅ Scraping completed successfully!")
            print("Check the generated CSV file for WooCommerce import.")
        else:
            print("\n❌ Scraping failed. Check the log file for details.")
            
        return result
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure the woocommerce_1688_scraper.py file is in the same directory")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())