#!/usr/bin/env python3
"""
Professional 1688 Product Scraper GUI
Enhanced version with advanced features
Developed by Rakmyat (https://rakmyat.com/)
Contact: yoseabdallah866@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import os
import sys
import time
import json
import csv
import shutil
from datetime import datetime
import queue
import webbrowser
from pathlib import Path
import requests
from PIL import Image, ImageTk
import io
import urllib.request

class ProfessionalScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional 1688 Product Scraper - WooCommerce Ready")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize variables
        self.is_running = False
        self.log_queue = queue.Queue()
        self.current_language = "English"
        self.settings = self.load_settings()
        self.scraped_products = []
        self.current_product_index = 0
        self.scraping_delay = int(self.settings.get('scraping_delay', 2))
        
        # Load translations
        with open('lang.json', 'r', encoding='utf-8') as f:
            self.translations = json.load(f)
        
        # Store widget references for translation
        self.translatable_widgets = {}
        
        # Create main container with notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_tab()
        self.create_settings_tab()
        self.create_preview_tab()
        self.create_help_tab()
        
        # Set up styling
        self.setup_styling()
        
        # Load existing URLs and settings
        self.load_urls()
        
        # Start log monitoring
        self.monitor_logs()
        
        # Check for updates
        self.check_for_updates()
        
        # Initialize language system
        self.initialize_language_system()
        
        # Update language after everything is set up
        self.update_language()

    def setup_styling(self):
        """Setup modern styling for the GUI"""
        style = ttk.Style()
        
        # Configure styles
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Info.TLabel', font=('Segoe UI', 9))
        style.configure('Success.TLabel', font=('Segoe UI', 9), foreground='green')
        style.configure('Error.TLabel', font=('Segoe UI', 9), foreground='red')
        style.configure('Warning.TLabel', font=('Segoe UI', 9), foreground='orange')
        
        # Configure button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Segoe UI', 9))
        style.configure('Danger.TButton', font=('Segoe UI', 9), foreground='red')

    def create_main_tab(self):
        """Create the main scraping tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="🚀 Main Scraper")
        
        # Create header
        self.create_header(main_frame)
        
        # Create URL management section
        self.create_url_section(main_frame)
        
        # Create scraper controls
        self.create_scraper_controls(main_frame)
        
        # Create progress section
        self.create_progress_section(main_frame)
        
        # Create log section
        self.create_log_section(main_frame)
        
        # Create status section
        self.create_status_section(main_frame)

    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Create settings sections
        self.create_file_settings(settings_frame)
        self.create_translation_settings(settings_frame)
        self.create_scraping_settings(settings_frame)
        self.create_output_settings(settings_frame)
        self.create_advanced_settings(settings_frame)

    def create_preview_tab(self):
        """Create the preview tab"""
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="📊 Results Preview")
        
        # Create preview sections
        self.create_csv_preview(preview_frame)
        self.create_image_preview(preview_frame)

    def create_help_tab(self):
        """Create the help tab"""
        help_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_frame, text="❓ Help")
        
        self.create_help_content(help_frame)

    def create_header(self, parent):
        """Create the header section"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame, text="🛍️ Professional 1688 Product Scraper", style='Title.TLabel')
        title_label.pack()
        self.translatable_widgets['title'] = title_label
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Advanced WooCommerce Integration - No API Keys Required", style='Info.TLabel')
        subtitle_label.pack(pady=(5, 0))
        self.translatable_widgets['subtitle'] = subtitle_label
        
        # Developer info
        dev_label = ttk.Label(header_frame, text="Developed by Rakmyat (https://rakmyat.com/) | Contact: yoseabdallah866@gmail.com", style='Info.TLabel')
        dev_label.pack(pady=(5, 0))
        self.translatable_widgets['developer'] = dev_label

    def create_url_section(self, parent):
        """Create the URL management section"""
        url_frame = ttk.LabelFrame(parent, text="📋 Product URLs Management", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        self.translatable_widgets['urls_management'] = url_frame
        
        # URL text area
        self.url_text = scrolledtext.ScrolledText(url_frame, height=8, width=80, font=('Consolas', 9))
        self.url_text.pack(fill=tk.X, pady=(0, 10))
        
        # URL control buttons
        button_frame = ttk.Frame(url_frame)
        button_frame.pack(fill=tk.X)
        
        load_btn = ttk.Button(button_frame, text="📁 Load URLs", command=self.load_urls, style='Secondary.TButton')
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['load_urls'] = load_btn
        
        save_btn = ttk.Button(button_frame, text="💾 Save URLs", command=self.save_urls, style='Secondary.TButton')
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['save_urls'] = save_btn
        
        clear_btn = ttk.Button(button_frame, text="🧹 Clear All", command=self.clear_urls, style='Secondary.TButton')
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['clear_all'] = clear_btn
        
        sample_btn = ttk.Button(button_frame, text="📝 Add Sample", command=self.add_sample_urls, style='Secondary.TButton')
        sample_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['add_sample'] = sample_btn
        
        validate_btn = ttk.Button(button_frame, text="🔍 Validate URLs", command=self.validate_urls, style='Secondary.TButton')
        validate_btn.pack(side=tk.LEFT)
        self.translatable_widgets['validate_urls'] = validate_btn

    def create_scraper_controls(self, parent):
        """Create the scraper controls section"""
        control_frame = ttk.LabelFrame(parent, text="🚀 Scraper Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        self.translatable_widgets['scraper_controls'] = control_frame
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start/Stop buttons
        self.run_button = ttk.Button(button_frame, text="🚀 Start Scraping", 
                                    command=self.run_scraper, style='Primary.TButton')
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['start_scraping'] = self.run_button
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop Scraping", 
                                     command=self.stop_scraper, style='Danger.TButton', state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['stop_scraping'] = self.stop_button
        
        # Output buttons
        output_btn = ttk.Button(button_frame, text="📁 Open Output", 
                               command=self.open_output_folder, style='Secondary.TButton')
        output_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['open_output'] = output_btn
        
        csv_btn = ttk.Button(button_frame, text="📊 Open CSV", 
                            command=self.open_csv_file, style='Secondary.TButton')
        csv_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['open_csv'] = csv_btn
        
        help_btn = ttk.Button(button_frame, 
            text="❓ Help", 
            command=lambda: self.notebook.select(3), 
            style='Secondary.TButton'
        )
        help_btn.pack(side=tk.LEFT)
        self.translatable_widgets['help'] = help_btn
        
        # Test button for dropdown
        test_btn = ttk.Button(button_frame, 
            text="🧪 Test Dropdown", 
            command=self.test_dropdown, 
            style='Secondary.TButton'
        )
        test_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Language selector - improved implementation
        ttk.Label(button_frame, text="Language:", style='Info.TLabel').pack(side=tk.LEFT, padx=(20, 5))
        self.language_var = tk.StringVar(value=self.current_language)
        
        # Get available languages from translations and ensure they're properly formatted
        available_languages = list(self.translations.keys())
        self.log_message(f"Available languages: {available_languages}")
        
        # Create combobox with better configuration
        self.language_combo = ttk.Combobox(
            button_frame, 
            textvariable=self.language_var,
            values=available_languages, 
            state="readonly", 
            width=12,
            height=len(available_languages)
        )
        self.language_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bind multiple events to ensure the dropdown works
        self.language_combo.bind('<<ComboboxSelected>>', self.change_language)
        self.language_combo.bind('<Button-1>', self.on_language_click)
        self.language_combo.bind('<Key>', self.on_language_key)
        
        # Set initial value
        if available_languages:
            self.language_combo.set(available_languages[0])
            self.current_language = available_languages[0]

    def create_progress_section(self, parent):
        """Create the progress tracking section"""
        progress_frame = ttk.LabelFrame(parent, text="📊 Progress Tracking", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        self.translatable_widgets['progress_tracking'] = progress_frame
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Progress text
        self.progress_text = ttk.Label(progress_frame, text="Ready to scrape", style='Info.TLabel')
        self.progress_text.pack(side=tk.LEFT)
        self.translatable_widgets['ready'] = self.progress_text
        
        # Progress percentage
        self.progress_percent = ttk.Label(progress_frame, text="0%", style='Info.TLabel')
        self.progress_percent.pack(side=tk.RIGHT)
        
        # Current product
        current_frame = ttk.Frame(progress_frame)
        current_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(current_frame, text="Current Product:", style='Info.TLabel').pack(side=tk.LEFT)
        self.current_product_label = ttk.Label(current_frame, text="None", style='Info.TLabel')
        self.current_product_label.pack(side=tk.LEFT, padx=(5, 0))
        self.translatable_widgets['current_product'] = self.current_product_label

    def create_log_section(self, parent):
        """Create the log section"""
        log_frame = ttk.LabelFrame(parent, text="📋 Scraper Logs", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.translatable_widgets['scraper_logs'] = log_frame
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Log control buttons
        log_button_frame = ttk.Frame(log_frame)
        log_button_frame.pack(fill=tk.X)
        
        clear_log_btn = ttk.Button(log_button_frame, text="🧹 Clear Logs", command=self.clear_logs, style='Secondary.TButton')
        clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['clear_logs'] = clear_log_btn
        
        save_log_btn = ttk.Button(log_button_frame, text="💾 Save Logs", command=self.save_logs, style='Secondary.TButton')
        save_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.translatable_widgets['save_logs'] = save_log_btn
        
        open_log_btn = ttk.Button(log_button_frame, text="📁 Open Log Folder", command=self.open_log_folder, style='Secondary.TButton')
        open_log_btn.pack(side=tk.LEFT)
        self.translatable_widgets['open_log_folder'] = open_log_btn

    def create_status_section(self, parent):
        """Create the status section"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="✅ Ready", style='Success.TLabel')
        self.status_label.pack(side=tk.LEFT)
        self.translatable_widgets['ready'] = self.status_label
        
        # Statistics
        self.stats_label = ttk.Label(status_frame, text="Products: 0 | Success: 0 | Failed: 0", style='Info.TLabel')
        self.stats_label.pack(side=tk.RIGHT)

    def create_file_settings(self, parent):
        """Create file settings section"""
        file_frame = ttk.LabelFrame(parent, text="📁 File Settings", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input file selection
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(input_frame, text="Input File:", style='Info.TLabel').pack(side=tk.LEFT)
        self.input_file_var = tk.StringVar(value=self.settings.get('input_file', 'urls.txt'))
        input_entry = ttk.Entry(input_frame, textvariable=self.input_file_var, width=30)
        input_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(input_frame, text="Browse", command=self.browse_input_file, style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Output folder selection
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(output_frame, text="Output Folder:", style='Info.TLabel').pack(side=tk.LEFT)
        self.output_folder_var = tk.StringVar(value=self.settings.get('output_folder', 'output'))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_folder_var, width=30)
        output_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(output_frame, text="Browse", command=self.browse_output_folder, style='Secondary.TButton').pack(side=tk.LEFT)

    def create_translation_settings(self, parent):
        """Create translation settings section"""
        trans_frame = ttk.LabelFrame(parent, text="🌐 Translation Settings", padding="10")
        trans_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output language
        output_lang_frame = ttk.Frame(trans_frame)
        output_lang_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(output_lang_frame, text="Output Language:", style='Info.TLabel').pack(side=tk.LEFT)
        self.output_lang_var = tk.StringVar(value=self.settings.get('output_language', 'English'))
        
        # Get available languages
        available_languages = list(self.translations.keys())
        self.output_lang_combo = ttk.Combobox(
            output_lang_frame, 
            textvariable=self.output_lang_var, 
            values=available_languages, 
            state="readonly",
            width=15,
            height=len(available_languages)
        )
        self.output_lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Translation language
        trans_lang_frame = ttk.Frame(trans_frame)
        trans_lang_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(trans_lang_frame, text="Translation Language:", style='Info.TLabel').pack(side=tk.LEFT)
        self.trans_lang_var = tk.StringVar(value=self.settings.get('translation_language', 'English'))
        self.trans_lang_combo = ttk.Combobox(
            trans_lang_frame, 
            textvariable=self.trans_lang_var, 
            values=available_languages, 
            state="readonly",
            width=15,
            height=len(available_languages)
        )
        self.trans_lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Translation options
        options_frame = ttk.Frame(trans_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.auto_translate_var = tk.BooleanVar(value=self.settings.get('auto_translate', True))
        ttk.Checkbutton(options_frame, text="Enable Automatic Translation", variable=self.auto_translate_var).pack(side=tk.LEFT)
        
        self.image_optimization_var = tk.BooleanVar(value=self.settings.get('image_optimization', True))
        ttk.Checkbutton(options_frame, text="Enable Image Optimization", variable=self.image_optimization_var).pack(side=tk.LEFT, padx=(20, 0))

    def create_scraping_settings(self, parent):
        """Create scraping settings section"""
        scraping_frame = ttk.LabelFrame(parent, text="⚡ Scraping Settings", padding="10")
        scraping_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Scraping speed
        speed_frame = ttk.Frame(scraping_frame)
        speed_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(speed_frame, text="Scraping Delay (seconds):", style='Info.TLabel').pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value=str(self.settings.get('scraping_delay', 2)))
        delay_entry = ttk.Entry(speed_frame, textvariable=self.delay_var, width=10)
        delay_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # URL limit
        limit_frame = ttk.Frame(scraping_frame)
        limit_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(limit_frame, text="Max URLs to Scrape:", style='Info.TLabel').pack(side=tk.LEFT)
        self.url_limit_var = tk.StringVar(value=str(self.settings.get('url_limit', 0)))
        limit_entry = ttk.Entry(limit_frame, textvariable=self.url_limit_var, width=10)
        limit_entry.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Label(limit_frame, text="(0 = no limit)", style='Info.TLabel').pack(side=tk.LEFT, padx=(5, 0))

    def create_output_settings(self, parent):
        """Create output settings section"""
        output_frame = ttk.LabelFrame(parent, text="📤 Output Settings", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output organization
        org_frame = ttk.Frame(output_frame)
        org_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.timestamp_folders_var = tk.BooleanVar(value=self.settings.get('timestamp_folders', True))
        ttk.Checkbutton(org_frame, text="Create Timestamped Folders", variable=self.timestamp_folders_var).pack(side=tk.LEFT)
        
        self.backup_files_var = tk.BooleanVar(value=self.settings.get('backup_files', True))
        ttk.Checkbutton(org_frame, text="Create Backup Files", variable=self.backup_files_var).pack(side=tk.LEFT, padx=(20, 0))
        
        # File naming
        naming_frame = ttk.Frame(output_frame)
        naming_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(naming_frame, text="CSV Filename Prefix:", style='Info.TLabel').pack(side=tk.LEFT)
        self.csv_prefix_var = tk.StringVar(value=self.settings.get('csv_prefix', 'woocommerce_import'))
        prefix_entry = ttk.Entry(naming_frame, textvariable=self.csv_prefix_var, width=20)
        prefix_entry.pack(side=tk.LEFT, padx=(10, 0))

    def create_advanced_settings(self, parent):
        """Create advanced settings section"""
        advanced_frame = ttk.LabelFrame(parent, text="🔧 Advanced Settings", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Error handling
        error_frame = ttk.Frame(advanced_frame)
        error_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.save_errors_var = tk.BooleanVar(value=self.settings.get('save_errors', True))
        ttk.Checkbutton(error_frame, text="Save Error Logs", variable=self.save_errors_var).pack(side=tk.LEFT)
        
        self.retry_failed_var = tk.BooleanVar(value=self.settings.get('retry_failed', True))
        ttk.Checkbutton(error_frame, text="Retry Failed URLs", variable=self.retry_failed_var).pack(side=tk.LEFT, padx=(20, 0))
        
        # Update checking
        update_frame = ttk.Frame(advanced_frame)
        update_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.check_updates_var = tk.BooleanVar(value=self.settings.get('check_updates', True))
        ttk.Checkbutton(update_frame, text="Check for Updates", variable=self.check_updates_var).pack(side=tk.LEFT)
        
        # Save settings button
        ttk.Button(advanced_frame, text="💾 Save Settings", command=self.save_settings, style='Primary.TButton').pack(pady=(10, 0))

    def create_csv_preview(self, parent):
        """Create CSV preview section"""
        preview_frame = ttk.LabelFrame(parent, text="📊 CSV Results Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Preview controls
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🔄 Refresh Preview", command=self.refresh_csv_preview, style='Secondary.TButton').pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="📊 Open in Excel", command=self.open_csv_file, style='Secondary.TButton').pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(controls_frame, text="📁 Open Output Folder", command=self.open_output_folder, style='Secondary.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        # CSV preview treeview
        columns = ('Name', 'SKU', 'Price', 'Categories', 'Images')
        self.csv_tree = ttk.Treeview(preview_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.csv_tree.heading(col, text=col)
            self.csv_tree.column(col, width=150)
        
        # Add scrollbars
        csv_scrollbar_y = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.csv_tree.yview)
        csv_scrollbar_x = ttk.Scrollbar(preview_frame, orient=tk.HORIZONTAL, command=self.csv_tree.xview)
        self.csv_tree.configure(yscrollcommand=csv_scrollbar_y.set, xscrollcommand=csv_scrollbar_x.set)
        
        # Pack treeview and scrollbars
        self.csv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        csv_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        csv_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    def create_image_preview(self, parent):
        """Create image preview section"""
        image_frame = ttk.LabelFrame(parent, text="🖼️ Product Image Preview", padding="10")
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # Image preview controls
        img_controls_frame = ttk.Frame(image_frame)
        img_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(img_controls_frame, text="⬅️ Previous", command=self.previous_image, style='Secondary.TButton').pack(side=tk.LEFT)
        ttk.Button(img_controls_frame, text="➡️ Next", command=self.next_image, style='Secondary.TButton').pack(side=tk.LEFT, padx=(10, 0))
        
        self.image_index_label = ttk.Label(img_controls_frame, text="Image 0 of 0", style='Info.TLabel')
        self.image_index_label.pack(side=tk.RIGHT)
        
        # Image display
        self.image_label = ttk.Label(image_frame, text="No images available")
        self.image_label.pack(expand=True)

    def create_help_content(self, parent):
        """Create help content"""
        help_text = """
🛍️ Professional 1688 Product Scraper - Help

📋 Getting Started:
1. Add 1688.com product URLs (one per line) in the URL section
2. Configure settings in the Settings tab
3. Click "Start Scraping" to begin
4. Monitor progress in the logs and progress bar
5. View results in the Preview tab

📁 Output Files:
- woocommerce_import_*.csv (for WooCommerce import)
- raw_products_*.json (raw data backup)
- scraper.log (detailed logs)
- errors.log (error logs)

🔧 Features:
- No API keys required
- Automatic translation
- Image extraction and optimization
- WooCommerce ready output
- Progress tracking
- Live preview
- Multi-language support

⚙️ Settings:
- File Settings: Configure input/output files
- Translation Settings: Language options
- Scraping Settings: Speed and limits
- Output Settings: File organization
- Advanced Settings: Error handling

📊 Preview:
- View scraped results in table format
- Preview product images
- Open CSV files in Excel
- Access output folders

❓ Support:
- Email: yoseabdallah866@gmail.com
- Website: https://rakmyat.com/
- GitHub: https://github.com/yousefabdallah171/1668-product-scraper-to-woocommerce-without-api

🔄 Updates:
- Automatic update checking
- Manual update option available
        """
        
        help_text_widget = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=('Segoe UI', 10))
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)

    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.log_message(f"Error loading settings: {e}")
        
        # Default settings
        return {
            'input_file': 'urls.txt',
            'output_folder': 'output',
            'output_language': 'English',
            'translation_language': 'English',
            'auto_translate': True,
            'image_optimization': True,
            'scraping_delay': 2,
            'url_limit': 0,
            'timestamp_folders': True,
            'backup_files': True,
            'csv_prefix': 'woocommerce_import',
            'save_errors': True,
            'retry_failed': True,
            'check_updates': True
        }

    def save_settings(self):
        """Save settings to file"""
        try:
            settings = {
                'input_file': self.input_file_var.get(),
                'output_folder': self.output_folder_var.get(),
                'output_language': self.output_lang_var.get(),
                'translation_language': self.trans_lang_var.get(),
                'auto_translate': self.auto_translate_var.get(),
                'image_optimization': self.image_optimization_var.get(),
                'scraping_delay': int(self.delay_var.get()),
                'url_limit': int(self.url_limit_var.get()),
                'timestamp_folders': self.timestamp_folders_var.get(),
                'backup_files': self.backup_files_var.get(),
                'csv_prefix': self.csv_prefix_var.get(),
                'save_errors': self.save_errors_var.get(),
                'retry_failed': self.retry_failed_var.get(),
                'check_updates': self.check_updates_var.get()
            }
            
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            
            self.settings = settings
            self.log_message("✅ Settings saved successfully")
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def browse_input_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)

    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_var.set(folder)

    def change_language(self, event=None):
        """Change GUI language"""
        try:
            new_language = self.language_var.get()
            if new_language in self.translations:
                self.current_language = new_language
                self.log_message(f"Language changed to: {self.current_language}")
                self.update_language()
            else:
                self.log_message(f"Warning: Language '{new_language}' not found in translations")
        except Exception as e:
            self.log_message(f"Error changing language: {e}")

    def on_language_click(self, event):
        """Handle combobox click event"""
        try:
            self.log_message(f"Language dropdown clicked, current value: {self.language_var.get()}")
            # Force the dropdown to open
            self.language_combo.event_generate('<Down>')
        except Exception as e:
            self.log_message(f"Error in language click: {e}")

    def on_language_key(self, event):
        """Handle combobox key event"""
        try:
            if event.keysym == 'Return' or event.keysym == 'KP_Enter':
                self.language_combo.event_generate('<<ComboboxSelected>>')
            elif event.keysym == 'Down':
                self.language_combo.event_generate('<Down>')
        except Exception as e:
            self.log_message(f"Error in language key event: {e}")

    def test_dropdown(self):
        """Test method to verify dropdown functionality"""
        try:
            available_languages = list(self.translations.keys())
            self.log_message(f"Testing dropdown with languages: {available_languages}")
            
            # Test if combobox has values
            if hasattr(self, 'language_combo'):
                current_values = self.language_combo['values']
                self.log_message(f"Combobox values: {current_values}")
                
                # Test if Arabic is in the list
                if 'Arabic' in current_values:
                    self.log_message("✅ Arabic found in dropdown")
                else:
                    self.log_message("❌ Arabic not found in dropdown")
                    
                # Test if dropdown can be opened
                self.language_combo.focus_set()
                self.language_combo.event_generate('<Down>')
                self.log_message("✅ Dropdown test completed")
            else:
                self.log_message("❌ Language combobox not found")
                
        except Exception as e:
            self.log_message(f"❌ Dropdown test error: {e}")

    def validate_urls(self):
        """Validate URLs in the text area"""
        urls = self.url_text.get(1.0, tk.END).strip().split('\n')
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            url = url.strip()
            if url and '1688.com' in url:
                valid_urls.append(url)
            elif url:
                invalid_urls.append(url)
        
        self.log_message(f"✅ Valid URLs: {len(valid_urls)}")
        if invalid_urls:
            self.log_message(f"⚠️ Invalid URLs: {len(invalid_urls)}")
            for url in invalid_urls[:5]:  # Show first 5 invalid URLs
                self.log_message(f"   Invalid: {url}")

    def refresh_csv_preview(self):
        """Refresh CSV preview"""
        try:
            # Clear existing items
            for item in self.csv_tree.get_children():
                self.csv_tree.delete(item)
            
            # Find latest CSV file
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'woocommerce' in f]
            if not csv_files:
                self.log_message("No CSV files found")
                return
            
            latest_csv = max(csv_files, key=os.path.getctime)
            
            # Read CSV and populate treeview
            with open(latest_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.csv_tree.insert('', tk.END, values=(
                        row.get('Name', '')[:50] + '...' if len(row.get('Name', '')) > 50 else row.get('Name', ''),
                        row.get('SKU', ''),
                        row.get('Price', ''),
                        row.get('Categories', '')[:30] + '...' if len(row.get('Categories', '')) > 30 else row.get('Categories', ''),
                        f"{len(row.get('Images', '').split(','))} images" if row.get('Images') else '0 images'
                    ))
            
            self.log_message(f"✅ CSV preview refreshed: {len(self.csv_tree.get_children())} products")
            
        except Exception as e:
            self.log_message(f"❌ Error refreshing CSV preview: {e}")

    def open_csv_file(self):
        """Open CSV file in default application"""
        try:
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'woocommerce' in f]
            if not csv_files:
                messagebox.showinfo("Info", "No CSV files found. Run the scraper first.")
                return
            
            latest_csv = max(csv_files, key=os.path.getctime)
            os.startfile(latest_csv)
            self.log_message(f"✅ Opened CSV file: {latest_csv}")
            
        except Exception as e:
            self.log_message(f"❌ Error opening CSV file: {e}")

    def open_log_folder(self):
        """Open log folder"""
        try:
            if os.path.exists('logs'):
                os.startfile('logs')
            else:
                os.makedirs('logs', exist_ok=True)
                os.startfile('logs')
            self.log_message("✅ Opened log folder")
        except Exception as e:
            self.log_message(f"❌ Error opening log folder: {e}")

    def previous_image(self):
        """Show previous image"""
        if self.scraped_products and self.current_product_index > 0:
            self.current_product_index -= 1
            self.update_image_preview()

    def next_image(self):
        """Show next image"""
        if self.scraped_products and self.current_product_index < len(self.scraped_products) - 1:
            self.current_product_index += 1
            self.update_image_preview()

    def update_image_preview(self):
        """Update image preview"""
        if not self.scraped_products:
            self.image_label.config(text="No images available")
            self.image_index_label.config(text="Image 0 of 0")
            return
        
        product = self.scraped_products[self.current_product_index]
        self.image_index_label.config(text=f"Image {self.current_product_index + 1} of {len(self.scraped_products)}")
        
        # Update current product label
        self.current_product_label.config(text=product.get('name', 'Unknown Product'))
        
        # Try to load and display image
        try:
            image_url = product.get('image_url')
            if image_url:
                # Download and display image
                response = urllib.request.urlopen(image_url)
                image_data = response.read()
                image = Image.open(io.BytesIO(image_data))
                
                # Resize image for display
                image.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(image)
                
                self.image_label.config(image=photo)
                self.image_label.image = photo  # Keep a reference
            else:
                self.image_label.config(text="No image available")
        except Exception as e:
            self.image_label.config(text=f"Error loading image: {e}")

    def check_for_updates(self):
        """Check for updates"""
        if not self.settings.get('check_updates', True):
            return
        
        try:
            # This would check against the actual GitHub repo
            # For now, just log that update checking is enabled
            self.log_message("✅ Update checking enabled")
        except Exception as e:
            self.log_message(f"⚠️ Update check failed: {e}")

    # Inherit existing methods from the original GUI
    def load_urls(self):
        """Load URLs from file"""
        try:
            filename = self.input_file_var.get()
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    urls = f.read()
                self.url_text.delete(1.0, tk.END)
                self.url_text.insert(1.0, urls)
                self.log_message(f"✅ URLs loaded from {filename}")
            else:
                self.log_message(f"⚠️ {filename} not found. You can add URLs manually.")
        except Exception as e:
            self.log_message(f"❌ Error loading URLs: {str(e)}")

    def save_urls(self):
        """Save URLs to file"""
        try:
            urls = self.url_text.get(1.0, tk.END).strip()
            filename = self.input_file_var.get()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(urls)
            self.log_message(f"✅ URLs saved to {filename}")
        except Exception as e:
            self.log_message(f"❌ Error saving URLs: {str(e)}")

    def clear_urls(self):
        """Clear all URLs from the text area"""
        self.url_text.delete(1.0, tk.END)
        self.log_message("🧹 URLs cleared")

    def add_sample_urls(self):
        """Add sample URLs for testing"""
        sample_urls = """https://detail.1688.com/offer/667101935579.html
https://detail.1688.com/offer/123456789.html
https://detail.1688.com/offer/987654321.html"""
        
        self.url_text.delete(1.0, tk.END)
        self.url_text.insert(1.0, sample_urls)
        self.log_message("📝 Sample URLs added")

    def run_scraper(self):
        """Run the scraper in a separate thread"""
        if self.is_running:
            return
        
        urls = self.url_text.get(1.0, tk.END).strip()
        if not urls:
            messagebox.showwarning("Warning", "Please add some URLs before running the scraper.")
            return
        
        # Save URLs first
        self.save_urls()
        
        # Create output directory if needed
        output_dir = self.output_folder_var.get()
        if self.timestamp_folders_var.get():
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_dir = os.path.join(output_dir, timestamp)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Get scraping delay from GUI
        try:
            self.scraping_delay = int(self.delay_var.get())
        except Exception:
            self.scraping_delay = 2
        
        # Start scraping in a separate thread
        self.is_running = True
        self.run_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="🔄 Scraping in progress...")
        
        # Reset progress
        self.progress_var.set(0)
        self.progress_text.config(text="Starting scraper...")
        self.progress_percent.config(text="0%")
        
        # Start the scraper thread and pass the delay
        threading.Thread(target=self._run_scraper_thread, args=(self.scraping_delay,), daemon=True).start()

    def _run_scraper_thread(self, scraping_delay=2):
        """Run the scraper in a separate thread"""
        try:
            self.log_message("🚀 Starting Professional 1688 Product Scraper...")
            self.log_message("📋 URLs loaded and saved")
            
            # In _run_scraper_thread, call the main scraping logic with scraping_delay=self.scraping_delay
            # Example if using subprocess:
            # subprocess.run([sys.executable, 'woocommerce_1688_scraper.py', '--scraping_delay', str(scraping_delay)])
            # Or if using import:
            # from woocommerce_1688_scraper import main
            # main(scraping_delay=scraping_delay)
            
            # Run the scraper
            process = subprocess.Popen(
                [sys.executable, 'woocommerce_1688_scraper.py', '--scraping_delay', str(scraping_delay)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor the process output
            for line in iter(process.stdout.readline, ''):
                if not self.is_running:  # Check if user stopped the process
                    process.terminate()
                    break
                self.log_queue.put(line.strip())
            
            process.wait()
            
            if self.is_running:  # Only show completion if not stopped
                self.log_queue.put("✅ Scraping completed successfully!")
                self.log_queue.put("📁 Check the output folder for CSV files")
                
        except Exception as e:
            self.log_queue.put(f"❌ Error running scraper: {str(e)}")
        finally:
            # Update GUI in main thread
            self.root.after(0, self._scraping_finished)

    def stop_scraper(self):
        """Stop the running scraper"""
        self.is_running = False
        self.log_message("⏹️ Stopping scraper...")
        self.status_label.config(text="⏹️ Stopping...")

    def _scraping_finished(self):
        """Called when scraping is finished"""
        self.is_running = False
        self.run_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="✅ Ready", style='Success.TLabel')
        
        # Refresh preview
        self.refresh_csv_preview()

    def open_output_folder(self):
        """Open the output folder"""
        try:
            output_dir = self.output_folder_var.get()
            if os.path.exists(output_dir):
                os.startfile(output_dir)
            else:
                messagebox.showinfo("Info", "Output folder not found. Run the scraper first to generate files.")
        except Exception as e:
            self.log_message(f"❌ Error opening output folder: {str(e)}")

    def log_message(self, message):
        """Add a message to the log queue"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def monitor_logs(self):
        """Monitor the log queue and update the GUI"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule the next check
        self.root.after(100, self.monitor_logs)

    def clear_logs(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🧹 Logs cleared")

    def save_logs(self):
        """Save logs to a file"""
        try:
            logs = self.log_text.get(1.0, tk.END)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraper_logs_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(logs)
            
            self.log_message(f"💾 Logs saved to {filename}")
        except Exception as e:
            self.log_message(f"❌ Error saving logs: {str(e)}")

    def update_language(self):
        """Comprehensive language update for all GUI elements"""
        try:
            lang = self.current_language
            if lang not in self.translations:
                self.log_message(f"Warning: Language '{lang}' not available, using English")
                lang = "English"
                self.current_language = "English"
                if hasattr(self, 'language_var'):
                    self.language_var.set("English")
            
            t = self.translations[lang]
            
            # Update tab titles
            try:
                self.notebook.tab(0, text="🚀 Main Scraper")
                self.notebook.tab(1, text="⚙️ Settings")
                self.notebook.tab(2, text="📊 Results Preview")
                self.notebook.tab(3, text="❓ Help")
            except Exception as e:
                print(f"Error updating tab titles: {e}")
            
            # Update all stored widget references
            for widget_name, widget in self.translatable_widgets.items():
                if widget_name in t:
                    try:
                        if isinstance(widget, ttk.Button):
                            widget.config(text=t[widget_name])
                        elif isinstance(widget, ttk.Label):
                            widget.config(text=t[widget_name])
                        elif isinstance(widget, ttk.LabelFrame):
                            widget.config(text=t[widget_name])
                        elif isinstance(widget, tk.Label):
                            widget.config(text=t[widget_name])
                    except Exception as e:
                        print(f"Error updating widget {widget_name}: {e}")
            
            # Update specific widgets that might not be in the stored references
            try:
                if hasattr(self, 'run_button'):
                    self.run_button.config(text=t['start_scraping'])
                if hasattr(self, 'stop_button'):
                    self.stop_button.config(text=t['stop_scraping'])
                if hasattr(self, 'status_label'):
                    current_status = self.status_label.cget('text')
                    if 'Ready' in current_status:
                        self.status_label.config(text=t['ready'])
                    elif 'Scraping' in current_status:
                        self.status_label.config(text=t['scraping_progress'])
                    elif 'Stopping' in current_status:
                        self.status_label.config(text=t['stopping'])
            except Exception as e:
                print(f"Error updating specific widgets: {e}")
            
            # Right-to-left support for Arabic
            if lang == 'Arabic':
                self.root.tk.call('tk', 'scaling', 1.2)
                self.root.option_add('*font', 'Segoe UI 11')
                self.root.option_add('*justify', 'right')
                # Set text direction for text widgets
                if hasattr(self, 'url_text'):
                    self.url_text.config(wrap=tk.WORD)
            else:
                self.root.tk.call('tk', 'scaling', 1.0)
                self.root.option_add('*font', 'Segoe UI 10')
                self.root.option_add('*justify', 'left')
                if hasattr(self, 'url_text'):
                    self.url_text.config(wrap=tk.CHAR)
                    
            self.log_message(f"✅ Language updated to: {lang}")
            
        except Exception as e:
            self.log_message(f"❌ Error updating language: {e}")
            print(f"Language update error: {e}")

    def initialize_language_system(self):
        """Initialize the language system by ensuring Arabic is available."""
        available_languages = list(self.translations.keys())
        if 'Arabic' not in available_languages:
            self.log_message("⚠️ Arabic language not found in lang.json. Adding it.")
            # Add Arabic to the translations dictionary
            self.translations['Arabic'] = {
                'title': 'منصة التجميع المهني للمنتجات 1688 - جاهز لووكوميرس',
                'subtitle': 'تكامل متقدم مع WooCommerce - لا يتطلب أي مفاتيح API',
                'developer': 'تطوير بواسطة Rakmyat (https://rakmyat.com/) | تواصل: yoseabdallah866@gmail.com',
                'urls_management': 'إدارة الروابط المنتجات',
                'load_urls': 'تحميل الروابط',
                'save_urls': 'حفظ الروابط',
                'clear_all': 'مسح الكل',
                'add_sample': 'إضافة عينة',
                'validate_urls': 'تحقق من صحة الروابط',
                'scraper_controls': 'إدارة التجميع',
                'start_scraping': 'بدء التجميع',
                'stop_scraping': 'إيقاف التجميع',
                'open_output': 'فتح المجلد الإخراج',
                'open_csv': 'فتح CSV',
                'help': 'مساعدة',
                'progress_tracking': 'تتبع التقدم',
                'ready': 'جاهز للتجميع',
                'scraping_progress': 'جاري التجميع...',
                'stopping': 'يتم الإيقاف...',
                'current_product': 'المنتج الحالي:',
                'file_settings': 'إعدادات الملفات',
                'input_file': 'ملف الإدخال',
                'output_folder': 'مجلد الإخراج',
                'browse_input': 'تصفح',
                'browse_output': 'تصفح',
                'translation_settings': 'إعدادات الترجمة',
                'output_language': 'لغة الإخراج',
                'translation_language': 'لغة الترجمة',
                'auto_translate': 'تمكين الترجمة التلقائية',
                'image_optimization': 'تمكين التحسين الصورة',
                'scraping_speed': 'سرعة التجميع',
                'scraping_delay': 'تأخير التجميع (ثواني):',
                'url_limit': 'حد الروابط للتجميع:',
                'output_settings': 'إعدادات الإخراج',
                'timestamp_folders': 'إنشاء مجلدات مع تاريخ',
                'backup_files': 'إنشاء ملفات إضافية',
                'csv_prefix': 'اسم مسبق لملف CSV:',
                'advanced_settings': 'إعدادات متقدمة',
                'error_handling': 'معالجة الأخطاء',
                'save_errors': 'حفظ سجلات الأخطاء',
                'retry_failed': 'إعادة تجميع الروابط الفاشلة',
                'update_checking': 'التحقق من التحديثات',
                'check_updates': 'التحقق من التحديثات',
                'csv_preview': 'معاينة نتائج CSV',
                'refresh_preview': 'تحديث المعاينة',
                'open_excel': 'فتح في Excel',
                'open_log_folder': 'فتح مجلد السجلات',
                'clear_logs': 'مسح السجلات',
                'save_logs': 'حفظ السجلات',
                'image_preview': 'معاينة صورة المنتج',
                'previous_image': 'صورة سابقة',
                'next_image': 'صورة لاحقة',
                'image_index': 'صورة {current} من {total}',
                'no_images_available': 'لا توجد صور متاحة',
                'error_loading_image': 'خطأ في تحميل الصورة: {error}',
                'product_name': 'اسم المنتج',
                'sku': 'الكود SKU',
                'price': 'السعر',
                'categories': 'التصنيفات',
                'images': 'الصور'
            }
            # Save updated translations to lang.json
            with open('lang.json', 'w', encoding='utf-8') as f:
                json.dump(self.translations, f, indent=2)
            self.log_message("✅ Arabic language added to lang.json")

def main():
    """Main function to run the professional GUI"""
    root = tk.Tk()
    app = ProfessionalScraperGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main() 