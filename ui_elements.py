import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

class AnnotationToolbar(tk.Toplevel):
    def __init__(self, parent, on_capture, on_cancel, on_undo, on_redo, current_tool_var):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#f0f0f0")
        self.focus_force()
        self.current_tool = current_tool_var
        self.on_capture = on_capture
        self.on_cancel = on_cancel
        self.on_undo = on_undo
        self.on_redo = on_redo
        self._build_toolbar()

    def _build_toolbar(self):
        btn_line = tk.Radiobutton(self, text="/", variable=self.current_tool, value="line", indicatoron=0, width=2, fg="#d32f2f")
        btn_rect = tk.Radiobutton(self, text="□", variable=self.current_tool, value="rect", indicatoron=0, width=2, fg="#1976d2")
        btn_ellipse = tk.Radiobutton(self, text="○", variable=self.current_tool, value="ellipse", indicatoron=0, width=2, fg="#388e3c")
        btn_arrow = tk.Radiobutton(self, text="→", variable=self.current_tool, value="arrow", indicatoron=0, width=2, fg="#d32f2f")
        btn_text = tk.Radiobutton(self, text="T", variable=self.current_tool, value="text", indicatoron=0, width=2, fg="#6a1b9a")
        btn_line.pack(side=tk.LEFT, padx=2, pady=5)
        btn_rect.pack(side=tk.LEFT, padx=2, pady=5)
        btn_ellipse.pack(side=tk.LEFT, padx=2, pady=5)
        btn_arrow.pack(side=tk.LEFT, padx=2, pady=5)
        btn_text.pack(side=tk.LEFT, padx=2, pady=5)
        btn_undo = tk.Button(self, text="↶", command=self.on_undo, width=2)
        btn_undo.pack(side=tk.LEFT, padx=2, pady=5)
        btn_redo = tk.Button(self, text="↷", command=self.on_redo, width=2)
        btn_redo.pack(side=tk.LEFT, padx=2, pady=5)
        btn_capture = tk.Button(self, text="Capture", command=self.on_capture, bg="#1976d2", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5, state=tk.NORMAL)
        btn_capture.pack(side=tk.LEFT, padx=5, pady=5)
        btn_cancel = tk.Button(self, text="Cancel", command=self.on_cancel, bg="#f44336", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10, pady=5)
        btn_cancel.pack(side=tk.LEFT, padx=5, pady=5)


class PreviewWindow:
    def __init__(self, parent, img, on_save, on_copy, on_retry, on_close):
        self.parent = parent
        self.img = img
        self.on_save = on_save
        self.on_copy = on_copy
        self.on_retry = on_retry
        self.on_close = on_close
        self.window = None
        self.create_preview()

    def create_preview(self):
        if self.window:
            self.window.destroy()
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("Screenshot Preview")
        self.window.geometry("800x600")
        self.window.configure(bg='#2c2c2c')
        
        # Create preview frame
        preview_frame = tk.Frame(self.window, bg='#2c2c2c')
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resize image for preview (maintain aspect ratio)
        display_size = (600, 400)
        img_copy = self.img.copy()
        img_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage for display
        photo = ImageTk.PhotoImage(img_copy)
        
        # Create image label
        img_label = tk.Label(preview_frame, image=photo, bg='#2c2c2c')
        img_label.image = photo  # Keep a reference
        img_label.pack(pady=10)
        
        # Create info label
        info_text = f"Size: {self.img.width} × {self.img.height} pixels"
        info_label = tk.Label(preview_frame, text=info_text, bg='#2c2c2c', fg='white', font=("Arial", 10))
        info_label.pack(pady=5)
        
        # Create button frame
        button_frame = tk.Frame(preview_frame, bg='#2c2c2c')
        button_frame.pack(pady=20)
        
        # Buttons
        save_btn = tk.Button(
            button_frame, text="💾 Save", command=self.on_save,
            bg='#4CAF50', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = tk.Button(
            button_frame, text="📋 Copy", command=self.on_copy,
            bg='#2196F3', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        retry_btn = tk.Button(
            button_frame, text="🔄 Retry", command=self.on_retry,
            bg='#FF9800', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        retry_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = tk.Button(
            button_frame, text="❌ Close", command=self.on_close,
            bg='#f44336', fg='white', font=("Arial", 10, "bold"),
            relief=tk.FLAT, padx=20, pady=5
        )
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind escape key to close
        self.window.bind("<Escape>", lambda e: self.on_close())

    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None


class CaptureConfirmation:
    def __init__(self, parent, coords):
        self.parent = parent
        self.coords = coords
        self.window = None
        self.show_confirmation()

    def show_confirmation(self):
        # Create a temporary confirmation overlay
        self.window = tk.Toplevel(self.parent)
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg='green')
        
        # Position the confirmation window
        if self.coords:
            x1, y1, x2, y2 = self.coords
            width, height = x2 - x1, y2 - y1
            self.window.geometry(f"{width}x{height}+{x1}+{y1}")
        else:
            self.window.geometry("200x100+100+100")
        
        # Add confirmation text
        label = tk.Label(
            self.window,
            text="✅ Screenshot Captured!",
            bg='green',
            fg='white',
            font=("Arial", 12, "bold")
        )
        label.pack(expand=True)
        
        # Auto-close after 1 second
        self.window.after(1000, self.destroy)

    def destroy(self):
        if self.window:
            self.window.destroy()
            self.window = None 