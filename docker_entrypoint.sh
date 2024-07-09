#!/bin/bash

echo "Please choose a test file to run:"
echo "1. keras_test.py"
echo "2. docTR_test.py"

read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        python3 testing/keras_test.py
        ;;
    2)
        python3 testing/docTR_test.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
