#!/usr/bin/env python3
"""
🚀 1688 Product Scraper - Main Launcher
The primary entry point for the 1688 Product Scraper application.

Developed by Rakmyat (https://rakmyat.com/)
Contact: yoseabdallah866@gmail.com
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import json
import threading
import time

class MainLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 1688 Product Scraper - Main Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        self.check_environment()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚀 1688 Product Scraper", 
                               font=('Segoe UI', 24, 'bold'))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Professional WooCommerce Integration", 
                                  font=('Segoe UI', 12))
        subtitle_label.pack(pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, text="Checking system...", 
                                     font=('Segoe UI', 10))
        self.status_label.pack()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Launch Professional GUI button
        self.gui_btn = ttk.Button(buttons_frame, text="🖥️ Launch Professional GUI", 
                                 command=self.launch_gui, style='Accent.TButton')
        self.gui_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Launch Smart Launcher button
        self.smart_btn = ttk.Button(buttons_frame, text="🚀 Launch Smart Launcher", 
                                   command=self.launch_smart_launcher)
        self.smart_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Run Scraper button
        self.scraper_btn = ttk.Button(buttons_frame, text="⚡ Run Scraper Directly", 
                                     command=self.run_scraper)
        self.scraper_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Check System button
        self.check_btn = ttk.Button(buttons_frame, text="🔍 Check System", 
                                   command=self.check_system)
        self.check_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Open folders buttons
        folders_frame = ttk.Frame(main_frame)
        folders_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(folders_frame, text="📁 Open Output Folder", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(folders_frame, text="📋 Open Logs File", 
                  command=self.open_logs_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(folders_frame, text="📄 Open URLs File", 
                  command=self.open_urls_file).pack(side=tk.LEFT)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Information", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_text = """
📋 Quick Start Guide:
1. Add product URLs to urls.txt
2. Click "Launch Professional GUI" 
3. Configure settings and start scraping
4. Check output folder for CSV files

🌐 Features:
• No API keys required
• English & Arabic support
• WooCommerce ready output
• Professional GUI interface
• Live progress tracking

📞 Support: yoseabdallah866@gmail.com
🌐 Website: https://rakmyat.com/
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT, 
                              font=('Segoe UI', 9))
        info_label.pack(anchor=tk.W)
        
    def check_environment(self):
        """Check the environment and update status"""
        def check():
            issues = []
            
            # Check Python
            try:
                version = sys.version_info
                if version.major < 3 or (version.major == 3 and version.minor < 7):
                    issues.append("Python 3.7+ required")
            except:
                issues.append("Python not found")
            
            # Check required files
            required_files = [
                "src/professional_gui.py",
                "src/woocommerce_1688_scraper.py",
                "src/run_scraper.py",
                "src/requirements.txt",
                "launcher/Smart_Launcher.py"
            ]
            
            for file in required_files:
                if not os.path.exists(file):
                    issues.append(f"Missing: {file}")
            
            # Check directories
            required_dirs = ["src", "launcher", "output", "logs"]
            for dir in required_dirs:
                if not os.path.exists(dir):
                    issues.append(f"Missing directory: {dir}")
            
            # Update UI
            if issues:
                status_text = "⚠️ Issues found:\n" + "\n".join(issues[:3])
                if len(issues) > 3:
                    status_text += f"\n... and {len(issues) - 3} more"
            else:
                status_text = "✅ System ready"
            
            self.root.after(0, lambda: self.status_label.config(text=status_text))
        
        threading.Thread(target=check, daemon=True).start()
    
    def launch_gui(self):
        """Launch the professional GUI"""
        try:
            if not os.path.exists("src/professional_gui.py"):
                messagebox.showerror("Error", "Professional GUI not found in src/ folder")
                return
            
            # Change to src directory and run
            os.chdir("src")
            subprocess.Popen([sys.executable, "professional_gui.py"])
            os.chdir("..")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch GUI: {e}")
    
    def launch_smart_launcher(self):
        """Launch the smart launcher"""
        try:
            if not os.path.exists("launcher/Smart_Launcher.py"):
                messagebox.showerror("Error", "Smart Launcher not found in launcher/ folder")
                return
            
            # Change to launcher directory and run
            os.chdir("launcher")
            subprocess.Popen([sys.executable, "Smart_Launcher.py"])
            os.chdir("..")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Smart Launcher: {e}")
    
    def run_scraper(self):
        """Run the scraper directly"""
        try:
            if not os.path.exists("src/run_scraper.py"):
                messagebox.showerror("Error", "Scraper not found in src/ folder")
                return
            
            # Change to src directory and run
            os.chdir("src")
            subprocess.Popen([sys.executable, "run_scraper.py"])
            os.chdir("..")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run scraper: {e}")
    
    def check_system(self):
        """Run system check"""
        try:
            # Run the system check directly
            subprocess.run([sys.executable, "src/system_check.py"], shell=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run system check: {e}")
    
    def open_output_folder(self):
        """Open the output folder"""
        try:
            if os.path.exists("output"):
                os.startfile("output")
            else:
                messagebox.showinfo("Info", "Output folder not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open output folder: {e}")
    
    def open_logs_file(self):
        """Open the logs file"""
        try:
            logs_file = "logs/woocommerce_scraper.log"
            if os.path.exists(logs_file):
                os.startfile(logs_file)
            else:
                messagebox.showinfo("Info", "Logs file not found. Run the scraper first to generate logs.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open logs file: {e}")
    
    def open_urls_file(self):
        """Open the URLs file"""
        try:
            if os.path.exists("urls.txt"):
                os.startfile("urls.txt")
            else:
                messagebox.showinfo("Info", "urls.txt not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open URLs file: {e}")
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    app = MainLauncher()
    app.run()

if __name__ == "__main__":
    main() 