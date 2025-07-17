# 🛍️ 1688 Product Scraper for WooCommerce

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)
![No API](https://img.shields.io/badge/No%20API%20Keys-Required-red.svg)

**Advanced 1688.com Product Scraper with WooCommerce Integration**  
*Developed by [Rakmyat](https://rakmyat.com/) | Contact: yoseabdallah866@gmail.com*

[🚀 Quick Start](#-quick-start) • [📋 Features](#-features) • [🔧 Installation](#-installation) • [📖 Usage](#-usage) • [🛠️ Troubleshooting](#️-troubleshooting)

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [🔧 Installation](#-installation)
- [📖 Usage](#-usage)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📁 File Structure](#-file-structure)
- [🤝 Contributing](#-contributing)
- [📞 Support](#-support)

---

## 🌟 Overview

This is a **professional-grade 1688.com product scraper** that extracts product data and converts it into WooCommerce-ready CSV files. No API keys required - 100% free and open source!

### 🎯 What It Does

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   1688.com      │    │   Scraper       │    │   WooCommerce   │
│   Product Page  │───▶│   Engine        │───▶│   CSV Export    │
│                 │    │                 │    │                 │
│ • Product Name  │    │ • Data Extract  │    │ • Import Ready  │
│ • Images        │    │ • Translation   │    │ • Categories    │
│ • Description   │    │ • Optimization  │    │ • Pricing       │
│ • Pricing       │    │ • Validation    │    │ • Images        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔥 Key Benefits

- ✅ **No API Keys Required** - Works directly with 1688.com
- ✅ **WooCommerce Ready** - Direct CSV import
- ✅ **Multi-language Support** - English & Arabic
- ✅ **Professional GUI** - Easy-to-use interface
- ✅ **Batch Processing** - Multiple URLs at once
- ✅ **Error Handling** - Robust error recovery
- ✅ **Logging System** - Detailed operation logs

---

## 🚀 Quick Start

### Method 1: GUI Launcher (Recommended)
```bash
# Run the main launcher
.\START_HERE.bat

# Or directly launch GUI
python src/professional_gui.py
```

### Method 2: Command Line
```bash
# Run scraper directly
python src/woocommerce_1688_scraper.py

# Or use the runner script
python src/run_scraper.py
```

### Method 3: Smart Launcher
```bash
# Launch the smart launcher
python launcher/Smart\ Launcher.py
```

---

## ✨ Features

### 🎨 Professional GUI Interface
```
┌─────────────────────────────────────────────────────────────┐
│ 🛍️ Professional 1688 Product Scraper - WooCommerce Ready  │
├─────────────────────────────────────────────────────────────┤
│ [🚀 Main Scraper] [⚙️ Settings] [📊 Results] [🔍 Search] │
├─────────────────────────────────────────────────────────────┤
│ 📋 Product URLs Management                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ https://detail.1688.com/offer/123456789.html         │ │
│ │ https://detail.1688.com/offer/987654321.html         │ │
│ └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 🚀 Scraper Controls                                       │
│ [🚀 Start Scraping] [⏹️ Stop] [📁 Open Output] [📊 CSV] │
├─────────────────────────────────────────────────────────────┤
│ 📊 Progress Tracking                                      │
│ ████████████████████████████████████████████████████████ │
│ Progress: 75% | Products: 3 | Success: 2 | Failed: 1     │
├─────────────────────────────────────────────────────────────┤
│ 📋 Scraper Logs                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [12:34:56] 🚀 Starting scraper...                     │ │
│ │ [12:34:58] ✅ Product 1 processed successfully        │ │
│ │ [12:35:01] ✅ Product 2 processed successfully        │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 🔍 Advanced Search Feature
```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 Search Products                                        │
├─────────────────────────────────────────────────────────────┤
│ Search Term: [Creative Phone Holder] [🔍 Search] [Clear] │
├─────────────────────────────────────────────────────────────┤
│ Results (3 found):                                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Product Name    │ Original Link    │ CSV File │ Price │ │
│ │─────────────────│──────────────────│──────────│───────│ │
│ │ Creative Phone  │ 1688.com/offer/ │ output/  │ $17.95│ │
│ │ Holder Pro      │ 123456789.html  │ file.csv │       │ │
│ │                 │                  │          │       │ │
│ │ Phone Stand     │ 1688.com/offer/ │ output/  │ $12.99│ │
│ │ Creative Design │ 987654321.html  │ file.csv │       │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 🌐 Multi-language Support
- 🇺🇸 **English** - Default language
- 🇸🇦 **Arabic** - Full Arabic support
- 🔄 **Auto-translation** - Automatic language detection

### 📊 Data Extraction Capabilities
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 Extracted Data Structure                               │
├─────────────────────────────────────────────────────────────┤
│ Product Information:                                      │
│ ├─ Name: "Creative Phone Holder Pro"                     │
│ ├─ SKU: "CPH-001"                                        │
│ ├─ Price: $17.95                                         │
│ ├─ Description: "High-quality phone holder..."            │
│ ├─ Images: 5 product images                              │
│ ├─ Categories: "Phone Accessories"                        │
│ └─ Original URL: 1688.com/offer/123456789.html          │
│                                                           │
│ WooCommerce Export:                                       │
│ ├─ CSV Format: WooCommerce Import Ready                  │
│ ├─ Images: Optimized for web                             │
│ ├─ Categories: Properly formatted                        │
│ ├─ Pricing: Regular and sale prices                      │
│ └─ SEO: Meta descriptions included                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Installation

### 📋 Prerequisites
```
┌─────────────────────────────────────────────────────────────┐
│ 📋 System Requirements                                    │
├─────────────────────────────────────────────────────────────┤
│ ✅ Python 3.7 or higher                                  │
│ ✅ Windows 10/11 (or Linux/Mac)                          │
│ ✅ Internet connection                                    │
│ ✅ 4GB RAM minimum                                       │
│ ✅ 500MB free disk space                                 │
└─────────────────────────────────────────────────────────────┘
```

### 🚀 Installation Steps

#### Step 1: Download & Extract
```bash
# Clone or download the repository
git clone https://github.com/your-repo/1688-product-scraper.git
cd 1688-product-scraper-to-woocommerce-without-api
```

#### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r src/requirements.txt

# Or let the system check install them automatically
.\START_HERE.bat
```

#### Step 3: Verify Installation
```bash
# Run system check
python src/system_check.py

# Expected output:
# ✅ Python version: 3.11.8
# ✅ requests: Available
# ✅ beautifulsoup4: Available
# ✅ lxml: Available
# ✅ pandas: Available
# ✅ tkinter: Available
```

### 📦 Dependencies
```
┌─────────────────────────────────────────────────────────────┐
│ 📦 Required Python Packages                               │
├─────────────────────────────────────────────────────────────┤
│ requests          │ HTTP requests library                 │
│ beautifulsoup4    │ HTML parsing and scraping            │
│ lxml              │ XML/HTML parser                      │
│ pandas            │ Data manipulation and CSV export      │
│ translators       │ Language translation service          │
│ cloudscraper      │ Anti-bot detection bypass            │
│ Pillow            │ Image processing                     │
│ tkinter           │ GUI framework (built-in)             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Usage

### 🎯 Getting Started

#### 1. Prepare Your URLs
```bash
# Edit urls.txt with your 1688.com product URLs
notepad urls.txt

# Example content:
https://detail.1688.com/offer/667101935579.html
https://detail.1688.com/offer/123456789.html
https://detail.1688.com/offer/987654321.html
```

#### 2. Launch the Application
```bash
# Method 1: Main launcher (recommended)
.\START_HERE.bat

# Method 2: Direct GUI
python src/professional_gui.py

# Method 3: Smart launcher
python launcher/Smart\ Launcher.py
```

#### 3. Configure Settings
```
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ Settings Configuration                                 │
├─────────────────────────────────────────────────────────────┤
│ 📁 File Settings:                                         │
│ ├─ Input File: urls.txt                                  │
│ ├─ Output Folder: output/                                │
│ └─ Language: English                                     │
│                                                           │
│ 🚀 Scraping Settings:                                    │
│ ├─ Scraping Delay: 2 seconds                            │
│ ├─ URL Limit: No limit                                  │
│ ├─ Auto Translate: Enabled                               │
│ └─ Image Optimization: Enabled                           │
│                                                           │
│ 📤 Output Settings:                                      │
│ ├─ Timestamp Folders: Enabled                            │
│ ├─ Backup Files: Enabled                                 │
│ ├─ CSV Prefix: woocommerce_import                        │
│ └─ Save Errors: Enabled                                  │
└─────────────────────────────────────────────────────────────┘
```

#### 4. Start Scraping
```
┌─────────────────────────────────────────────────────────────┐
│ 🚀 Scraping Process                                      │
├─────────────────────────────────────────────────────────────┤
│ 1. Add URLs to the text area                             │
│ 2. Click "🚀 Start Scraping"                             │
│ 3. Monitor progress in real-time                         │
│ 4. Check output folder for results                       │
│ 5. Import CSV to WooCommerce                             │
└─────────────────────────────────────────────────────────────┘
```

### 🔍 Using the Search Feature

#### 1. Open Search Tab
- Click on the "🔍 Search" tab in the GUI

#### 2. Enter Search Term
- Type any product name, description, or keyword
- Click "🔍 Search" button

#### 3. View Results
- Results show across all CSV files
- Click on any result to open the original 1688.com link
- Use "Copy Link" to copy URLs to clipboard

### 📊 Understanding Output Files

#### CSV Files
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 WooCommerce CSV Structure                              │
├─────────────────────────────────────────────────────────────┤
│ Column Name        │ Description                          │
│────────────────────│──────────────────────────────────────│
│ Name              │ Product name                          │
│ Type              │ Product type (simple/variable)        │
│ Published         │ Published status (1/0)               │
│ Featured          │ Featured status (1/0)                │
│ Catalog visibility│ Visibility (visible/hidden)          │
│ Short description │ Short product description             │
│ Description       │ Full product description              │
│ Date sale price   │ Sale price start date                │
│ Date sale price   │ Sale price end date                  │
│ Tax status        │ Tax status (taxable/none)            │
│ Tax class         │ Tax class                            │
│ In stock?         │ Stock status (1/0)                   │
│ Stock             │ Stock quantity                        │
│ Weight (kg)       │ Product weight                        │
│ Length (cm)       │ Product length                        │
│ Width (cm)        │ Product width                         │
│ Height (cm)       │ Product height                        │
│ Allow customer    │ Allow customer reviews (1/0)          │
│ reviews?          │                                      │
│ Purchase note     │ Purchase note                         │
│ Sale price        │ Sale price                            │
│ Regular price     │ Regular price                         │
│ Categories        │ Product categories                    │
│ Tags              │ Product tags                          │
│ Shipping class    │ Shipping class                        │
│ Images            │ Product images (comma-separated)      │
│ Download limit    │ Download limit                        │
│ Download expiry   │ Download expiry days                  │
│ Parent            │ Parent product ID                     │
│ Grouped products  │ Grouped product IDs                   │
│ Upsells           │ Upsell product IDs                    │
│ Cross-sells       │ Cross-sell product IDs                │
│ External URL      │ External product URL                  │
│ Button text       │ Button text                           │
│ Position          │ Menu order                            │
│ Attribute 1 name  │ Custom attribute name                 │
│ Attribute 1 value │ Custom attribute value                │
│ Attribute 1       │ Custom attribute visibility           │
│ visible           │                                      │
│ Attribute 1       │ Custom attribute global               │
│ global            │                                      │
└─────────────────────────────────────────────────────────────┘
```

#### Log Files
```
┌─────────────────────────────────────────────────────────────┐
│ 📋 Log File Structure                                     │
├─────────────────────────────────────────────────────────────┤
│ File: logs/woocommerce_scraper.log                       │
│                                                           │
│ Format: [YYYY-MM-DD HH:MM:SS] [LEVEL] Message           │
│                                                           │
│ Example entries:                                          │
│ [2025-07-13 12:34:56] [INFO] Starting scraper...        │
│ [2025-07-13 12:34:58] [INFO] Found 3 URLs to process    │
│ [2025-07-13 12:35:01] [INFO] Product 1 processed        │
│ [2025-07-13 12:35:05] [ERROR] Failed to fetch URL       │
│ [2025-07-13 12:35:10] [INFO] Scraping completed         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture

### 🔧 System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│ 🏗️ System Architecture                                   │
├─────────────────────────────────────────────────────────────┤
│                                                           │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│ │   GUI       │    │   Scraper   │    │   Output    │    │
│ │   Layer     │───▶│   Engine    │───▶│   Layer     │    │
│ │             │    │             │    │             │    │
│ │ • Tkinter   │    │ • Requests  │    │ • CSV Files │    │
│ │ • Threading │    │ • Beautiful │    │ • Log Files │    │
│ │ • Queue     │    │   Soup      │    │ • Images    │    │
│ │ • Settings  │    │ • Cloud     │    │ • JSON      │    │
│ │             │    │   Scraper   │    │             │    │
│ └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                   │                   │          │
│        ▼                   ▼                   ▼          │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│ │   Config    │    │   Data      │    │   Export    │    │
│ │   Layer     │    │   Process   │    │   Layer     │    │
│ │             │    │             │    │             │    │
│ │ • Settings  │    │ • Extract   │    │ • WooCommerce│   │
│ │ • Language  │    │ • Translate │    │ • CSV Format│   │
│ │ • URLs      │    │ • Validate  │    │ • Images    │   │
│ │ • Logging   │    │ • Optimize  │    │ • Backup    │   │
│ └─────────────┘    └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Data Flow
```
┌─────────────────────────────────────────────────────────────┐
│ 🔄 Data Processing Flow                                   │
├─────────────────────────────────────────────────────────────┤
│                                                           │
│ 1. URL Input ──▶ 2. Web Scraping ──▶ 3. Data Extraction │
│    │                    │                    │            │
│    ▼                    ▼                    ▼            │
│ 8. Results ◀── 7. CSV Export ◀── 6. Translation ◀── 5.  │
│    │                    │                    │            │
│    ▼                    ▼                    ▼            │
│ 9. Logging ◀── 4. Validation ◀── 4. Image Processing    │
│                                                           │
│ Detailed Steps:                                           │
│ ├─ 1. URL Input: Read from urls.txt or GUI               │
│ ├─ 2. Web Scraping: Fetch HTML with anti-bot bypass      │
│ ├─ 3. Data Extraction: Parse HTML for product data       │
│ ├─ 4. Validation: Check data completeness                │
│ ├─ 5. Image Processing: Download and optimize images     │
│ ├─ 6. Translation: Translate to target language          │
│ ├─ 7. CSV Export: Format for WooCommerce import          │
│ ├─ 8. Results: Save to output folder                     │
│ └─ 9. Logging: Record all operations                     │
└─────────────────────────────────────────────────────────────┘
```

### 🛡️ Error Handling
```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ Error Handling Strategy                               │
├─────────────────────────────────────────────────────────────┤
│                                                           │
│ ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│ │   Error     │    │   Recovery  │    │   Logging   │    │
│ │   Detection │───▶│   Strategy  │───▶│   System    │    │
│ │             │    │             │    │             │    │
│ │ • Network   │    │ • Retry     │    │ • File      │    │
│ │ • Parsing   │    │ • Skip      │    │ • Console   │    │
│ │ • Timeout   │    │ • Fallback  │    │ • GUI       │    │
│ │ • Validation│    │ • Continue  │    │ • Email     │    │
│ └─────────────┘    └─────────────┘    └─────────────┘    │
│                                                           │
│ Error Types Handled:                                     │
│ ├─ Network Errors: Connection timeout, DNS failure       │
│ ├─ Parsing Errors: Invalid HTML, missing data           │
│ ├─ Validation Errors: Incomplete product information     │
│ ├─ Translation Errors: API failure, language issues      │
│ ├─ Export Errors: File permission, disk space           │
│ └─ System Errors: Memory, CPU, file system              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Troubleshooting

### 🔍 Common Issues & Solutions

#### 1. ❌ "Module not found" Error
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Solution: Missing Dependencies                         │
├─────────────────────────────────────────────────────────────┤
│ Error: ModuleNotFoundError: No module named 'requests'   │
│                                                           │
│ Solution:                                                 │
│ 1. Run: pip install -r src/requirements.txt             │
│ 2. Or: .\START_HERE.bat (auto-installs)                 │
│ 3. Or: python -m pip install requests beautifulsoup4    │
└─────────────────────────────────────────────────────────────┘
```

#### 2. ❌ "No URLs found" Error
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Solution: Empty URLs File                             │
├─────────────────────────────────────────────────────────────┤
│ Error: No URLs found in urls.txt                         │
│                                                           │
│ Solution:                                                 │
│ 1. Edit urls.txt file                                    │
│ 2. Add 1688.com product URLs (one per line)             │
│ 3. Example:                                              │
│    https://detail.1688.com/offer/123456789.html         │
│    https://detail.1688.com/offer/987654321.html         │
└─────────────────────────────────────────────────────────────┘
```

#### 3. ❌ "Connection timeout" Error
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Solution: Network Issues                              │
├─────────────────────────────────────────────────────────────┤
│ Error: Connection timeout or network error                │
│                                                           │
│ Solutions:                                                │
│ 1. Check internet connection                             │
│ 2. Try different URLs                                    │
│ 3. Increase scraping delay (Settings → Delay: 5 seconds)│
│ 4. Use VPN if blocked                                    │
│ 5. Check firewall settings                               │
└─────────────────────────────────────────────────────────────┘
```

#### 4. ❌ "Anti-bot detection" Error
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Solution: Anti-Bot Protection                         │
├─────────────────────────────────────────────────────────────┤
│ Error: 403 Forbidden or anti-bot detection               │
│                                                           │
│ Solutions:                                                │
│ 1. Increase delay between requests (5-10 seconds)        │
│ 2. Use fewer URLs per session                            │
│ 3. Try different time of day                             │
│ 4. Check if IP is blocked                                │
│ 5. Use proxy if necessary                                │
└─────────────────────────────────────────────────────────────┘
```

#### 5. ❌ "GUI not opening" Error
```
┌─────────────────────────────────────────────────────────────┐
│ 🔧 Solution: GUI Issues                                  │
├─────────────────────────────────────────────────────────────┤
│ Error: Tkinter not available or GUI crashes              │
│                                                           │
│ Solutions:                                                │
│ 1. Install tkinter: pip install tk                       │
│ 2. Use command line: python src/woocommerce_1688_scraper.py│
│ 3. Check Python installation                             │
│ 4. Try different Python version                          │
│ 5. Run as administrator                                  │
└─────────────────────────────────────────────────────────────┘
```

### 🔧 Debug Mode

#### Enable Debug Logging
```bash
# Edit settings.json
{
  "debug_mode": true,
  "log_level": "DEBUG",
  "save_debug_logs": true
}
```

#### Check Log Files
```bash
# View latest logs
type logs\woocommerce_scraper.log

# Or open log folder
explorer logs\
```

#### System Check
```bash
# Run comprehensive system check
python src/system_check.py

# Expected output:
# ✅ Python version: 3.11.8
# ✅ All dependencies available
# ✅ All files found
# ✅ All directories created
```

### 🚨 Emergency Recovery

#### Reset All Settings
```bash
# Delete settings files
del settings.json
del src\settings.json

# Restart application
.\START_HERE.bat
```

#### Clear All Data
```bash
# Remove all output files
rmdir /s /q output
rmdir /s /q logs

# Restart application
.\START_HERE.bat
```

---

## 📁 File Structure

```
┌─────────────────────────────────────────────────────────────┐
│ 📁 Project Structure                                      │
├─────────────────────────────────────────────────────────────┤
│ 1688-product-scraper-to-woocommerce-without-api/         │
│ ├── 📄 README.md                    # This file           │
│ ├── 📄 urls.txt                     # Product URLs        │
│ ├── 📄 START_HERE.bat               # Main launcher       │
│ ├── 📄 START_HERE.py                # Python launcher     │
│ ├── 📄 .gitignore                   # Git ignore rules    │
│ │                                                         │
│ ├── 📁 src/                        # Source code          │
│ │   ├── 📄 professional_gui.py      # Main GUI            │
│ │   ├── 📄 woocommerce_1688_scraper.py # Core scraper    │
│ │   ├── 📄 run_scraper.py          # CLI runner          │
│ │   ├── 📄 system_check.py         # System validator    │
│ │   ├── 📄 requirements.txt         # Dependencies        │
│ │   ├── 📄 settings.json           # App settings        │
│ │   ├── 📄 lang.json               # Language files      │
│ │   └── 📄 urls.txt                # URL backup          │
│ │                                                         │
│ ├── 📁 launcher/                   # Launcher scripts     │
│ │   ├── 📄 Smart Launcher.py       # Smart launcher      │
│ │   ├── 📄 script check .bat       # System check        │
│ │   ├── 📄 Run Scraper.bat         # Direct scraper      │
│ │   └── 📄 launcher_config.json    # Launcher config     │
│ │                                                         │
│ ├── 📁 output/                     # Generated files      │
│ │   ├── 📄 woocommerce_import_*.csv # WooCommerce CSV    │
│ │   ├── 📄 raw_products.json       # Raw data backup     │
│ │   └── 📄 page_content_*.html     # Debug HTML files    │
│ │                                                         │
│ ├── 📁 logs/                       # Log files           │
│ │   ├── 📄 woocommerce_scraper.log # Main log file       │
│ │   └── 📄 scraper_logs_*.txt      # GUI logs            │
│ │                                                         │
│ └── 📁 .git/                       # Git repository       │
│     ├── 📄 config                   # Git config          │
│     ├── 📄 HEAD                     # Git HEAD            │
│     └── 📁 objects/                 # Git objects         │
└─────────────────────────────────────────────────────────────┘
```

### 📊 File Descriptions

#### Core Files
- **`professional_gui.py`** - Main GUI application with all features
- **`woocommerce_1688_scraper.py`** - Core scraping engine
- **`run_scraper.py`** - Command-line interface
- **`system_check.py`** - System validation and dependency check

#### Configuration Files
- **`settings.json`** - Application settings and preferences
- **`lang.json`** - Multi-language support files
- **`requirements.txt`** - Python package dependencies
- **`urls.txt`** - Product URLs to scrape

#### Output Files
- **`woocommerce_import_*.csv`** - WooCommerce-ready CSV files
- **`raw_products.json`** - Raw scraped data backup
- **`woocommerce_scraper.log`** - Detailed operation logs

#### Launcher Files
- **`START_HERE.bat`** - Windows batch launcher
- **`Smart Launcher.py`** - Advanced launcher with system check
- **`script check .bat`** - System validation script

---

## 🤝 Contributing

### 🛠️ Development Setup
```bash
# Clone repository
git clone https://github.com/your-repo/1688-product-scraper.git

# Install development dependencies
pip install -r src/requirements.txt

# Run tests
python src/system_check.py
```

### 📝 Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### 🐛 Bug Reports
When reporting bugs, please include:
- Python version
- Operating system
- Error message
- Steps to reproduce
- Log files (if available)

### 💡 Feature Requests
For new features, please describe:
- Use case
- Expected behavior
- Implementation suggestions

---

## 📞 Support

### 🆘 Getting Help

#### 📧 Email Support
- **Email**: yoseabdallah866@gmail.com
- **Response Time**: 24-48 hours
- **Include**: Error logs, system info, steps to reproduce

#### 🌐 Website
- **Website**: https://rakmyat.com/
- **Documentation**: Full guides and tutorials
- **Updates**: Latest version information

#### 💬 Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share solutions
- **Wiki**: Community-maintained documentation

### 🔧 Professional Support

#### 🏢 Enterprise Support
- **Custom Development**: Tailored solutions
- **Integration**: WooCommerce, Shopify, other platforms
- **Training**: Team training and workshops
- **Maintenance**: Ongoing support and updates

#### 📊 Consulting Services
- **E-commerce Strategy**: Product sourcing optimization
- **Automation**: Workflow automation
- **Performance**: Speed and efficiency optimization
- **Security**: Anti-detection and protection

### 📚 Resources

#### 📖 Documentation
- **User Guide**: Complete usage instructions
- **API Reference**: Technical documentation
- **Examples**: Sample configurations
- **Tutorials**: Step-by-step guides

#### 🎥 Video Tutorials
- **Installation**: Setup and configuration
- **Usage**: Basic and advanced features
- **Troubleshooting**: Common issues and solutions
- **Integration**: WooCommerce import process

#### 📋 Templates
- **URL Lists**: Sample product URLs
- **Settings**: Optimized configurations
- **CSV Templates**: Custom import formats
- **Log Formats**: Structured logging templates

---

## 📄 License

```
┌─────────────────────────────────────────────────────────────┐
│ 📄 MIT License                                            │
├─────────────────────────────────────────────────────────────┤
│                                                           │
│ Copyright (c) 2025 Rakmyat                               │
│                                                           │
│ Permission is hereby granted, free of charge, to any     │
│ person obtaining a copy of this software and associated   │
│ documentation files (the "Software"), to deal in the     │
│ Software without restriction, including without limitation │
│ the rights to use, copy, modify, merge, publish,         │
│ distribute, sublicense, and/or sell copies of the        │
│ Software, and to permit persons to whom the Software is  │
│ furnished to do so, subject to the following conditions: │
│                                                           │
│ The above copyright notice and this permission notice     │
│ shall be included in all copies or substantial portions   │
│ of the Software.                                          │
│                                                           │
│ THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF     │
│ ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED  │
│ TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A       │
│ PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT       │
│ SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR     │
│ ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN     │
│ ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,     │
│ OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE     │
│ OR OTHER DEALINGS IN THE SOFTWARE.                       │
└─────────────────────────────────────────────────────────────┘
```

---

<div align="center">

**Made with ❤️ by [Rakmyat](https://rakmyat.com/)**

[🏠 Home](https://rakmyat.com/) • [📧 Contact](mailto:yoseabdallah866@gmail.com) • [🐛 Issues](https://github.com/your-repo/issues) • [⭐ Star](https://github.com/your-repo)

</div>
