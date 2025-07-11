#!/usr/bin/env python3
"""
Test script for dropdown functionality
"""

import tkinter as tk
from tkinter import ttk
import json

def test_dropdown():
    """Test the dropdown functionality"""
    root = tk.Tk()
    root.title("Dropdown Test")
    root.geometry("400x300")
    
    # Load translations
    try:
        with open('lang.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
        print(f"✅ Loaded translations: {list(translations.keys())}")
    except Exception as e:
        print(f"❌ Error loading lang.json: {e}")
        return
    
    # Create frame
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Create label
    ttk.Label(frame, text="Language Selector Test", font=('Segoe UI', 14, 'bold')).pack(pady=(0, 20))
    
    # Create combobox
    language_var = tk.StringVar(value="English")
    available_languages = list(translations.keys())
    
    ttk.Label(frame, text="Select Language:").pack(side=tk.LEFT, padx=(0, 10))
    
    combo = ttk.Combobox(
        frame, 
        textvariable=language_var,
        values=available_languages, 
        state="readonly", 
        width=15,
        height=len(available_languages)
    )
    combo.pack(side=tk.LEFT, padx=(0, 10))
    
    # Test button
    def test_click():
        print(f"Current selection: {language_var.get()}")
        print(f"Available options: {combo['values']}")
        if 'Arabic' in combo['values']:
            print("✅ Arabic found in dropdown")
        else:
            print("❌ Arabic not found in dropdown")
    
    test_btn = ttk.Button(frame, text="Test Dropdown", command=test_click)
    test_btn.pack(side=tk.LEFT)
    
    # Status label
    status_label = ttk.Label(frame, text="Ready to test", foreground="green")
    status_label.pack(pady=(20, 0))
    
    def on_selection(event):
        selected = language_var.get()
        status_label.config(text=f"Selected: {selected}")
        print(f"Language changed to: {selected}")
    
    combo.bind('<<ComboboxSelected>>', on_selection)
    
    # Set initial value
    if available_languages:
        combo.set(available_languages[0])
    
    print(f"Dropdown created with {len(available_languages)} languages: {available_languages}")
    
    root.mainloop()

if __name__ == "__main__":
    test_dropdown() 