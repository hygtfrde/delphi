import os
import cv2
import pytesseract

# Path to Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Directory containing JPEG images
folder_path = 'extracted_frames'

# List all files in the directory
files = os.listdir(folder_path)

# Iterate over each file in the directory
for file_name in files:
    # Check if the file is a JPEG image
    if file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
        # Construct the full path to the image
        image_path = os.path.join(folder_path, file_name)

        # Load the image
        frame = cv2.imread(image_path)

        # Pre-process frame (e.g., resize, denoise, binarize)
        # Here, you can add any pre-processing steps you need before OCR
        # For example, resizing the image to a specific size
        # frame = cv2.resize(frame, (new_width, new_height))

        # Apply OCR to the pre-processed frame
        text = pytesseract.image_to_string(frame)

        # Print extracted text
        print(f"Text extracted from {file_name}:")
        print(text)
        print()  # Add a blank line for readability
