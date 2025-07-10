# 🛍️ 1688.com Product Scraper for WooCommerce

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yousefabdallah171/1668_product_scraper)

> **A powerful, intelligent tool to scrape product data from 1688.com and prepare it for WooCommerce import with advanced features and robust error handling.**

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🛠️ Usage Guide](#️-usage-guide)
- [📊 Output Examples](#-output-examples)
- [🔧 Configuration](#-configuration)
- [❓ Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

### 🎯 **Core Features**
- ✅ **Intelligent Product Extraction** - Automatically detects and extracts product names, descriptions, prices, and images
- ✅ **Multi-Selector Support** - Uses multiple CSS selectors to ensure maximum data extraction success
- ✅ **Robust Error Handling** - Continues processing even if some products fail
- ✅ **Automatic Translation** - Translates Chinese content to English for WooCommerce compatibility
- ✅ **Image Optimization** - Filters and validates product images, removes duplicates and non-product images
- ✅ **CSV Export** - Generates WooCommerce-compatible CSV files with proper formatting

### 🔧 **Advanced Features**
- 🔄 **Retry Logic** - Automatically retries failed requests with exponential backoff
- 📝 **Detailed Logging** - Comprehensive logging for debugging and monitoring
- 🎨 **Rich Description Support** - Extracts full HTML descriptions with formatting preserved
- 🖼️ **Image Gallery Support** - Captures all product images, not just the main one
- ⚡ **Performance Optimized** - Efficient processing with configurable delays to avoid rate limiting

### 📊 **Data Extraction Capabilities**
```
Product Information Extracted:
├── Product Name (with fallbacks)
├── Full Description (HTML + Text)
├── Price (with currency detection)
├── Product Images (filtered & validated)
├── Category Information
├── Product Attributes
└── Seller Information
```

---

## 🚀 Quick Start

### **Step 1: Download & Setup**
```bash
# Clone the repository
git clone https://github.com/yousefabdallah171/1668_product_scraper.git
cd 1668_product_scraper

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Prepare Your URLs**
Create a `urls.txt` file with your 1688.com product links:
```txt
https://detail.1688.com/offer/123456789.html
https://detail.1688.com/offer/987654321.html
https://detail.1688.com/offer/456789123.html
```

### **Step 3: Run the Scraper**
```bash
# Windows
python run_scraper.py

# Or double-click
run_scraper.bat
```

### **Step 4: Import to WooCommerce**
1. Go to WooCommerce → Products → Import
2. Upload the generated CSV file
3. Map the fields and import!

---

## 📦 Installation

### **System Requirements**
- ✅ Windows 10/11, macOS, or Linux
- ✅ Python 3.8 or higher
- ✅ Internet connection
- ✅ Google Chrome (for debugging)

### **Detailed Installation Steps**

#### **1. Install Python**
```bash
# Download from python.org
# Make sure to check "Add Python to PATH" during installation

# Verify installation
python --version
# Should show: Python 3.8.x or higher
```

#### **2. Install Dependencies**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

#### **3. Verify Installation**
```bash
# Test the scraper
python run_scraper.py --test
```

---

## 🛠️ Usage Guide

### **Basic Usage**

#### **1. Prepare Your Product URLs**
```txt
# urls.txt - One URL per line
https://detail.1688.com/offer/123456789.html
https://detail.1688.com/offer/987654321.html
```

#### **2. Run the Scraper**
```bash
python run_scraper.py
```

#### **3. Check the Output**
```
📁 Generated Files:
├── woocommerce_import_YYYYMMDD_HHMMSS.csv  # Main CSV file
├── raw_products_YYYYMMDD_HHMMSS.json       # Raw data backup
└── scraper.log                             # Detailed logs
```

### **Advanced Usage**

#### **Custom Configuration**
```python
# Edit woocommerce_1688_scraper.py
# Modify these settings:

DELAY_BETWEEN_REQUESTS = 3  # Seconds between requests
MAX_RETRIES = 3             # Number of retry attempts
TIMEOUT = 30                # Request timeout in seconds
```

#### **Batch Processing**
```bash
# Process multiple URL files
python run_scraper.py --input urls_batch1.txt
python run_scraper.py --input urls_batch2.txt
```

---

## 📊 Output Examples

### **CSV Output Structure**
```csv
Name,Description,Short Description,Regular Price,Images,Categories,Type,SKU
"Product Name","Full description with HTML formatting...","Short description...","29.99","image1.jpg,image2.jpg","Electronics","simple","1688-123456"
```

### **Sample Extracted Data**
```json
{
  "name": "Creative Romantic Starry Sky Light Projection",
  "description": "<p>Beautiful LED projection light with multiple colors...</p>",
  "price": "29.99",
  "images": [
    "https://img.alicdn.com/imgextra/i1/123456.jpg",
    "https://img.alicdn.com/imgextra/i2/123456.jpg"
  ],
  "category": "Home & Garden",
  "attributes": {
    "Color": "Multi-color",
    "Power": "5W",
    "Material": "Plastic"
  }
}
```

### **Visual Output Examples**

#### **Before Processing**
```
🌐 1688.com Product Page
├── Chinese product name
├── Chinese description
├── Chinese price (¥)
└── Multiple images
```

#### **After Processing**
```
📦 WooCommerce Ready
├── English product name
├── English description (HTML formatted)
├── USD price ($)
├── Filtered product images
└── Proper categories
```

---

## 🔧 Configuration

### **Main Configuration Options**

#### **1. Request Settings**
```python
# In woocommerce_1688_scraper.py
DELAY_BETWEEN_REQUESTS = 3    # Seconds between requests
MAX_RETRIES = 3               # Retry attempts for failed requests
TIMEOUT = 30                  # Request timeout
USER_AGENT = "Mozilla/5.0..." # Browser user agent
```

#### **2. Extraction Settings**
```python
# Description extraction selectors
DESCRIPTION_SELECTORS = [
    '#description .html-description',
    '.product-description',
    '.desc-content'
]

# Image filtering
IMAGE_FILTERS = [
    'video', 'logo', 'icon', 'placeholder'
]
```

#### **3. Output Settings**
```python
# CSV export options
CSV_ENCODING = 'utf-8-sig'    # Excel compatibility
BACKUP_FILES = True           # Create backup files
LOG_LEVEL = 'INFO'            # Logging level
```

---

## ❓ Troubleshooting

### **Common Issues & Solutions**

#### **1. "No products were processed successfully"**
**Problem:** All products failed to extract
**Solutions:**
```bash
# Check your URLs are valid
python -c "import requests; print(requests.get('https://detail.1688.com/offer/123456789.html').status_code)"

# Check network connection
ping detail.1688.com

# Try with fewer URLs first
# Edit urls.txt to include only 2-3 URLs
```

#### **2. "Failed to fetch page"**
**Problem:** Network or blocking issues
**Solutions:**
```python
# Increase delays in the script
DELAY_BETWEEN_REQUESTS = 5  # Increase from 3 to 5

# Use different user agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

#### **3. "No description found"**
**Problem:** Description extraction failing
**Solutions:**
```python
# Add more selectors
DESCRIPTION_SELECTORS.extend([
    '.detail-content',
    '[class*="desc"]',
    '.product-details'
])
```

#### **4. "CSV file not generated"**
**Problem:** No successful product processing
**Solutions:**
```bash
# Check logs for errors
cat scraper.log

# Verify URLs are accessible
# Try with a single, known working URL
```

### **Debug Mode**
```bash
# Enable detailed logging
python run_scraper.py --debug

# Check individual product extraction
python -c "
from woocommerce_1688_scraper import extract_product_info
import requests
html = requests.get('YOUR_URL').text
print(extract_product_info(html, 'YOUR_URL'))
"
```

### **Performance Optimization**

#### **For Large Batches**
```python
# Increase delays to avoid rate limiting
DELAY_BETWEEN_REQUESTS = 5
MAX_CONCURRENT_REQUESTS = 1

# Process in smaller batches
# Split urls.txt into files with 10-20 URLs each
```

#### **For Better Success Rate**
```python
# Use more robust user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]
```

---

## 📈 Performance & Statistics

### **Typical Performance Metrics**
```
📊 Performance Statistics:
├── Success Rate: 85-95%
├── Processing Speed: 3-5 seconds per product
├── Image Extraction: 3-15 images per product
├── Description Length: 500-2000 characters
└── CSV Generation: Instant
```

### **Resource Usage**
```
💻 System Requirements:
├── CPU: Minimal (single-threaded)
├── RAM: 50-100MB
├── Storage: 1-10MB per product
└── Network: 1-5MB per product
```

---

## 🔒 Security & Legal

### **Important Disclaimers**
- ⚠️ **Educational Use Only** - This tool is for educational purposes
- ⚠️ **Respect Terms of Service** - Always check website terms before scraping
- ⚠️ **Rate Limiting** - Built-in delays to avoid overwhelming servers
- ⚠️ **No Warranty** - Use at your own risk

### **Best Practices**
```python
# Always use delays between requests
DELAY_BETWEEN_REQUESTS = 3

# Respect robots.txt
# Check website terms of service

# Don't overload servers
# Process in small batches
```

---

## 🤝 Contributing

### **How to Contribute**
1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### **Development Setup**
```bash
# Clone the repository
git clone https://github.com/yousefabdallah171/1668_product_scraper.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

### **Testing**
```bash
# Run tests
python -m pytest tests/

# Test with sample URLs
python run_scraper.py --test
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **MIT License**
```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 Support

### **Getting Help**
- 📧 **Create an Issue** - [GitHub Issues](https://github.com/yousefabdallah171/1668_product_scraper/issues)
- 📖 **Check Documentation** - This README and code comments
- 🔍 **Search Issues** - Look for similar problems

### **Before Asking for Help**
1. ✅ Check this README thoroughly
2. ✅ Review the troubleshooting section
3. ✅ Check existing GitHub issues
4. ✅ Try with a single, known working URL
5. ✅ Include error messages and logs

---

## 🎯 Roadmap

### **Planned Features**
- 🔄 **Multi-threading support** for faster processing
- 🌐 **Proxy support** for better reliability
- 📊 **Web interface** for easier usage
- 🔍 **Advanced filtering** options
- 📱 **Mobile app** companion

### **Recent Updates**
- ✅ **Enhanced description extraction** with multiple selectors
- ✅ **Improved image filtering** and validation
- ✅ **Better error handling** and logging
- ✅ **Robust retry logic** for failed requests
- ✅ **Comprehensive documentation** and examples

---

## 🙏 Acknowledgments

- **BeautifulSoup** - For HTML parsing
- **Requests** - For HTTP requests
- **Cloudscraper** - For bypassing protection
- **Googletrans** - For translation features
- **Pandas** - For CSV handling

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yousefabdallah171/1668_product_scraper)
![GitHub forks](https://img.shields.io/github/forks/yousefabdallah171/1668_product_scraper)
![GitHub issues](https://img.shields.io/github/issues/yousefabdallah171/1668_product_scraper)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yousefabdallah171/1668_product_scraper)

---

**⭐ Star this repository if it helped you!**

**🔄 Fork it if you want to contribute!**

**📧 Report issues if you find bugs!**

---

*Made with ❤️ for the WooCommerce community*
