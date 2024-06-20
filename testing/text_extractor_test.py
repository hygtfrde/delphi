import os
import cv2
import pytesseract
import easyocr
import numpy as np
from PIL import Image


"""
    Image Quality and Orientation:
        - Problem: The crease or curvature of the book page might cause distortion or blurriness in the image, making it difficult for pytesseract to accurately recognize text.
        - Solution: Ensure that the images are captured with good lighting, minimal shadows, and the pages are as flat as possible. Avoid angles that distort the text near the crease.
    Text Alignment and Distortion:
        - Problem: Text near the crease may not align perfectly due to the curvature or folding of the book, causing parts of the text to be cut off.
        - Solution: Use image preprocessing techniques such as deskewing (straightening skewed images), dewarping (correcting perspective distortion), and cropping to focus on the flat, clear areas of the page.
    OCR Configuration:
        - Problem: Pytesseract's default configuration might not be optimized for handling curved or distorted text regions.
        - Solution: Adjust pytesseract parameters such as page segmentation mode (--psm), OCR engine mode (--oem), and configuration settings (config argument in image_to_string method) to improve text recognition in challenging areas.   
    Image Preprocessing:
        - Problem: Lack of adequate preprocessing steps (like noise reduction, binarization, or contrast adjustment) before OCR can lead to inaccuracies near creases or folds.
        - Solution: Implement preprocessing steps tailored to enhance text readability, such as resizing, applying filters for noise reduction, adjusting brightness/contrast, and binarizing the image to improve text extraction.
    Other OCRs:
        - EasyOCR
        - Keras-OCR
        - DocTR
"""


def pytesseract_main():
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to the image file
    image_file = os.path.join(script_dir, 'test_frame_1.jpg')

    if os.path.exists(image_file):
        # 1) Load the image
        frame = cv2.imread(image_file)
        
        # 2) Try PIL Image
        # image_pil = Image.open(image_file)
        # frame = np.array(image_pil)
        # if frame.dtype != np.uint8:
        #     frame = frame.astype(np.uint8)
        
        # Check if the image was successfully loaded
        if frame is not None:
            # 1) Apply OCR to the image directly
            text = pytesseract.image_to_string(frame)
            
            # 2) Try Preprocessing
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # gray = cv2.GaussianBlur(gray, (3, 3), 0)
            # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # text = pytesseract.image_to_string(thresh)
            

            # Save extracted text to a file
            text_output_file = os.path.join(script_dir, 'text_output_1.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            # Print extracted text
            # print(f"Text extracted from {image_file}:")
            # print(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")


def easyOCR_main():
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to the image file
    image_file = os.path.join(script_dir, 'test_frame_1.jpg')

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
            text_output_file = os.path.join(script_dir, 'text_output_1_easyocr.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")


if __name__ == "__main__":
    easyOCR_main()
