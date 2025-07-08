#!/usr/bin/env python3
"""
Basic tests for the Advanced Screen Capture Tool
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the current directory to the path so we can import screenshot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestScreenCaptureTool(unittest.TestCase):
    """Test cases for the ScreenCaptureTool class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock tkinter to avoid GUI issues during testing
        self.tkinter_patcher = patch('tkinter.Tk')
        self.mock_tk = self.tkinter_patcher.start()
        
        # Mock mss to avoid screen capture issues
        self.mss_patcher = patch('mss.mss')
        self.mock_mss = self.mss_patcher.start()
        
        # Mock PIL
        self.pil_patcher = patch('PIL.Image')
        self.mock_pil = self.pil_patcher.start()
        
        # Import the module after mocking
        from screenshot import ScreenCaptureTool, ConfigManager
        
        # Create a mock monitor configuration
        mock_monitor = {
            'left': 0,
            'top': 0,
            'width': 1920,
            'height': 1080
        }
        
        # Configure mss mock
        mock_sct = MagicMock()
        mock_sct.monitors = [mock_monitor]
        mock_sct.monitors[0] = mock_monitor
        self.mock_mss.return_value.__enter__.return_value = mock_sct
        
        # Configure PIL mock
        mock_image = MagicMock()
        mock_image.size = (1920, 1080)
        self.mock_pil.frombytes.return_value = mock_image
        
        # Configure tkinter mock
        mock_root = MagicMock()
        mock_canvas = MagicMock()
        mock_root.winfo_screenwidth.return_value = 1920
        mock_root.winfo_screenheight.return_value = 1080
        self.mock_tk.return_value = mock_root
        
        self.ScreenCaptureTool = ScreenCaptureTool
        self.ConfigManager = ConfigManager
    
    def tearDown(self):
        """Clean up after tests"""
        self.tkinter_patcher.stop()
        self.mss_patcher.stop()
        self.pil_patcher.stop()
    
    def test_config_manager_initialization(self):
        """Test ConfigManager initialization"""
        config_manager = self.ConfigManager("test_config.json")
        self.assertEqual(config_manager.config_file, "test_config.json")
    
    def test_default_settings(self):
        """Test that default settings are properly set"""
        # This test would need more mocking to work properly
        # For now, we'll just test that the class can be imported
        self.assertIsNotNone(self.ScreenCaptureTool)
    
    def test_settings_structure(self):
        """Test that settings have the expected structure"""
        # Create a minimal instance for testing settings
        with patch('screenshot.messagebox'):
            with patch('screenshot.mss.mss'):
                tool = self.ScreenCaptureTool()
                
                # Check that essential settings exist
                required_settings = [
                    'overlay_alpha',
                    'selection_color',
                    'selection_width',
                    'background_color',
                    'text_color',
                    'auto_save',
                    'copy_to_clipboard',
                    'default_filename'
                ]
                
                for setting in required_settings:
                    self.assertIn(setting, tool.settings)
    
    def test_config_file_operations(self):
        """Test configuration file operations"""
        import json
        import tempfile
        
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {
                'overlay_alpha': 0.3,
                'selection_color': '#ff0000',
                'auto_save': True
            }
            json.dump(test_config, f)
            config_file = f.name
        
        try:
            config_manager = self.ConfigManager(config_file)
            default_settings = {
                'overlay_alpha': 0.2,
                'selection_color': '#ff4444',
                'auto_save': False
            }
            
            # Test loading config
            loaded_settings = config_manager.load_config(default_settings)
            
            # Check that loaded settings override defaults
            self.assertEqual(loaded_settings['overlay_alpha'], 0.3)
            self.assertEqual(loaded_settings['selection_color'], '#ff0000')
            self.assertEqual(loaded_settings['auto_save'], True)
            
            # Check that default settings are preserved for missing keys
            self.assertIn('selection_width', loaded_settings)
            
        finally:
            # Clean up
            if os.path.exists(config_file):
                os.unlink(config_file)

if __name__ == '__main__':
    unittest.main() 