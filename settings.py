import os
import json
import tkinter as tk
from tkinter import ttk

class ConfigManager:
    """Manages configuration file operations"""
    
    def __init__(self, config_file="screenshot_config.json"):
        self.config_file = config_file
        
    def load_config(self, default_settings):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
                    print(f"✅ Loaded configuration from {self.config_file}")
            else:
                print("📝 No configuration file found, using defaults")
        except Exception as e:
            print(f"⚠️  Failed to load configuration: {e}")
        
        return default_settings
    
    def save_config(self, settings):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"✅ Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"⚠️  Failed to save configuration: {e}")


class SettingsDialog:
    """Settings dialog for configuring the screenshot tool"""
    
    def __init__(self, parent, settings, on_save):
        self.parent = parent
        self.settings = settings.copy()
        self.on_save = on_save
        self.dialog = None
        
    def show(self):
        """Show the settings dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Screenshot Tool Settings")
        self.dialog.geometry("500x600")
        self.dialog.configure(bg='#2c2c2c')
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(self.dialog, bg='#2c2c2c')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, text="⚙️ Settings", 
            bg='#2c2c2c', fg='white', 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # General settings tab
        general_frame = tk.Frame(notebook, bg='#2c2c2c')
        notebook.add(general_frame, text="General")
        self.create_general_settings(general_frame)
        
        # Appearance tab
        appearance_frame = tk.Frame(notebook, bg='#2c2c2c')
        notebook.add(appearance_frame, text="Appearance")
        self.create_appearance_settings(appearance_frame)
        
        # Hotkeys tab
        hotkeys_frame = tk.Frame(notebook, bg='#2c2c2c')
        notebook.add(hotkeys_frame, text="Hotkeys")
        self.create_hotkeys_settings(hotkeys_frame)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#2c2c2c')
        button_frame.pack(pady=20)
        
        save_btn = tk.Button(
            button_frame, text="💾 Save", command=self.save_settings,
            bg='#4CAF50', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame, text="❌ Cancel", command=self.dialog.destroy,
            bg='#f44336', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind escape key
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())
        
    def create_general_settings(self, parent):
        """Create general settings controls"""
        # Auto-save
        auto_save_var = tk.BooleanVar(value=self.settings['auto_save'])
        auto_save_cb = tk.Checkbutton(
            parent, text="Auto-save screenshots", 
            variable=auto_save_var, bg='#2c2c2c', fg='white',
            selectcolor='#4CAF50', font=("Arial", 10)
        )
        auto_save_cb.pack(anchor=tk.W, pady=5)
        
        # Copy to clipboard
        copy_clipboard_var = tk.BooleanVar(value=self.settings['copy_to_clipboard'])
        copy_clipboard_cb = tk.Checkbutton(
            parent, text="Auto-copy to clipboard", 
            variable=copy_clipboard_var, bg='#2c2c2c', fg='white',
            selectcolor='#4CAF50', font=("Arial", 10)
        )
        copy_clipboard_cb.pack(anchor=tk.W, pady=5)
        
        # Include cursor
        include_cursor_var = tk.BooleanVar(value=self.settings['include_cursor'])
        include_cursor_cb = tk.Checkbutton(
            parent, text="Include cursor in screenshots", 
            variable=include_cursor_var, bg='#2c2c2c', fg='white',
            selectcolor='#4CAF50', font=("Arial", 10)
        )
        include_cursor_cb.pack(anchor=tk.W, pady=5)
        
        # Show magnifier
        show_magnifier_var = tk.BooleanVar(value=self.settings['show_magnifier'])
        show_magnifier_cb = tk.Checkbutton(
            parent, text="Show magnifier", 
            variable=show_magnifier_var, bg='#2c2c2c', fg='white',
            selectcolor='#4CAF50', font=("Arial", 10)
        )
        show_magnifier_cb.pack(anchor=tk.W, pady=5)
        
        # Default filename
        filename_frame = tk.Frame(parent, bg='#2c2c2c')
        filename_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            filename_frame, text="Default filename prefix:", 
            bg='#2c2c2c', fg='white', font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        filename_var = tk.StringVar(value=self.settings['default_filename'])
        filename_entry = tk.Entry(
            filename_frame, textvariable=filename_var,
            bg='#3c3c3c', fg='white', insertbackground='white',
            font=("Arial", 10)
        )
        filename_entry.pack(fill=tk.X, pady=5)
        
        # Store variables for later access
        self.auto_save_var = auto_save_var
        self.copy_clipboard_var = copy_clipboard_var
        self.include_cursor_var = include_cursor_var
        self.show_magnifier_var = show_magnifier_var
        self.filename_var = filename_var
        
    def create_appearance_settings(self, parent):
        """Create appearance settings controls"""
        # Overlay alpha
        alpha_frame = tk.Frame(parent, bg='#2c2c2c')
        alpha_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            alpha_frame, text="Overlay transparency:", 
            bg='#2c2c2c', fg='white', font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        alpha_var = tk.DoubleVar(value=self.settings['overlay_alpha'])
        alpha_scale = tk.Scale(
            alpha_frame, from_=0.1, to=0.8, resolution=0.1,
            variable=alpha_var, orient=tk.HORIZONTAL,
            bg='#2c2c2c', fg='white', highlightbackground='#2c2c2c',
            troughcolor='#3c3c3c', activebackground='#4CAF50'
        )
        alpha_scale.pack(fill=tk.X, pady=5)
        
        # Selection color
        color_frame = tk.Frame(parent, bg='#2c2c2c')
        color_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            color_frame, text="Selection border color:", 
            bg='#2c2c2c', fg='white', font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        color_var = tk.StringVar(value=self.settings['selection_color'])
        color_entry = tk.Entry(
            color_frame, textvariable=color_var,
            bg='#3c3c3c', fg='white', insertbackground='white',
            font=("Arial", 10)
        )
        color_entry.pack(fill=tk.X, pady=5)
        
        # Selection width
        width_frame = tk.Frame(parent, bg='#2c2c2c')
        width_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            width_frame, text="Selection border width:", 
            bg='#2c2c2c', fg='white', font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        width_var = tk.IntVar(value=self.settings['selection_width'])
        width_scale = tk.Scale(
            width_frame, from_=1, to=5, resolution=1,
            variable=width_var, orient=tk.HORIZONTAL,
            bg='#2c2c2c', fg='white', highlightbackground='#2c2c2c',
            troughcolor='#3c3c3c', activebackground='#4CAF50'
        )
        width_scale.pack(fill=tk.X, pady=5)
        
        # Magnifier settings
        mag_frame = tk.Frame(parent, bg='#2c2c2c')
        mag_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            mag_frame, text="Magnifier size:", 
            bg='#2c2c2c', fg='white', font=("Arial", 10)
        ).pack(anchor=tk.W)
        
        mag_size_var = tk.IntVar(value=self.settings['magnifier_size'])
        mag_size_scale = tk.Scale(
            mag_frame, from_=100, to=300, resolution=10,
            variable=mag_size_var, orient=tk.HORIZONTAL,
            bg='#2c2c2c', fg='white', highlightbackground='#2c2c2c',
            troughcolor='#3c3c3c', activebackground='#4CAF50'
        )
        mag_size_scale.pack(fill=tk.X, pady=5)
        
        # Store variables
        self.alpha_var = alpha_var
        self.color_var = color_var
        self.width_var = width_var
        self.mag_size_var = mag_size_var
        
    def create_hotkeys_settings(self, parent):
        """Create hotkeys settings controls"""
        # Hotkey info
        info_label = tk.Label(
            parent, text="Configure keyboard shortcuts\n(Changes require restart)", 
            bg='#2c2c2c', fg='#FF9800', font=("Arial", 10),
            justify=tk.LEFT
        )
        info_label.pack(anchor=tk.W, pady=10)
        
        # Hotkey mappings
        hotkeys = [
            ("Capture", "Enter"),
            ("Cancel", "Escape"),
            ("Save dialog", "Ctrl+S"),
            ("Copy to clipboard", "Ctrl+C"),
            ("Toggle magnifier", "Ctrl+M"),
            ("Settings", "Ctrl+,")
        ]
        
        for action, default_key in hotkeys:
            frame = tk.Frame(parent, bg='#2c2c2c')
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                frame, text=f"{action}:", 
                bg='#2c2c2c', fg='white', font=("Arial", 10),
                width=15, anchor=tk.W
            ).pack(side=tk.LEFT)
            
            key_var = tk.StringVar(value=default_key)
            key_entry = tk.Entry(
                frame, textvariable=key_var,
                bg='#3c3c3c', fg='white', insertbackground='white',
                font=("Arial", 10), width=15
            )
            key_entry.pack(side=tk.LEFT, padx=5)
            
            # Store reference to the variable
            setattr(self, f"{action.lower().replace(' ', '_')}_var", key_var)
        
    def save_settings(self):
        """Save the current settings"""
        # Update settings dictionary
        self.settings.update({
            'auto_save': self.auto_save_var.get(),
            'copy_to_clipboard': self.copy_clipboard_var.get(),
            'include_cursor': self.include_cursor_var.get(),
            'show_magnifier': self.show_magnifier_var.get(),
            'default_filename': self.filename_var.get(),
            'overlay_alpha': self.alpha_var.get(),
            'selection_color': self.color_var.get(),
            'selection_width': self.width_var.get(),
            'magnifier_size': self.mag_size_var.get()
        })
        
        # Call the save callback
        self.on_save(self.settings)
        
        # Close dialog
        self.dialog.destroy() 