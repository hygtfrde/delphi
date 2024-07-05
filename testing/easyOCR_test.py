import os
import cv2
import easyocr


def easyOCR_main():
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to the image file
    image_file = os.path.join(script_dir, 'test_frames/test_frame_2.jpg')

    if os.path.exists(image_file):
        # Load the image with OpenCV
        frame = cv2.imread(image_file)
        
        # Check if the image was successfully loaded
        if frame is not None:
            # Initialize the EasyOCR Reader
            reader = easyocr.Reader(['en'])  # Specify the language, 'en' for English
            
            # Convert the image to grayscale as EasyOCR may perform better on such images
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply OCR directly to the grayscale image
            results = reader.readtext(gray_frame)
            
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
