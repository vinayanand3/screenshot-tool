#!/bin/bash

echo "Starting Advanced Screen Capture Tool..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Run the application
python3 screenshot.py 