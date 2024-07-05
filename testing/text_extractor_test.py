from keras_test import keras_ocr_main

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
        - Keras-OCR (current issues with modules and dependencies)
        - Doc TR
"""




# MAIN
if __name__ == "__main__":
    keras_ocr_main()
