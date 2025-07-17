#!/usr/bin/env python3
"""
System Check Script for 1688 Product Scraper
Comprehensive validation of all components and dependencies
"""

import os
import sys
import subprocess
import importlib
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

class SystemChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
        self.cache_file = "src/system_check_cache.json"
        self.cache_valid_hours = 24  # Cache valid for 24 hours
        
    def get_system_hash(self):
        """Generate a hash of system state for caching"""
        system_info = {
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'files': [],
            'directories': []
        }
        
        # Check key files
        key_files = [
            "src/professional_gui.py",
            "src/woocommerce_1688_scraper.py", 
            "src/run_scraper.py",
            "src/requirements.txt",
            "src/settings.json",
            "src/lang.json",
            "launcher/Smart_Launcher.py",
            "launcher/script_check.bat",
            "launcher/Run Scraper.bat",
            "urls.txt"
        ]
        
        for file_path in key_files:
            if os.path.exists(file_path):
                try:
                    mtime = os.path.getmtime(file_path)
                    system_info['files'].append((file_path, mtime))
                except:
                    pass
        
        # Check directories
        key_dirs = ["src", "launcher", "output", "logs"]
        for dir_name in key_dirs:
            if os.path.exists(dir_name):
                system_info['directories'].append(dir_name)
        
        # Create hash
        hash_string = json.dumps(system_info, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def load_cache(self):
        """Load cached check results"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
                
                # Check if cache is still valid
                cache_time = datetime.fromisoformat(cache['timestamp'])
                if datetime.now() - cache_time < timedelta(hours=self.cache_valid_hours):
                    # Check if system state has changed
                    if cache.get('system_hash') == self.get_system_hash():
                        return cache.get('results', {})
        except:
            pass
        return None
    
    def save_cache(self, results):
        """Save check results to cache"""
        try:
            cache = {
                'timestamp': datetime.now().isoformat(),
                'system_hash': self.get_system_hash(),
                'results': results
            }
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
        except:
            pass
    
    def check_python_version(self):
        """Check Python version"""
        self.total_checks += 1
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 7:
                print("✅ Python version: {}.{}.{}".format(version.major, version.minor, version.micro))
                self.success_count += 1
            else:
                self.issues.append(f"Python {version.major}.{version.minor} is too old. Need 3.7+")
                print(f"❌ Python version too old: {version.major}.{version.minor}")
        except Exception as e:
            self.issues.append(f"Python version check failed: {e}")
            print(f"❌ Python version check failed: {e}")
    
    def check_dependencies(self):
        """Check required dependencies"""
        dependencies = [
            'requests',
            'beautifulsoup4',
            'lxml',
            'pandas',
            'tkinter'
        ]
        
        for dep in dependencies:
            self.total_checks += 1
            try:
                if dep == 'tkinter':
                    import tkinter
                    print(f"✅ {dep}: Available")
                else:
                    importlib.import_module(dep)
                    print(f"✅ {dep}: Available")
                self.success_count += 1
            except ImportError:
                self.issues.append(f"Missing dependency: {dep}")
                print(f"❌ {dep}: Not installed")
            except Exception as e:
                self.warnings.append(f"Warning with {dep}: {e}")
                print(f"⚠️ {dep}: Warning - {e}")
    
    def check_file_structure(self):
        """Check if all required files exist"""
        required_files = [
            "src/professional_gui.py",
            "src/woocommerce_1688_scraper.py", 
            "src/run_scraper.py",
            "src/requirements.txt",
            "src/settings.json",
            "src/lang.json",
            "launcher/Smart_Launcher.py",
            "launcher/script_check.bat",
            "launcher/Run Scraper.bat",
            "urls.txt"
        ]
        
        for file_path in required_files:
            self.total_checks += 1
            if os.path.exists(file_path):
                print(f"✅ {file_path}: Found")
                self.success_count += 1
            else:
                self.issues.append(f"Missing file: {file_path}")
                print(f"❌ {file_path}: Not found")
    
    def check_directories(self):
        """Check if required directories exist"""
        required_dirs = [
            ("src", "src/"),
            ("launcher", "launcher/"),
            ("output", "output/"),
            ("logs", "logs/")
        ]
        
        for dir_name, dir_path in required_dirs:
            self.total_checks += 1
            if os.path.exists(dir_path):
                print(f"✅ {dir_name}/: Found")
                self.success_count += 1
            else:
                self.issues.append(f"Missing directory: {dir_name}")
                print(f"❌ {dir_name}/: Not found")
    
    def check_urls_file(self):
        """Check if urls.txt has content"""
        self.total_checks += 1
        try:
            if os.path.exists("urls.txt"):
                with open("urls.txt", "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        print(f"✅ urls.txt: Found {len(lines)} URL(s)")
                        self.success_count += 1
                    else:
                        self.warnings.append("urls.txt is empty")
                        print("⚠️ urls.txt: Empty file")
            else:
                self.issues.append("urls.txt not found")
                print("❌ urls.txt: Not found")
        except Exception as e:
            self.issues.append(f"Error reading urls.txt: {e}")
            print(f"❌ urls.txt: Error - {e}")
    
    def check_settings(self):
        """Check if settings files are valid"""
        self.total_checks += 1
        try:
            if os.path.exists("src/settings.json"):
                with open("src/settings.json", "r", encoding="utf-8") as f:
                    json.load(f)
                print("✅ settings.json: Valid JSON")
                self.success_count += 1
            else:
                self.issues.append("settings.json not found")
                print("❌ settings.json: Not found")
        except Exception as e:
            self.issues.append(f"Invalid settings.json: {e}")
            print(f"❌ settings.json: Invalid - {e}")
    
    def install_dependencies(self):
        """Install missing dependencies"""
        print("\n🔧 Installing dependencies...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "src/requirements.txt"
            ], check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def run_all_checks(self):
        """Run all system checks with caching"""
        print("=" * 50)
        print("🔍 1688 Product Scraper - System Check")
        print("=" * 50)
        
        # Try to load from cache first
        cached_results = self.load_cache()
        if cached_results:
            print("📋 Using cached results (system unchanged)")
            self.issues = cached_results.get('issues', [])
            self.warnings = cached_results.get('warnings', [])
            self.success_count = cached_results.get('success_count', 0)
            self.total_checks = cached_results.get('total_checks', 0)
            
            # Show cached results
            success_rate = (self.success_count / self.total_checks) * 100 if self.total_checks > 0 else 0
            print(f"✅ Cached results: {self.success_count}/{self.total_checks} ({success_rate:.1f}%)")
            
            if self.warnings:
                print(f"\n⚠️ Warnings ({len(self.warnings)}):")
                for warning in self.warnings:
                    print(f"  • {warning}")
            
            if self.issues:
                print(f"\n❌ Issues ({len(self.issues)}):")
                for issue in self.issues:
                    print(f"  • {issue}")
            
            if not self.issues and not self.warnings:
                print("\n🎉 All checks passed! System is ready.")
                return True
            elif self.issues:
                print(f"\n⚠️ {len(self.issues)} issues found. Some features may not work.")
                return False
            else:
                print("\n✅ System ready with minor warnings.")
                return True
        
        # Run fresh checks
        print("🔍 Running fresh system check...")
        self.check_python_version()
        self.check_dependencies()
        self.check_file_structure()
        self.check_directories()
        self.check_urls_file()
        self.check_settings()
        
        print("\n" + "=" * 50)
        print("📊 CHECK RESULTS")
        print("=" * 50)
        
        success_rate = (self.success_count / self.total_checks) * 100 if self.total_checks > 0 else 0
        print(f"✅ Passed: {self.success_count}/{self.total_checks} ({success_rate:.1f}%)")
        
        if self.warnings:
            print(f"\n⚠️ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.issues:
            print(f"\n❌ Issues ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  • {issue}")
        
        # Save results to cache
        results = {
            'issues': self.issues,
            'warnings': self.warnings,
            'success_count': self.success_count,
            'total_checks': self.total_checks
        }
        self.save_cache(results)
        
        if not self.issues and not self.warnings:
            print("\n🎉 All checks passed! System is ready.")
            return True
        elif self.issues:
            print(f"\n⚠️ {len(self.issues)} issues found. Some features may not work.")
            return False
        else:
            print("\n✅ System ready with minor warnings.")
            return True

def main():
    """Main function"""
    checker = SystemChecker()
    success = checker.run_all_checks()
    
    if not success and checker.issues:
        print("\n🔧 Attempting to fix issues...")
        if any("Missing dependency" in issue for issue in checker.issues):
            checker.install_dependencies()
    
    # Don't wait for user input - just return
    return success

if __name__ == "__main__":
    main() 