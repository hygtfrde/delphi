import os
import cv2
import pytesseract
import numpy as np
from PIL import Image


# Path to Tesseract executable (change this to your Tesseract installation path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextExtractor:
    def __init__(self, output_folder='output_text'):
        self.output_folder = output_folder


    def extract_text(self, frame_path):
        if os.path.exists(frame_path):
            # 1) Load the image
            # frame = cv2.imread(frame_path)
            
            # Load the image using PIL
            image_pil = Image.open(frame_path)
            frame = np.array(image_pil)
            if frame.dtype != np.uint8:
                frame = frame.astype(np.uint8)

            # Check if the image was successfully loaded
            if frame is not None:
                # Apply OCR to the image
                text = pytesseract.image_to_string(frame)

                # Save the extracted text to a file
                text_output_file = os.path.join(self.output_folder, f'{os.path.basename(frame_path)}_text_output.txt')
                
                with open(text_output_file, 'w') as file:
                    file.write(text)
                
                print(f"Extracted text saved to: {text_output_file}")
            else:
                print(f"Failed to load image frame: {frame_path}")
        else:
            print(f"File not found: {frame_path}")
