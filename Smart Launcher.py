#!/usr/bin/env python3
"""
1688 Product Scraper - Smart Launcher
One-click launcher with automatic setup and dependency checking
Developed by Rakmyat (https://rakmyat.com/)
Contact: yoseabdallah866@gmail.com
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading
import json
import time
from pathlib import Path

class SmartLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("1688 Product Scraper - Smart Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Configuration file for tracking setup status
        self.config_file = "launcher_config.json"
        self.setup_completed = self.load_config()
        
        # Create GUI
        self.create_gui()
        
        # Check everything on first run
        if not self.setup_completed:
            self.perform_first_time_setup()
        else:
            self.status_label.config(text="✅ Ready to launch - All checks passed")
            self.launch_button.config(state='normal')

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def create_gui(self):
        """Create the GUI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🛍️ 1688 Product Scraper", font=('Segoe UI', 20, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, text="Smart Professional Launcher", font=('Segoe UI', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="🔍 System Check", padding="15")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status text
        self.status_text = tk.Text(status_frame, height=8, width=60, font=('Consolas', 9))
        self.status_text.pack(fill=tk.X)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Checking system...", font=('Segoe UI', 9))
        self.status_label.pack(pady=(5, 0))
        
        # Features frame
        features_frame = ttk.LabelFrame(main_frame, text="🚀 Professional Features", padding="15")
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features_text = """
• Advanced Settings Panel • Real-time Progress Tracking • Live CSV Results Preview
• Multi-language Support • Product Image Preview • Comprehensive Logging
• URL Validation & Error Handling • Organized Output • WooCommerce Ready
        """
        
        features_label = ttk.Label(features_frame, text=features_text, font=('Segoe UI', 9), justify=tk.LEFT)
        features_label.pack(anchor=tk.W)
        
        # Launch button
        self.launch_button = ttk.Button(
            main_frame,
            text="🚀 Launch Professional GUI",
            command=self.launch_professional,
            style='Accent.TButton',
            state='disabled'
        )
        self.launch_button.pack(pady=10, fill=tk.X)
        
        # Help button
        help_button = ttk.Button(
            main_frame,
            text="❓ Help & Information",
            command=self.show_help
        )
        help_button.pack(pady=5, fill=tk.X)
        
        # Developer info
        dev_label = ttk.Label(main_frame, text="Developed by Rakmyat (https://rakmyat.com/)", font=('Segoe UI', 8))
        dev_label.pack(pady=(20, 0))

    def load_config(self):
        """Load configuration to check if setup is completed"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                return config.get('setup_completed', False)
        except Exception:
            pass
        return False

    def save_config(self):
        """Save configuration after successful setup"""
        try:
            config = {
                'setup_completed': True,
                'setup_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'python_version': sys.version,
                'files_checked': True
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.log_message(f"Warning: Could not save config: {e}")

    def log_message(self, message):
        """Add message to status text"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update()

    def perform_first_time_setup(self):
        """Perform comprehensive first-time setup"""
        self.log_message("🔍 Performing first-time system check...")
        self.progress_var.set(0)
        
        # Check Python
        self.log_message("✓ Checking Python installation...")
        if not self.check_python():
            return
        self.progress_var.set(20)
        
        # Check required files
        self.log_message("✓ Checking required files...")
        if not self.check_required_files():
            return
        self.progress_var.set(40)
        
        # Install dependencies
        self.log_message("✓ Installing dependencies...")
        if not self.install_dependencies():
            return
        self.progress_var.set(60)
        
        # Create directories
        self.log_message("✓ Creating output directories...")
        self.create_directories()
        self.progress_var.set(80)
        
        # Test scraper
        self.log_message("✓ Testing scraper components...")
        if not self.test_scraper():
            return
        self.progress_var.set(100)
        
        # Setup completed
        self.log_message("✅ All checks passed! Setup completed successfully.")
        self.status_label.config(text="✅ Ready to launch - All checks passed")
        self.launch_button.config(state='normal')
        self.save_config()

    def check_python(self):
        """Check Python installation"""
        try:
            version = sys.version_info
            if version.major < 3 or (version.major == 3 and version.minor < 7):
                self.log_message("❌ Error: Python 3.7 or higher required")
                self.log_message(f"Current version: {sys.version}")
                messagebox.showerror("Python Error", 
                    "Python 3.7 or higher is required.\n"
                    "Please install from https://www.python.org/downloads/")
                return False
            
            self.log_message(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error checking Python: {e}")
            return False

    def check_required_files(self):
        """Check if all required files exist"""
        required_files = [
            "professional_gui.py",
            "woocommerce_1688_scraper.py",
            "run_scraper.py",
            "requirements.txt"
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
            else:
                self.log_message(f"✅ Found {file}")
        
        if missing_files:
            self.log_message(f"❌ Missing files: {', '.join(missing_files)}")
            messagebox.showerror("Missing Files", 
                f"The following files are missing:\n{', '.join(missing_files)}\n\n"
                "Please ensure all files are in the same directory.")
            return False
        
        self.log_message("✅ All required files found")
        return True

    def install_dependencies(self):
        """Install required Python packages"""
        try:
            self.log_message("Installing required packages...")
            
            # List of required packages
            packages = [
                "requests",
                "beautifulsoup4",
                "cloudscraper",
                "translators",
                "pillow",
                "lxml"
            ]
            
            for package in packages:
                try:
                    self.log_message(f"Installing {package}...")
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", package, "--quiet"
                    ], check=True, capture_output=True)
                    self.log_message(f"✅ {package} installed")
                except subprocess.CalledProcessError:
                    self.log_message(f"⚠️ Warning: Could not install {package}")
            
            # Try to install from requirements.txt if it exists
            if os.path.exists("requirements.txt"):
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
                    ], check=True, capture_output=True)
                    self.log_message("✅ Requirements installed from requirements.txt")
                except subprocess.CalledProcessError:
                    self.log_message("⚠️ Warning: Could not install from requirements.txt")
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error installing dependencies: {e}")
            messagebox.showerror("Installation Error", 
                f"Failed to install dependencies:\n{e}\n\n"
                "Please try running: pip install -r requirements.txt")
            return False

    def create_directories(self):
        """Create necessary directories"""
        directories = ['output', 'logs', 'temp_downloads', 'product_images']
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.log_message(f"✅ Created directory: {directory}")
            except Exception as e:
                self.log_message(f"⚠️ Warning: Could not create {directory}: {e}")

    def test_scraper(self):
        """Test scraper components"""
        try:
            # Test importing the scraper
            self.log_message("Testing scraper imports...")
            
            # Test basic imports
            test_imports = [
                "import requests",
                "import cloudscraper",
                "from bs4 import BeautifulSoup",
                "import translators"
            ]
            
            for import_statement in test_imports:
                try:
                    exec(import_statement)
                    self.log_message(f"✅ {import_statement}")
                except Exception as e:
                    self.log_message(f"❌ {import_statement} failed: {e}")
                    return False
            
            self.log_message("✅ All scraper components tested successfully")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error testing scraper: {e}")
            return False

    def launch_professional(self):
        """Launch professional GUI"""
        try:
            self.log_message("🚀 Launching Professional GUI...")
            self.status_label.config(text="Launching Professional GUI...")
            
            # Launch in separate thread
            def run_gui():
                try:
                    subprocess.run([sys.executable, "professional_gui.py"], check=True)
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Launch Error", f"Failed to launch GUI: {e}")
                except Exception as e:
                    messagebox.showerror("Launch Error", f"Unexpected error: {e}")
            
            thread = threading.Thread(target=run_gui, daemon=True)
            thread.start()
            
            # Hide launcher window
            self.root.withdraw()
            
        except Exception as e:
            self.log_message(f"❌ Error launching GUI: {e}")
            messagebox.showerror("Error", f"Failed to launch GUI: {e}")

    def show_help(self):
        """Show help information"""
        help_text = """
🛍️ 1688 Product Scraper - Smart Launcher Help

📋 How to Use:
1. The launcher automatically checks everything on first run
2. Click "Launch Professional GUI" when ready
3. Add 1688.com product URLs
4. Configure settings and start scraping
5. Check output folder for CSV files

🔍 First-Time Setup:
• Python version check (3.7+ required)
• Required files validation
• Dependency installation
• Directory creation
• Component testing

🎛️ Professional Features:
• Advanced Settings Panel
• Real-time Progress Tracking
• Live CSV Results Preview
• Multi-language Support (English/Arabic)
• Product Image Preview
• Comprehensive Logging
• URL Validation & Error Handling
• Organized Output with Timestamps
• WooCommerce Ready CSV Export

📁 Output Files:
• woocommerce_import_*.csv (WooCommerce ready)
• backup_*.json (raw data backup)
• scraper_logs_*.txt (detailed logs)
• errors_*.log (error tracking)

🔧 Requirements:
• Python 3.7 or higher
• Internet connection
• Valid 1688.com URLs

📞 Support:
• Email: yoseabdallah866@gmail.com
• Website: https://rakmyat.com/
• GitHub: https://github.com/yousefabdallah171/1668-product-scraper-to-woocommerce-without-api

💡 Tips:
• First run may take longer due to setup
• Subsequent runs will be much faster
• Always validate URLs before scraping
• Check logs for troubleshooting
• No API keys required - 100% FREE!
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - 1688 Product Scraper Smart Launcher")
        help_window.geometry("700x600")
        help_window.resizable(True, True)
        
        # Center help window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (help_window.winfo_width() // 2)
        y = (help_window.winfo_screenheight() // 2) - (help_window.winfo_height() // 2)
        help_window.geometry(f"+{x}+{y}")
        
        # Create help content
        help_text_widget = tk.Text(help_window, wrap=tk.WORD, font=('Segoe UI', 10))
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(help_window, orient=tk.VERTICAL, command=help_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        help_text_widget.configure(yscrollcommand=scrollbar.set)

    def run(self):
        """Run the smart launcher"""
        # Configure style
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Segoe UI', 12, 'bold'))
        
        # Start GUI
        self.root.mainloop()

def main():
    """Main function"""
    try:
        launcher = SmartLauncher()
        launcher.run()
    except Exception as e:
        # If GUI fails, show error in console
        print(f"Error launching Smart Launcher: {e}")
        print("Please ensure Python and tkinter are installed.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 