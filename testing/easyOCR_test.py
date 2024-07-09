import os
import cv2
import numpy as np
import easyocr


def flatten_image(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Edge detection using Canny
    edged = cv2.Canny(blurred, 50, 150)
    # Find contours in the edged image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort contours by area and keep the largest ones
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    points_original = None
    # Loop over the contours to find the one with four corners
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            points_original = approx
            break
    # If we didn't find a contour with four points, return the original frame
    if points_original is None or len(points_original) != 4:
        return frame
    # Rearrange points_original to match the order: top-left, top-right, bottom-right, bottom-left
    points_original = np.array(sorted(np.concatenate(points_original).tolist()), dtype="float32")
    # Ensure points are sorted in the order of top-left, top-right, bottom-right, bottom-left
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
    
    cv2.imshow('Flattened Image', flattened_image)
    key = cv2.waitKey(5000)
    if key != -1:
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return flattened_image




def enlarge_image(image_file):
    # Enlarge the image by a factor (e.g., 2 times)
    scale_factor = 2
    width = int(image_file.shape[1] * scale_factor)
    height = int(image_file.shape[0] * scale_factor)
    dimensions = (width, height)
    enlarged_image = cv2.resize(image_file, dimensions, interpolation=cv2.INTER_LINEAR)
    return enlarged_image



def easyOCR_main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, 'test_frames/test_frame_888.jpg')

    if os.path.exists(image_file):
        frame = cv2.imread(image_file)
        if frame is not None:
            # Specify the language, 'en' for English
            reader = easyocr.Reader(['en'])
            flattened_image = flatten_image(frame)
            
            cv2.imshow('Flattened Image', flattened_image)
            key = cv2.waitKey(5000)
            if key != -1:
                cv2.waitKey(0)
            cv2.imwrite('testing/test_flattened.jpg', flattened_image)
            cv2.destroyAllWindows()
            return True
            
            # Apply OCR
            results = reader.readtext(flattened_image)
            # Combine the extracted text into a single string
            text = '\n'.join([result[1] for result in results])

            # Extract the base name of the image file without extension
            base_name = os.path.splitext(os.path.basename(image_file))[0]
            text_output_file = os.path.join(script_dir, 'test_output_text', f'{base_name}_output.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")

