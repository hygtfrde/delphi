#!/bin/bash

echo "-------"
echo "Docker /app"
ls /app
echo "-------"

# Activate the virtual environment
source /app/venv/bin/activate

echo "Please choose a test file to run:"
echo "1. docTR_test.py"
echo "2. easyOCR_test.py"
echo "3. keras_test.py"
echo "4. pytesseract_test.py"

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        python3 /app/testing/ocr_modules/docTR_test.py
        ;;
    2)
        python3 /app/testing/ocr_modules/easyOCR_test.py
        ;;
    3)
        python3 /app/testing/ocr_modules/keras_test.py
        ;;
    4)
        python3 /app/testing/ocr_modules/pytesseract_test.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
