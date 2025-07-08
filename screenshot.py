import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
import mss
import mss.tools
import os
import datetime
import pyperclip
from io import BytesIO
import threading
import time
import json
import configparser
import math

# Try to import Windows-specific clipboard support
try:
    import win32clipboard
    import win32con
    WINDOWS_CLIPBOARD_AVAILABLE = True
except ImportError:
    WINDOWS_CLIPBOARD_AVAILABLE = False
    print("⚠️  Windows clipboard support not available. Install pywin32 for better clipboard functionality.")

# Try to import cursor capture support
try:
    import pyautogui
    CURSOR_CAPTURE_AVAILABLE = True
except ImportError:
    CURSOR_CAPTURE_AVAILABLE = False
    print("⚠️  Cursor capture not available. Install pyautogui for cursor support.")


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


class ScreenCaptureTool:
    def __init__(self):
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize settings with defaults
        self.settings = {
            'overlay_alpha': 0.2,
            'selection_color': '#ff4444',
            'selection_width': 2,
            'background_color': '#2c2c2c',
            'text_color': '#ffffff',
            'auto_save': True,
            'copy_to_clipboard': False,
            'default_filename': 'screenshot',
            'show_cursor': False,
            'include_cursor': False,
            'show_magnifier': False,  # Disabled by default to prevent errors
            'magnifier_size': 150,
            'magnifier_zoom': 3,
            'overlay_color': '#222222',
            'overlay_stipple': 'gray50',
        }
        
        # Load configuration
        self.settings = self.config_manager.load_config(self.settings)
        
        # Initialize monitor info
        self.initialize_monitors()
        
        # Initialize UI
        self.setup_ui()
        
        # State variables
        self.start_x = self.start_y = 0
        self.rect = None
        self.selection_text = None
        self.is_dragging = False
        self.captured_image = None
        self.preview_window = None
        self.magnifier_window = None
        self.magnifier_canvas = None
        self.settings_dialog = None

    def initialize_monitors(self):
        """Initialize monitor information with better error handling"""
        try:
            with mss.mss() as sct:
                # Get all monitors
                self.monitors = sct.monitors
                self.virtual_monitor = sct.monitors[0]  # Virtual monitor covering all screens
                
                # Calculate total display area
                self.total_width = self.virtual_monitor['width']
                self.total_height = self.virtual_monitor['height']
                self.total_left = self.virtual_monitor['left']
                self.total_top = self.virtual_monitor['top']
                
                print(f"📱 Detected {len(self.monitors)-1} monitor(s)")
                for i, monitor in enumerate(self.monitors[1:], 1):
                    print(f"   Monitor {i}: {monitor['width']}x{monitor['height']}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize monitors: {str(e)}")
            raise

    def setup_ui(self):
        """Setup the main UI with improved styling and functionality"""
        self.root = tk.Tk()
        self.root.title("Screen Capture Tool")
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.total_width}x{self.total_height}+{self.total_left}+{self.total_top}")
        
        # Window attributes
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 1.0)
        self.root.configure(bg=self.settings['background_color'])
        
        # Take a screenshot of the full screen for overlay effect
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            self.full_bg_img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            self.full_bg_tk = ImageTk.PhotoImage(self.full_bg_img)
        
        # Bind keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.cancel_capture())
        self.root.bind("<Control-s>", lambda e: self.save_with_dialog())
        self.root.bind("<Control-c>", lambda e: self.copy_to_clipboard())
        self.root.bind("<Control-m>", lambda e: self.toggle_magnifier())
        self.root.bind("<Control-comma>", lambda e: self.show_settings())
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.cancel_capture)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            cursor="crosshair",
            bg=self.settings['background_color'],
            highlightthickness=0,
            width=self.total_width,
            height=self.total_height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Display the screenshot as the canvas background
        self.bg_img_id = self.canvas.create_image(0, 0, image=self.full_bg_tk, anchor="nw")
        
        # Draw a static thick yellow dashed border around the entire canvas
        self.screen_border_id = self.canvas.create_rectangle(
            1, 1, self.total_width-2, self.total_height-2,
            outline="#FFD600", width=5, dash=(12, 6), tags="screen_border"
        )
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Create instruction overlay
        self.create_instruction_overlay()
        
        # Create magnifier only if explicitly enabled
        if self.settings.get('show_magnifier', False):
            self.create_magnifier()

    def create_instruction_overlay(self):
        """Create instruction text overlay"""
        instructions = [
            "🖱️  Click and drag to select area",
            "⌨️  Press ESC to cancel",
            "⌨️  Press Enter to capture",
            "⌨️  Ctrl+S to save with custom name",
            "⌨️  Ctrl+C to copy to clipboard",
            "⌨️  Ctrl+M to toggle magnifier",
            "⌨️  Ctrl+, to open settings"
        ]
        
        y_offset = 20
        for instruction in instructions:
            text_id = self.canvas.create_text(
                20, y_offset,
                text=instruction,
                fill=self.settings['text_color'],
                anchor="nw",
                font=("Arial", 10),
                tags="instructions"
            )
            y_offset += 25

    def show_settings(self):
        """Show settings dialog"""
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.root, self.settings, self.save_settings)
        self.settings_dialog.show()

    def save_settings(self, new_settings):
        """Save new settings and update UI"""
        self.settings = new_settings
        
        # Update UI elements
        self.root.attributes("-alpha", self.settings['overlay_alpha'])
        self.root.configure(bg=self.settings['background_color'])
        self.canvas.configure(bg=self.settings['background_color'])
        
        # Update magnifier
        if self.settings['show_magnifier'] and not self.magnifier_window:
            self.create_magnifier()
        elif not self.settings['show_magnifier'] and self.magnifier_window:
            self.magnifier_window.destroy()
        
        # Save to file
        self.config_manager.save_config(self.settings)
        
        print("✅ Settings updated and saved")

    def create_magnifier(self):
        """Create magnifier window for pixel-precise selection"""
        # Only create magnifier if it's enabled in settings
        if not self.settings.get('show_magnifier', False):
            return
            
        if hasattr(self, 'magnifier_window') and self.magnifier_window:
            self.magnifier_window.destroy()
        
        try:
            self.magnifier_window = tk.Toplevel()
            self.magnifier_window.title("Magnifier")
            self.magnifier_window.geometry(f"{self.settings['magnifier_size']}x{self.settings['magnifier_size']}")
            self.magnifier_window.overrideredirect(True)
            self.magnifier_window.attributes("-topmost", True)
            self.magnifier_window.configure(bg='black')
            
            # Create magnifier canvas
            self.magnifier_canvas = tk.Canvas(
                self.magnifier_window,
                width=self.settings['magnifier_size'],
                height=self.settings['magnifier_size'],
                bg='black',
                highlightthickness=2,
                highlightbackground='white'
            )
            self.magnifier_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Position magnifier initially
            self.magnifier_window.geometry(f"+{self.total_left + 100}+{self.total_top + 100}")
            
        except Exception as e:
            print(f"Error creating magnifier: {e}")
            self.magnifier_window = None
            self.magnifier_canvas = None

    def update_magnifier(self, x, y):
        """Update magnifier with current mouse position"""
        # Check if magnifier exists and is enabled
        if not hasattr(self, 'magnifier_window') or not self.magnifier_window:
            return
        if not hasattr(self, 'magnifier_canvas') or not self.magnifier_canvas:
            return
        
        try:
            # Capture a small region around the cursor
            with mss.mss() as sct:
                # Calculate capture region
                zoom = self.settings['magnifier_zoom']
                size = self.settings['magnifier_size']
                capture_size = size // zoom
                
                # Convert canvas coordinates to screen coordinates
                screen_x = int(x) + self.total_left
                screen_y = int(y) + self.total_top
                
                # Ensure capture region is within screen bounds
                left = max(0, screen_x - capture_size // 2)
                top = max(0, screen_y - capture_size // 2)
                right = min(self.total_width, left + capture_size)
                bottom = min(self.total_height, top + capture_size)
                
                # Adjust if we hit screen boundaries
                if right - left < capture_size:
                    left = max(0, right - capture_size)
                if bottom - top < capture_size:
                    top = max(0, bottom - capture_size)
                
                # Capture the region
                monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
                img = sct.grab(monitor)
                
                # Convert to PIL Image and resize
                pil_img = Image.frombytes("RGB", img.size, img.rgb)
                pil_img = pil_img.resize((size, size), Image.Resampling.NEAREST)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(pil_img)
                
                # Update canvas
                self.magnifier_canvas.delete("all")
                self.magnifier_canvas.create_image(0, 0, image=photo, anchor="nw")
                self.magnifier_canvas.image = photo  # Keep reference
                
                # Draw crosshair
                center = size // 2
                self.magnifier_canvas.create_line(center, 0, center, size, fill='red', width=1)
                self.magnifier_canvas.create_line(0, center, size, center, fill='red', width=1)
                
                # Position magnifier near cursor but not under it
                mag_x = screen_x + 20
                mag_y = screen_y + 20
                
                # Ensure magnifier stays on screen
                if mag_x + size > self.total_width:
                    mag_x = screen_x - size - 20
                if mag_y + size > self.total_height:
                    mag_y = screen_y - size - 20
                
                self.magnifier_window.geometry(f"+{mag_x}+{mag_y}")
                
        except Exception as e:
            # Silently handle magnifier errors
            pass

    def toggle_magnifier(self):
        """Toggle magnifier on/off"""
        try:
            if hasattr(self, 'magnifier_window') and self.magnifier_window:
                self.magnifier_window.destroy()
                self.magnifier_window = None
                self.magnifier_canvas = None
                self.settings['show_magnifier'] = False
            else:
                self.settings['show_magnifier'] = True
                self.create_magnifier()
        except Exception as e:
            print(f"Error toggling magnifier: {e}")

    def on_button_press(self, event):
        """Handle mouse button press"""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.is_dragging = True
        
        # Clear previous selection and overlays
        self.clear_selection()
        self.canvas.delete("overlay_clip")
        self.canvas.delete("selection_bg")
        # Remove the screen border when starting selection
        self.canvas.delete("screen_border")
        
        # Create new selection rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="#1976d2",  # bold blue
            width=3,
            dash=(5, 5),
            tags="selection"
        )
        
        # Create selection info text
        self.selection_text = self.canvas.create_text(
            self.start_x + 10, self.start_y - 25,
            text="",
            fill="#ffffff",
            anchor="nw",
            font=("Arial", 10, "bold"),
            tags="selection"
        )

    def on_move_press(self, event):
        """Handle mouse drag"""
        if not self.is_dragging or not self.rect:
            return
        
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        
        # Update rectangle
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
        
        # Update selection info
        self.update_selection_info(cur_x, cur_y)
        
        # Update overlay: darken only outside the selection area
        self.canvas.delete("overlay_clip")
        self.canvas.delete("selection_bg")
        x1, y1 = min(self.start_x, cur_x), min(self.start_y, cur_y)
        x2, y2 = max(self.start_x, cur_x), max(self.start_y, cur_y)
        overlay_color = self.settings.get('overlay_color', '#222222')
        overlay_stipple = self.settings.get('overlay_stipple', 'gray50')
        # Top
        self.canvas.create_rectangle(0, 0, self.total_width, y1, fill=overlay_color, stipple=overlay_stipple, outline="", tags="overlay_clip")
        # Bottom
        self.canvas.create_rectangle(0, y2, self.total_width, self.total_height, fill=overlay_color, stipple=overlay_stipple, outline="", tags="overlay_clip")
        # Left
        self.canvas.create_rectangle(0, y1, x1, y2, fill=overlay_color, stipple=overlay_stipple, outline="", tags="overlay_clip")
        # Right
        self.canvas.create_rectangle(x2, y1, self.total_width, y2, fill=overlay_color, stipple=overlay_stipple, outline="", tags="overlay_clip")
        
        # Paste the selected region of the screenshot image into the selection area
        if x2 > x1 and y2 > y1:
            region = self.full_bg_img.crop((int(x1), int(y1), int(x2), int(y2)))
            region_tk = ImageTk.PhotoImage(region)
            self.selection_bg_img = region_tk  # Keep reference
            self.canvas.create_image(x1, y1, image=region_tk, anchor="nw", tags="selection_bg")
        
        # Bring selection rectangle and info text to front
        self.canvas.tag_raise(self.rect)
        if self.selection_text:
            self.canvas.tag_raise(self.selection_text)
        
        # Update magnifier
        self.update_magnifier(cur_x, cur_y)

    def on_button_release(self, event):
        """Handle mouse button release"""
        print("[DEBUG] on_button_release called")
        if not self.is_dragging:
            print("[DEBUG] Not dragging, returning.")
            return
        
        self.is_dragging = False
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        print(f"[DEBUG] Mouse released at ({end_x}, {end_y})")
        
        # Calculate selection area
        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))
        print(f"[DEBUG] Selection coords: ({x1}, {y1}, {x2}, {y2})")
        
        # Remove overlay clips
        self.canvas.delete("overlay_clip")
        
        # Check if selection is too small
        if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
            print("[DEBUG] Selection too small, clearing selection.")
            self.clear_selection()
            self.canvas.delete("overlay")
            return
        
        # Update final selection info
        self.update_selection_info(end_x, end_y)
        
        # Show annotation toolbar after selection
        print("[DEBUG] Calling show_annotation_toolbar...")
        self.show_annotation_toolbar(x1, y1, x2, y2)

    def show_annotation_toolbar(self, x1, y1, x2, y2):
        print(f"[DEBUG] show_annotation_toolbar called with coords: ({x1}, {y1}, {x2}, {y2})")
        # Remove any existing toolbar
        if hasattr(self, 'annotation_toolbar') and self.annotation_toolbar:
            print("[DEBUG] Destroying existing annotation_toolbar.")
            self.annotation_toolbar.destroy()
            self.annotation_toolbar = None
        
        # Create toolbar window
        self.annotation_toolbar = tk.Toplevel(self.root)
        self.annotation_toolbar.overrideredirect(True)
        self.annotation_toolbar.attributes("-topmost", True)
        self.annotation_toolbar.configure(bg="#f0f0f0")
        print("[DEBUG] Annotation toolbar window created.")
        self.annotation_toolbar.focus_force()
        
        # Tool state
        self.current_tool = tk.StringVar(value="line")
        self.annotation_objects = []  # Store drawn shapes
        self.annotation_redo_stack = []  # For redo
        self.drawing_object = None
        self.text_entry = None
        
        # Tool buttons with bold colors
        btn_line = tk.Radiobutton(self.annotation_toolbar, text="/", variable=self.current_tool, value="line", indicatoron=0, width=2, fg="#d32f2f")
        btn_rect = tk.Radiobutton(self.annotation_toolbar, text="□", variable=self.current_tool, value="rect", indicatoron=0, width=2, fg="#1976d2")
        btn_ellipse = tk.Radiobutton(self.annotation_toolbar, text="○", variable=self.current_tool, value="ellipse", indicatoron=0, width=2, fg="#388e3c")
        btn_arrow = tk.Radiobutton(self.annotation_toolbar, text="→", variable=self.current_tool, value="arrow", indicatoron=0, width=2, fg="#d32f2f")
        btn_text = tk.Radiobutton(self.annotation_toolbar, text="T", variable=self.current_tool, value="text", indicatoron=0, width=2, fg="#6a1b9a")
        btn_line.pack(side=tk.LEFT, padx=2, pady=5)
        btn_rect.pack(side=tk.LEFT, padx=2, pady=5)
        btn_ellipse.pack(side=tk.LEFT, padx=2, pady=5)
        btn_arrow.pack(side=tk.LEFT, padx=2, pady=5)
        btn_text.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Undo/Redo buttons
        btn_undo = tk.Button(self.annotation_toolbar, text="↶", command=self.undo_annotation, width=2)
        btn_undo.pack(side=tk.LEFT, padx=2, pady=5)
        btn_redo = tk.Button(self.annotation_toolbar, text="↷", command=self.redo_annotation, width=2)
        btn_redo.pack(side=tk.LEFT, padx=2, pady=5)
        
        # Capture/Cancel buttons
        btn_capture = tk.Button(self.annotation_toolbar, text="Capture", command=self.confirm_capture, bg="#1976d2", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5, state=tk.NORMAL)
        btn_capture.pack(side=tk.LEFT, padx=5, pady=5)
        print(f"[DEBUG] Capture button state after creation: {btn_capture['state']}")
        btn_cancel = tk.Button(self.annotation_toolbar, text="Cancel", command=self.cancel_capture, bg="#f44336", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Center toolbar horizontally to the selection rectangle, at the bottom
        toolbar_width = 460
        toolbar_height = 40
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        sel_left = min(x1, x2) - self.total_left
        sel_right = max(x1, x2) - self.total_left
        sel_center_x = sel_left + ((sel_right - sel_left) // 2)
        sel_bottom_y = max(y1, y2) - self.total_top
        sel_top_y = min(y1, y2) - self.total_top
        pos_x = root_x + sel_center_x - (toolbar_width // 2)
        pos_y = root_y + sel_bottom_y + 10  # Default: below selection
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        # Clamp horizontally
        if pos_x < 0:
            pos_x = 0
        if pos_x + toolbar_width > screen_w:
            pos_x = screen_w - toolbar_width
        # If not enough space below, show above selection
        if pos_y + toolbar_height > screen_h:
            pos_y = root_y + sel_top_y - toolbar_height - 10
            if pos_y < 0:
                pos_y = 0  # Clamp to top
        self.annotation_toolbar.geometry(f"{toolbar_width}x{toolbar_height}+{pos_x}+{pos_y}")
        
        # Store selection for annotation tools
        self.selected_coords = (x1, y1, x2, y2)
        
        # Enable drawing on the selection area
        self.enable_annotation_mode(x1, y1, x2, y2)

    def enable_annotation_mode(self, x1, y1, x2, y2):
        """Enable drawing annotations on the selected area"""
        self.canvas.config(cursor="tcross")
        self.canvas.tag_raise("selection")
        self.canvas.bind("<ButtonPress-1>", self.on_annotate_press)
        self.canvas.bind("<B1-Motion>", self.on_annotate_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_annotate_release)

    def on_annotate_press(self, event):
        tool = self.current_tool.get()
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if tool == "line":
            self.drawing_object = self.canvas.create_line(x, y, x, y, fill="#d32f2f", width=4, tags="annotation")
        elif tool == "rect":
            self.drawing_object = self.canvas.create_rectangle(x, y, x, y, outline="#1976d2", width=4, tags="annotation")
        elif tool == "ellipse":
            self.drawing_object = self.canvas.create_oval(x, y, x, y, outline="#388e3c", width=4, tags="annotation")
        elif tool == "arrow":
            self.drawing_object = self.canvas.create_line(x, y, x, y, fill="#d32f2f", width=4, arrow=tk.LAST, tags="annotation")
        elif tool == "text":
            # Place a text entry box at the clicked location, embedded in the canvas
            if self.text_entry:
                self.canvas.delete(self.text_entry_window)
                self.text_entry.destroy()
            self.text_entry = tk.Entry(self.canvas, font=("Arial", 12), bd=1)
            self.text_entry_window = self.canvas.create_window(x, y, window=self.text_entry, anchor="nw")
            self.text_entry.focus_set()
            self.text_entry.bind("<Return>", lambda e: self.finish_text_annotation(x, y))
            self.text_entry.bind("<Escape>", lambda e: self.cancel_text_entry())
        self.annotate_start = (x, y)

    def on_annotate_drag(self, event):
        if not self.drawing_object:
            return
        tool = self.current_tool.get()
        x0, y0 = self.annotate_start
        x1, y1 = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if tool in ("line", "arrow"):
            self.canvas.coords(self.drawing_object, x0, y0, x1, y1)
        elif tool == "rect":
            self.canvas.coords(self.drawing_object, x0, y0, x1, y1)
        elif tool == "ellipse":
            self.canvas.coords(self.drawing_object, x0, y0, x1, y1)

    def on_annotate_release(self, event):
        if not self.drawing_object:
            return
        tool = self.current_tool.get()
        # Save the annotation object for undo/redo later
        self.annotation_objects.append(self.drawing_object)
        self.drawing_object = None
        self.annotate_start = None
        # Bring toolbar to front and focus it
        if hasattr(self, 'annotation_toolbar') and self.annotation_toolbar:
            self.annotation_toolbar.lift()
            self.annotation_toolbar.focus_force()

    def finish_text_annotation(self, x, y):
        if not self.text_entry:
            return
        text = self.text_entry.get()
        if text:
            text_id = self.canvas.create_text(x, y, text=text, fill="#6a1b9a", font=("Arial", 14, "bold"), anchor="nw", tags="annotation")
            self.annotation_objects.append(text_id)
        if hasattr(self, 'text_entry_window'):
            self.canvas.delete(self.text_entry_window)
            del self.text_entry_window
        self.text_entry.destroy()
        self.text_entry = None
        # Bring toolbar to front and focus it
        if hasattr(self, 'annotation_toolbar') and self.annotation_toolbar:
            self.annotation_toolbar.lift()
            self.annotation_toolbar.focus_force()

    def cancel_text_entry(self):
        if self.text_entry:
            if hasattr(self, 'text_entry_window'):
                self.canvas.delete(self.text_entry_window)
                del self.text_entry_window
            self.text_entry.destroy()
            self.text_entry = None
        # Bring toolbar to front and focus it
        if hasattr(self, 'annotation_toolbar') and self.annotation_toolbar:
            self.annotation_toolbar.lift()
            self.annotation_toolbar.focus_force()

    def on_mouse_move(self, event):
        """Handle mouse movement for real-time feedback"""
        try:
            if not self.is_dragging and self.rect:
                cur_x = self.canvas.canvasx(event.x)
                cur_y = self.canvas.canvasy(event.y)
                self.update_selection_info(cur_x, cur_y)
            
            # Update magnifier only if it's enabled
            if self.settings.get('show_magnifier', False):
                self.update_magnifier(event.x, event.y)
        except Exception as e:
            # Silently handle mouse move errors to prevent crashes
            pass

    def update_selection_info(self, cur_x, cur_y):
        """Update the selection information display"""
        if not self.selection_text:
            return
            
        x1 = int(min(self.start_x, cur_x))
        y1 = int(min(self.start_y, cur_y))
        x2 = int(max(self.start_x, cur_x))
        y2 = int(max(self.start_y, cur_y))
        
        width = x2 - x1
        height = y2 - y1
        
        info_text = f"Selection: {width} × {height} pixels"
        
        # Update text position and content
        self.canvas.coords(self.selection_text, x1 + 10, y1 - 25)
        self.canvas.itemconfig(self.selection_text, text=info_text)

    def clear_selection(self):
        """Clear current selection"""
        self.canvas.delete("selection")
        self.rect = None
        self.selection_text = None

    def get_selection_coordinates(self):
        """Get the current selection coordinates in screen space"""
        if not self.rect:
            return None
            
        coords = self.canvas.coords(self.rect)
        if len(coords) != 4:
            return None
            
        x1, y1, x2, y2 = coords
        
        # Convert to screen coordinates
        screen_x1 = int(min(x1, x2)) + self.total_left
        screen_y1 = int(min(y1, y2)) + self.total_top
        screen_x2 = int(max(x1, x2)) + self.total_left
        screen_y2 = int(max(y1, y2)) + self.total_top
        
        return screen_x1, screen_y1, screen_x2, screen_y2

    def capture_region(self, x, y, width, height):
        """Capture the specified region with threading support"""
        try:
            with mss.mss() as sct:
                monitor = {"top": y, "left": x, "width": width, "height": height}
                img = sct.grab(monitor)
                
                # Convert to PIL Image for processing
                pil_img = Image.frombytes("RGB", img.size, img.rgb)
                
                # Add cursor if enabled and available
                if self.settings['include_cursor'] and CURSOR_CAPTURE_AVAILABLE:
                    pil_img = self.add_cursor_to_image(pil_img, x, y, width, height)
                
                return pil_img
                
        except Exception as e:
            messagebox.showerror("Capture Error", f"Failed to capture screen: {str(e)}")
            return None

    def add_cursor_to_image(self, img, capture_x, capture_y, capture_width, capture_height):
        """Add cursor to the captured image"""
        try:
            # Get cursor position
            cursor_x, cursor_y = pyautogui.position()
            
            # Check if cursor is within capture area
            if (capture_x <= cursor_x <= capture_x + capture_width and 
                capture_y <= cursor_y <= capture_y + capture_height):
                
                # Calculate cursor position relative to captured image
                rel_x = cursor_x - capture_x
                rel_y = cursor_y - capture_y
                
                # Create a simple cursor icon
                draw = ImageDraw.Draw(img)
                cursor_size = 10
                
                # Draw cursor crosshair
                draw.line([(rel_x - cursor_size, rel_y), (rel_x + cursor_size, rel_y)], 
                         fill='red', width=2)
                draw.line([(rel_x, rel_y - cursor_size), (rel_x, rel_y + cursor_size)], 
                         fill='red', width=2)
                
                # Draw cursor circle
                draw.ellipse([(rel_x - 3, rel_y - 3), (rel_x + 3, rel_y + 3)], 
                           fill='red', outline='white', width=1)
            
            return img
            
        except Exception as e:
            print(f"Warning: Failed to add cursor to image: {e}")
            return img

    def show_capture_confirmation(self):
        """Show visual confirmation that capture was successful"""
        # Create a temporary confirmation overlay
        confirmation = tk.Toplevel(self.root)
        confirmation.overrideredirect(True)
        confirmation.attributes("-topmost", True)
        confirmation.configure(bg='green')
        
        # Position the confirmation window
        coords = self.get_selection_coordinates()
        if coords:
            x1, y1, x2, y2 = coords
            width, height = x2 - x1, y2 - y1
            confirmation.geometry(f"{width}x{height}+{x1}+{y1}")
        else:
            confirmation.geometry("200x100+100+100")
        
        # Add confirmation text
        label = tk.Label(
            confirmation,
            text="✅ Screenshot Captured!",
            bg='green',
            fg='white',
            font=("Arial", 12, "bold")
        )
        label.pack(expand=True)
        
        # Auto-close after 1 second
        confirmation.after(1000, confirmation.destroy)

    def save_screenshot(self, img, filename=None):
        """Save screenshot to file with threading"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.settings['default_filename']}_{timestamp}.png"
        
        try:
            # Ensure filename has .png extension
            if not filename.lower().endswith('.png'):
                filename += '.png'
            
            # Save the image
            img.save(filename, "PNG")
            print(f"✅ Screenshot saved to {filename}")
            return filename
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save screenshot: {str(e)}")
            return None

    def copy_to_clipboard_advanced(self, img):
        """Copy image to clipboard using Windows-specific methods"""
        try:
            if WINDOWS_CLIPBOARD_AVAILABLE:
                # Convert image to bytes
                img_bytes = BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                img_data = img_bytes.getvalue()
                
                # Use Windows clipboard API
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                
                # Set image data
                win32clipboard.SetClipboardData(win32con.CF_DIB, img_data)
                win32clipboard.CloseClipboard()
                
                print("📋 Screenshot copied to clipboard (Windows API)")
                return True
            else:
                # Fallback to basic clipboard
                img_bytes = BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                self.root.clipboard_clear()
                self.root.clipboard_append(img_bytes.getvalue())
                print("📋 Screenshot copied to clipboard (Basic)")
                return True
                
        except Exception as e:
            print(f"Clipboard error: {e}")
            return False

    def copy_to_clipboard(self):
        """Copy screenshot to clipboard with threading"""
        coords = self.get_selection_coordinates()
        if not coords:
            messagebox.showwarning("No Selection", "Please select an area first")
            return
            
        x1, y1, x2, y2 = coords
        width, height = x2 - x1, y2 - y1
        
        img = self.capture_region(x1, y1, width, height)
        if img:
            success = self.copy_to_clipboard_advanced(img)
            if not success:
                messagebox.showerror("Clipboard Error", "Failed to copy to clipboard")

    def save_with_dialog(self):
        """Save screenshot with custom filename dialog"""
        coords = self.get_selection_coordinates()
        if not coords:
            messagebox.showwarning("No Selection", "Please select an area first")
            return
            
        x1, y1, x2, y2 = coords
        width, height = x2 - x1, y2 - y1
        
        img = self.capture_region(x1, y1, width, height)
        if img:
            # Show save dialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save Screenshot As"
            )
            
            if filename:
                self.save_screenshot(img, filename)

    def show_preview_window(self, img):
        """Show preview window with retry/redo options"""
        if self.preview_window:
            self.preview_window.destroy()
        
        self.preview_window = tk.Toplevel()
        self.preview_window.title("Screenshot Preview")
        self.preview_window.geometry("800x600")
        self.preview_window.configure(bg='#2c2c2c')
        
        # Store the captured image
        self.captured_image = img
        
        # Create preview frame
        preview_frame = tk.Frame(self.preview_window, bg='#2c2c2c')
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resize image for preview (maintain aspect ratio)
        display_size = (600, 400)
        img_copy = img.copy()
        img_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage for display
        photo = ImageTk.PhotoImage(img_copy)
        
        # Create image label
        img_label = tk.Label(preview_frame, image=photo, bg='#2c2c2c')
        img_label.image = photo  # Keep a reference
        img_label.pack(pady=10)
        
        # Create info label
        info_text = f"Size: {img.width} × {img.height} pixels"
        info_label = tk.Label(preview_frame, text=info_text, bg='#2c2c2c', fg='white', font=("Arial", 10))
        info_label.pack(pady=5)
        
        # Create button frame
        button_frame = tk.Frame(preview_frame, bg='#2c2c2c')
        button_frame.pack(pady=20)
        
        # Buttons
        save_btn = tk.Button(
            button_frame, text="💾 Save", command=self.save_from_preview,
            bg='#4CAF50', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = tk.Button(
            button_frame, text="📋 Copy", command=self.copy_from_preview,
            bg='#2196F3', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        retry_btn = tk.Button(
            button_frame, text="🔄 Retry", command=self.retry_capture,
            bg='#FF9800', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        retry_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame, text="❌ Close", command=self.close_preview,
            bg='#f44336', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind escape key to close
        self.preview_window.bind("<Escape>", lambda e: self.close_preview())

    def save_from_preview(self):
        """Save screenshot from preview window"""
        if self.captured_image:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save Screenshot As"
            )
            
            if filename:
                self.save_screenshot(self.captured_image, filename)

    def copy_from_preview(self):
        """Copy screenshot from preview window"""
        if self.captured_image:
            success = self.copy_to_clipboard_advanced(self.captured_image)
            if not success:
                messagebox.showerror("Clipboard Error", "Failed to copy to clipboard")

    def retry_capture(self):
        """Retry capture from preview window"""
        if self.preview_window:
            self.preview_window.destroy()
            self.preview_window = None
        self.captured_image = None
        # Restore main window and reset state for new selection
        if hasattr(self, 'root') and self.root:
            self.root.deiconify()
            self.root.lift()
            self.canvas.delete("all")
            self.rect = None
            self.selection_text = None
            self.is_dragging = False
            self.annotation_objects = []
            self.annotation_redo_stack = []
            self.drawing_object = None
            self.text_entry = None
            if hasattr(self, 'annotation_toolbar') and self.annotation_toolbar:
                self.annotation_toolbar.destroy()
                self.annotation_toolbar = None
            # Recreate instruction overlay
            self.create_instruction_overlay()
            # Re-enable selection mode
            self.canvas.config(cursor="crosshair")
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def close_preview(self):
        """Close preview window and exit"""
        try:
            if hasattr(self, 'preview_window') and self.preview_window:
                self.preview_window.destroy()
                self.preview_window = None
            
            if hasattr(self, 'magnifier_window') and self.magnifier_window:
                self.magnifier_window.destroy()
                self.magnifier_window = None
                self.magnifier_canvas = None
            
            if hasattr(self, 'root') and self.root:
                self.root.quit()
                self.root.destroy()
                
        except Exception as e:
            print(f"Error during preview cleanup: {e}")
            # Force exit if cleanup fails
            import sys
            sys.exit(0)

    def confirm_capture(self):
        """Confirm and capture the current selection with annotations"""
        coords = self.get_selection_coordinates()
        if not coords:
            messagebox.showwarning("No Selection", "Please select an area first")
            return
        
        x1, y1, x2, y2 = coords
        width, height = x2 - x1, y2 - y1
        
        # Get selection rectangle's canvas coordinates
        if not self.rect:
            messagebox.showerror("Error", "No selection rectangle found.")
            return
        canvas_coords = self.canvas.coords(self.rect)
        canvas_x1 = int(min(canvas_coords[0], canvas_coords[2]))
        canvas_y1 = int(min(canvas_coords[1], canvas_coords[3]))
        
        # Hide the capture window
        self.root.withdraw()
        self.root.update()
        
        # Capture the region
        img = self.capture_region(x1, y1, width, height)
        if img:
            # Composite annotations onto the image using canvas offsets
            self.render_annotations_on_image(img, canvas_x1, canvas_y1)
            self.show_preview_window(img)
        else:
            self.show_capture_error()

    def render_annotations_on_image(self, img, offset_x, offset_y):
        """Draw all canvas annotations onto the PIL image, offsetting by selection area (canvas coordinates)"""
        draw = ImageDraw.Draw(img)
        for obj_id in self.annotation_objects:
            coords = self.canvas.coords(obj_id)
            if not coords:
                continue
            coords = [c - offset_x if i % 2 == 0 else c - offset_y for i, c in enumerate(coords)]
            obj_type = self.canvas.type(obj_id)
            if obj_type == "line":
                color = self.canvas.itemcget(obj_id, "fill")
                width = int(float(self.canvas.itemcget(obj_id, "width")))
                arrow = self.canvas.itemcget(obj_id, "arrow")
                draw.line(coords, fill=color, width=width)
                # Draw arrowhead if needed
                if arrow == str(tk.LAST) or arrow == "last":
                    x0, y0, x1, y1 = coords
                    # Arrowhead size and angle
                    arrow_length = 18
                    arrow_angle = math.radians(25)
                    dx = x1 - x0
                    dy = y1 - y0
                    angle = math.atan2(dy, dx)
                    left_angle = angle + math.pi - arrow_angle
                    right_angle = angle + math.pi + arrow_angle
                    left_x = x1 + arrow_length * math.cos(left_angle)
                    left_y = y1 + arrow_length * math.sin(left_angle)
                    right_x = x1 + arrow_length * math.cos(right_angle)
                    right_y = y1 + arrow_length * math.sin(right_angle)
                    draw.polygon([(x1, y1), (left_x, left_y), (right_x, right_y)], fill=color)
            elif obj_type == "rectangle":
                outline = self.canvas.itemcget(obj_id, "outline")
                width = int(float(self.canvas.itemcget(obj_id, "width")))
                draw.rectangle(coords, outline=outline, width=width)
            elif obj_type == "oval":
                outline = self.canvas.itemcget(obj_id, "outline")
                width = int(float(self.canvas.itemcget(obj_id, "width")))
                draw.ellipse(coords, outline=outline, width=width)
            elif obj_type == "text":
                text = self.canvas.itemcget(obj_id, "text")
                fill = self.canvas.itemcget(obj_id, "fill")
                draw.text((coords[0], coords[1]), text, fill=fill)
        # No return needed, modifies img in place

    def show_capture_error(self):
        """Show capture error and restore window"""
        messagebox.showerror("Capture Error", "Failed to capture screenshot")
        self.root.deiconify()

    def cancel_capture(self):
        """Cancel the capture operation"""
        try:
            # Clean up magnifier
            if hasattr(self, 'magnifier_window') and self.magnifier_window:
                self.magnifier_window.destroy()
                self.magnifier_window = None
            
            # Clean up preview window
            if hasattr(self, 'preview_window') and self.preview_window:
                self.preview_window.destroy()
                self.preview_window = None
            
            # Clean up settings dialog
            if hasattr(self, 'settings_dialog') and self.settings_dialog:
                self.settings_dialog.dialog.destroy()
                self.settings_dialog = None
            
            # Destroy main window
            if hasattr(self, 'root') and self.root:
                self.root.quit()
                self.root.destroy()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
            # Force exit if cleanup fails
            import sys
            sys.exit(0)

    def undo_annotation(self):
        if self.annotation_objects:
            last_id = self.annotation_objects.pop()
            # Store all info needed to recreate the annotation
            obj_type = self.canvas.type(last_id)
            coords = self.canvas.coords(last_id)
            info = {"type": obj_type, "coords": coords}
            if obj_type == "line":
                info["fill"] = self.canvas.itemcget(last_id, "fill")
                info["width"] = self.canvas.itemcget(last_id, "width")
                info["arrow"] = self.canvas.itemcget(last_id, "arrow")
            elif obj_type == "rectangle":
                info["outline"] = self.canvas.itemcget(last_id, "outline")
                info["width"] = self.canvas.itemcget(last_id, "width")
            elif obj_type == "oval":
                info["outline"] = self.canvas.itemcget(last_id, "outline")
                info["width"] = self.canvas.itemcget(last_id, "width")
            elif obj_type == "text":
                info["text"] = self.canvas.itemcget(last_id, "text")
                info["fill"] = self.canvas.itemcget(last_id, "fill")
                info["font"] = self.canvas.itemcget(last_id, "font")
            self.annotation_redo_stack.append(info)
            self.canvas.delete(last_id)

    def redo_annotation(self):
        if self.annotation_redo_stack:
            info = self.annotation_redo_stack.pop()
            obj_type = info["type"]
            coords = info["coords"]
            if obj_type == "line":
                obj_id = self.canvas.create_line(*coords, fill=info.get("fill", "red"), width=int(float(info.get("width", 2))), arrow=info.get("arrow", tk.NONE), tags="annotation")
            elif obj_type == "rectangle":
                obj_id = self.canvas.create_rectangle(*coords, outline=info.get("outline", "blue"), width=int(float(info.get("width", 2))), tags="annotation")
            elif obj_type == "oval":
                obj_id = self.canvas.create_oval(*coords, outline=info.get("outline", "green"), width=int(float(info.get("width", 2))), tags="annotation")
            elif obj_type == "text":
                obj_id = self.canvas.create_text(coords[0], coords[1], text=info.get("text", ""), fill=info.get("fill", "purple"), font=info.get("font", ("Arial", 14, "bold")), anchor="nw", tags="annotation")
            else:
                obj_id = None
            if obj_id:
                self.annotation_objects.append(obj_id)

    def run(self):
        """Run the application"""
        try:
            print("🚀 Starting Screen Capture Tool...")
            print("💡 Tips: Click and drag to select, ESC to cancel, Enter to capture")
            print(f"🔍 Magnifier: {'Enabled' if self.settings['show_magnifier'] else 'Disabled'}")
            print(f"🖱️  Cursor capture: {'Available' if CURSOR_CAPTURE_AVAILABLE else 'Not available'}")
            print(f"📋 Advanced clipboard: {'Available' if WINDOWS_CLIPBOARD_AVAILABLE else 'Not available'}")
            print(f"⚙️  Settings: Press Ctrl+, to open settings")
            
            # Add a timeout to prevent endless loops (5 minutes)
            def timeout_handler():
                print("⏰ Timeout reached, closing application...")
                self.cancel_capture()
            
            # Schedule timeout after 5 minutes
            self.root.after(300000, timeout_handler)  # 5 minutes = 300000 ms
            
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Application error: {str(e)}")
            self.cancel_capture()


def main():
    """Main entry point for the application"""
    try:
        app = ScreenCaptureTool()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()