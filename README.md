# 📸 Advanced Screen Capture Tool

A powerful, feature-rich screen capture tool built with Python and Tkinter. Capture, annotate, and share screenshots with ease!

## ✨ Features

- **🖱️ Interactive Selection**: Click and drag to select any area of your screen
- **✏️ Annotation Tools**: Draw lines, rectangles, ellipses, arrows, and add text
- **🔍 Magnifier**: Pixel-precise selection with zoom functionality
- **📋 Clipboard Support**: Copy screenshots directly to clipboard
- **💾 Auto-save**: Automatically save screenshots with timestamps
- **⚙️ Customizable Settings**: Adjust colors, transparency, and hotkeys
- **🔄 Undo/Redo**: Full annotation history support
- **🎨 Modern UI**: Dark theme with intuitive interface
- **⌨️ Keyboard Shortcuts**: Quick access to all features
- **🖱️ Cursor Capture**: Include cursor in screenshots (optional)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/screenshot-tool.git
   cd screenshot-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python screenshot.py
   ```

## 📦 Dependencies

The tool uses the following Python packages:

- `tkinter` - GUI framework (included with Python)
- `PIL` (Pillow) - Image processing
- `mss` - Screen capture
- `pyperclip` - Clipboard operations
- `pywin32` - Windows clipboard support (optional)
- `pyautogui` - Cursor capture support (optional)

## 🎯 Usage

### Basic Screenshot
1. Run the application
2. Click and drag to select an area
3. Press **Enter** to capture
4. Choose to save or copy to clipboard

### Annotation Mode
1. Select an area (click and drag)
2. Use the annotation toolbar that appears:
   - **/** - Draw lines
   - **□** - Draw rectangles
   - **○** - Draw ellipses
   - **→** - Draw arrows
   - **T** - Add text
   - **↶/↷** - Undo/Redo
3. Click **Capture** to save with annotations

### Keyboard Shortcuts
- **Enter** - Capture selected area
- **Escape** - Cancel capture
- **Ctrl+S** - Save with custom filename
- **Ctrl+C** - Copy to clipboard
- **Ctrl+M** - Toggle magnifier
- **Ctrl+,** - Open settings

## ⚙️ Configuration

The tool automatically saves your preferences to `screenshot_config.json`. You can customize:

- **Auto-save**: Automatically save screenshots
- **Copy to clipboard**: Auto-copy after capture
- **Include cursor**: Show cursor in screenshots
- **Magnifier**: Enable pixel-precise selection
- **Colors**: Selection border and overlay colors
- **Transparency**: Overlay transparency level
- **Hotkeys**: Customize keyboard shortcuts

## 🛠️ Advanced Features

### Magnifier
Enable the magnifier in settings for pixel-precise selection. The magnifier shows a zoomed view around your cursor.

### Multi-Monitor Support
The tool automatically detects and supports multiple monitors, allowing you to capture across all screens.

### Annotation Tools
- **Lines**: Draw straight lines with customizable colors
- **Shapes**: Add rectangles and ellipses
- **Arrows**: Create directional arrows
- **Text**: Add text annotations with custom fonts
- **Undo/Redo**: Full history of annotation changes

### Clipboard Integration
- **Windows**: Uses native Windows clipboard API for better image quality
- **Cross-platform**: Fallback support for other operating systems

## 📁 File Structure

```
screenshot-tool/
├── screenshot.py          # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── .gitignore           # Git ignore rules
└── screenshot_config.json # User settings (auto-generated)
```

## 🔧 Troubleshooting

### Common Issues

**"Windows clipboard support not available"**
- Install pywin32: `pip install pywin32`

**"Cursor capture not available"**
- Install pyautogui: `pip install pyautogui`

**Permission errors on macOS**
- Grant screen recording permissions in System Preferences > Security & Privacy

**Display issues on Linux**
- Ensure you have a display server running (X11 or Wayland)

### Performance Tips

- Disable magnifier if not needed for better performance
- Use lower overlay transparency for faster rendering
- Close other applications to free up system resources

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Screen capture powered by [mss](https://github.com/BoboTiG/python-mss)
- Image processing with [Pillow](https://python-pillow.org/)
- Icons and emojis for better UX

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [issues](https://github.com/yourusername/screenshot-tool/issues)
3. Create a new issue with detailed information

---

**Made with ❤️ for the developer community** 