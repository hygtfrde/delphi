import os
import cv2
import numpy as np
import easyocr
import os

"""
This program:
    - processes an image
    - improves its quality
    - extracts text using optical character recognition (OCR)
"""

def enlarge_image(image_file):
    # Enlarge the image by a factor (e.g., 2 times)
    scale_factor = 2
    width = int(image_file.shape[1] * scale_factor)
    height = int(image_file.shape[0] * scale_factor)
    dimensions = (width, height)
    enlarged_image = cv2.resize(image_file, dimensions, interpolation=cv2.INTER_LINEAR)
    return enlarged_image


def flatten_image(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Thresholding for better edge detection
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    edged = cv2.Canny(thresh, 50, 150)
    
    # Morphological operations to improve edge continuity
    kernel = np.ones((5, 5), np.uint8)
    edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the edged image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort contours by area and keep the largest ones
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    points_original = None

    def is_rectangular(contour):
        # Check for convexity and potentially other shape properties
        return cv2.isContourConvex(contour) and len(cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)) == 4

    # Loop over the contours to find the one with four corners and largest area
    for contour in contours:
        if cv2.contourArea(contour) > 1000 and is_rectangular(contour):  # Area threshold to filter out small contours
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                points_original = approx
                break

    # If we didn't find a contour with four points, return the original frame
    if points_original is None or len(points_original) != 4:
        print('WARNING: edge detection has issues')
        return frame
    print('Detected 4 different edges!!!')

    # Rearrange points_original to match the order: top-left, top-right, bottom-right, bottom-left
    points_original = np.array(sorted(np.concatenate(points_original).tolist()), dtype="float32")
    s = points_original.sum(axis=1)
    diff = np.diff(points_original, axis=1)
    
    rect = np.zeros((4, 2), dtype="float32")
    rect[0] = points_original[np.argmin(s)]  # top-left
    rect[2] = points_original[np.argmax(s)]  # bottom-right
    rect[1] = points_original[np.argmin(diff)]  # top-right
    rect[3] = points_original[np.argmax(diff)]  # bottom-left

    # Points in the output image
    (tl, tr, br, bl) = rect
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    points_transformed = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    
    # Get the transformation matrix
    matrix = cv2.getPerspectiveTransform(rect, points_transformed)
    # Apply perspective transformation
    flattened_image = cv2.warpPerspective(frame, matrix, (maxWidth, maxHeight))
    
    return flattened_image


def enhance_image(image):
    """ Apply quality improvement techniques: denoising, sharpening, and contrast adjustment """
    
    # Denoise using Gaussian blur
    denoised = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Sharpen the image using a kernel
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    # Convert to grayscale and apply histogram equalization to improve contrast
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    contrast_adjusted = cv2.equalizeHist(gray)
    
    return contrast_adjusted


def display_images(original, improved):
    """ Display original and improved images side by side """
    
    # Convert gray to BGR for stacking
    combined = np.hstack((original, cv2.cvtColor(improved, cv2.COLOR_GRAY2BGR)))
    cv2.imshow('Original vs Improved', combined)
    
    key = cv2.waitKey(5000)
    if key != -1:
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def easyOCR_main(frame_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    image_file = os.path.join(parent_dir, f'test_frames/{frame_path}')

    output_dir = os.path.join(parent_dir, 'easyOCR_output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory 'easyOCR_output' created at: {output_dir}")
    else:
        print(f"Directory 'easyOCR_output' already exists at: {output_dir}")

    if os.path.exists(image_file):
        # Extract the base name of the image file without extension
        base_name = os.path.splitext(os.path.basename(image_file))[0]
        frame = cv2.imread(image_file)
        if frame is not None:
            # Specify the language, 'en' for English
            reader = easyocr.Reader(['en'])
            
            # Apply quality improvements
            improved_frame = enhance_image(frame) 
            
            # Display both images for comparison
            display_images(frame, improved_frame)
            
            # Apply OCR on the improved image
            results = reader.readtext(frame)
            improved_results = reader.readtext(improved_frame)


            # Combine the extracted text into a single string
            text = '\n'.join([result[1] for result in results])
            improved_text = '\n'.join([result[1] for result in improved_results])

            # Save the extracted text into the same directory
            text_output_file = os.path.join(output_dir, f'{base_name}_text_output.txt')
            improved_text_output_file = os.path.join(output_dir, f'{base_name}_improved_text_output.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
            with open(improved_text_output_file, 'w') as file:
                file.write(improved_text)

            print(f"Extracted text saved to: {text_output_file}")
            print(f"Extracted text: {text}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")


# Test the program with an image
if __name__ == "__main__":
    easyOCR_main('your_image.jpg')
