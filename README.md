# 🛍️ Professional 1688 Product Scraper for WooCommerce

A powerful, feature-rich desktop application that scrapes product data from 1688.com and exports it into WooCommerce-compatible CSV files. **100% FREE** - No API keys, subscriptions, or payments required.

---

## 🚨 Recent Updates & Bug Fixes
- **Critical IndentationError fixed** in core scraper logic
- **Full code health check**: syntax, logic, and runtime issues addressed
- **Professional GUI only**: Basic GUI removed for a streamlined experience
- **Actively maintained**: Please report any issues or feature requests on [GitHub](https://github.com/yousefabdallah171/1668-product-scraper-to-woocommerce-without-api)

---

## ✨ Features

### 🎛️ Advanced Settings Panel
- **File Management**: Select input file, choose output folder
- **Language Options**: Output language (Arabic/English), translation language selection
- **Scraping Controls**: Enable/disable automatic translation, image optimization
- **Performance Settings**: Control scraping speed/delay, limit number of URLs
- **Output Organization**: Timestamped folders, backup files, custom CSV prefixes

### 🖥️ Professional Scraper Controls
- **Start/Stop Buttons**: Safe scraper termination
- **Real-time Monitoring**: Live progress tracking and status updates
- **Output Management**: Open output folder, CSV files, log folders
- **Help System**: Comprehensive instructions and troubleshooting

### 🔗 Advanced URL Management
- **URL Editor**: Paste/edit URLs in text area
- **File Operations**: Load/save URLs from/to files
- **Validation**: URL validation and error checking
- **Sample Data**: Add test URLs for quick setup

### 📊 Progress Tracking & Analytics
- **Progress Bar**: Real-time percentage completion
- **Statistics**: Scraped vs. total URLs counter
- **Live Updates**: Current product being processed
- **Performance Metrics**: Success/failure rates

### 🧾 Live Results Preview
- **CSV Preview**: Display scraped results in read-only table
- **Excel Integration**: Open CSV files directly in Excel
- **Image Preview**: Live product image thumbnails
- **Data Export**: Multiple output formats

### 🌐 Multi-language Support
- **English Interface**: Full English GUI
- **Arabic Interface**: Complete Arabic translation
- **Dynamic Language Switching**: Change interface language on-the-fly
- **Localized Messages**: All user messages translated

### 📤 Advanced Output Features
- **WooCommerce Ready**: Perfect CSV format for WooCommerce import
- **Multiple Formats**: CSV, JSON backup, detailed logs
- **Organized Output**: Timestamped folders, backup files
- **Error Handling**: Comprehensive error logging and recovery

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Professional GUI
```bash
python professional_gui.py
```

### Command Line Usage
```bash
python run_scraper.py
```

---

## 📋 Usage Instructions

### 1. Setting Up URLs
1. Open the Professional GUI
2. Go to the "Main Scraper" tab
3. Add 1688.com product URLs (one per line)
4. Use "Validate URLs" to check for errors
5. Save URLs to file for future use

### 2. Configuring Settings
1. Go to the "Settings" tab
2. **File Settings**: Choose input file and output folder
3. **Translation Settings**: Select output and translation languages
4. **Scraping Settings**: Set delay and URL limits
5. **Output Settings**: Configure file organization
6. **Advanced Settings**: Error handling and update options
7. Click "Save Settings"

### 3. Running the Scraper
1. Go to "Main Scraper" tab
2. Click "Start Scraping"
3. Monitor progress in real-time
4. View logs for detailed information
5. Check "Results Preview" tab for output

### 4. Managing Results
1. **CSV Preview**: View scraped data in table format
2. **Image Preview**: Browse product images
3. **Export Options**: Open in Excel, access output folders
4. **Backup Files**: JSON backups for data recovery

---

## 🛠️ Advanced Features

### Multi-language Interface
- Switch between English and Arabic
- All interface elements translated
- Dynamic language loading from `lang.json`

### Progress Tracking
- Real-time progress bar
- Current product display
- Success/failure statistics
- Detailed logging system

### Error Handling
- Comprehensive error logging
- Automatic retry for failed URLs
- User-friendly error messages
- Detailed error reports

### Output Organization
```
output/
├── 2025-07-10_15-00/
│   ├── woocommerce_import_20250710_150000.csv
│   ├── backup_woocommerce_import_20250710_150000.json
│   └── scraper_logs_20250710_150000.txt
└── logs/
    ├── scraper_20250710_150000.log
    └── errors_20250710_150000.log
```

---

## 📁 File Structure

```
1668_product_scraper/
├── professional_gui.py          # Professional GUI application
├── woocommerce_1688_scraper.py # Core scraping logic
├── run_scraper.py              # Command line runner
├── lang.json                   # Multi-language translations
├── settings.json               # User settings (auto-generated)
├── urls.txt                    # Input URLs file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── output/                     # Generated CSV files
├── logs/                       # Log files
└── temp_downloads/             # Temporary files
```

---

## 🔧 Configuration

### Settings File (`settings.json`)
```json
{
  "input_file": "urls.txt",
  "output_folder": "output",
  "output_language": "English",
  "translation_language": "English",
  "auto_translate": true,
  "image_optimization": true,
  "scraping_delay": 2,
  "url_limit": 0,
  "timestamp_folders": true,
  "backup_files": true,
  "csv_prefix": "woocommerce_import",
  "save_errors": true,
  "retry_failed": true,
  "check_updates": true
}
```

### Language File (`lang.json`)
- English and Arabic translations
- Dynamic interface language switching
- Extensible for additional languages

---

## 📊 Output Format

### WooCommerce CSV Structure
```csv
Name,Description,Short Description,SKU,Price,Categories,Images,URL,Stock Status,Type,Status
Product Name,Full description...,Short desc...,SKU123,29.99,Category1,image1.jpg,url,instock,simple,publish
```

### Generated Files
- **CSV Files**: WooCommerce import ready
- **JSON Backups**: Raw data backup
- **Log Files**: Detailed operation logs
- **Error Logs**: Error tracking and debugging

---

## 🚨 Troubleshooting

### Common Issues

**1. Unicode Encoding Errors**
- Fixed in latest version
- Use `professional_gui.py` for best compatibility

**2. Scraper Not Starting**
- Check if URLs are valid 1688.com links
- Ensure all dependencies are installed
- Check log files for detailed errors

**3. No Images Extracted**
- Images are automatically filtered for quality
- Check network connection
- Verify URL accessibility

**4. Translation Issues**
- Disable auto-translation in settings
- Check internet connection for translation service
- Use manual language selection

### Error Logs
- Check `logs/errors_*.log` for detailed error information
- Review `logs/scraper_*.log` for operation details
- Use GUI log viewer for real-time monitoring

---

## 🔄 Updates

### Version History
- **v2.0**: Professional GUI with advanced features
- **v1.5**: Enhanced scraper with better error handling
- **v1.0**: Basic GUI and core functionality

### Update Checking
- Automatic update notifications
- Manual update checking in settings
- GitHub repository integration

---

## 📞 Support

### Contact Information
- **Developer**: Rakmyat (https://rakmyat.com/)
- **Email**: yoseabdallah866@gmail.com
- **GitHub**: https://github.com/yousefabdallah171/1668-product-scraper-to-woocommerce-without-api

### Getting Help
1. Check the Help tab in the GUI
2. Review error logs for specific issues
3. Contact developer with detailed error information
4. Check GitHub issues for known problems
