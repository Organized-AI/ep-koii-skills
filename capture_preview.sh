#!/bin/bash
# Quick script to help capture a preview of the web interface

echo "=================================="
echo "EP-133 K.O. II Web Interface"
echo "Preview Capture Helper"
echo "=================================="
echo ""
echo "1. Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "2. Starting web server..."
echo "   The interface will open at: http://localhost:5000"
echo ""
echo "3. NEXT STEPS:"
echo "   - Open http://localhost:5000 in your browser"
echo "   - Take a screenshot of the interface"
echo "   - Save it as: assets/web-interface-preview.png"
echo "   - Press Ctrl+C here to stop the server"
echo ""
echo "Starting server now..."
python3 web_interface.py
