import os
import cv2
import numpy as np
import easyocr


def easyOCR_main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, 'test_frames/test_frame_1.jpg')

    if os.path.exists(image_file):
        # Load the image with OpenCV
        frame = cv2.imread(image_file)
        
        # Check if the image was successfully loaded
        if frame is not None:
            # Specify the language, 'en' for English
            reader = easyocr.Reader(['en'])
            
            # Convert the image to grayscale as EasyOCR may perform better on such images
            # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Enlarge the image by a factor (e.g., 2 times)
            scale_factor = 2
            width = int(frame.shape[1] * scale_factor)
            height = int(frame.shape[0] * scale_factor)
            dimensions = (width, height)
            enlarged_frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_LINEAR)
            
            
            
            # Apply OCR directly to the frame, greyscale, etc.
            results = reader.readtext(enlarged_frame)
            # Combine the extracted text into a single string
            text = '\n'.join([result[1] for result in results])

            # Save extracted text to a file
            text_output_file = os.path.join(f"{script_dir}/test_output_text", 'text_output_1_easyocr.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")
