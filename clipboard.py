import sys
from io import BytesIO
from PIL import Image, ImageDraw

try:
    import win32clipboard
    import win32con
    WINDOWS_CLIPBOARD_AVAILABLE = True
except ImportError:
    WINDOWS_CLIPBOARD_AVAILABLE = False
    print("⚠️  Windows clipboard support not available. Install pywin32 for better clipboard functionality.")

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import pyautogui
    CURSOR_CAPTURE_AVAILABLE = True
except ImportError:
    CURSOR_CAPTURE_AVAILABLE = False
    print("⚠️  Cursor capture not available. Install pyautogui for cursor support.")


def copy_image_to_clipboard(img, root=None):
    """Copy PIL image to clipboard, using Windows API if available, else fallback."""
    if WINDOWS_CLIPBOARD_AVAILABLE:
        try:
            output = BytesIO()
            img.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_DIB, data)
            win32clipboard.CloseClipboard()
            print("📋 Screenshot copied to clipboard (Windows API)")
            return True
        except Exception as e:
            print(f"Clipboard error (Windows): {e}")
            return False
    elif root is not None:
        try:
            output = BytesIO()
            img.save(output, format='PNG')
            output.seek(0)
            root.clipboard_clear()
            root.clipboard_append(output.getvalue())
            print("📋 Screenshot copied to clipboard (Tkinter)")
            return True
        except Exception as e:
            print(f"Clipboard error (Tkinter): {e}")
            return False
    elif pyperclip:
        try:
            output = BytesIO()
            img.save(output, format='PNG')
            pyperclip.copy(output.getvalue())
            print("📋 Screenshot copied to clipboard (pyperclip)")
            return True
        except Exception as e:
            print(f"Clipboard error (pyperclip): {e}")
            return False
    else:
        print("No clipboard method available.")
        return False


def add_cursor_to_image(img, capture_x, capture_y, capture_width, capture_height):
    """Add cursor to the captured image"""
    if not CURSOR_CAPTURE_AVAILABLE:
        return img
        
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