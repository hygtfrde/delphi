import os
import cv2
import numpy as np
import easyocr

def flatten_image(frame):
    # Points in the original image (you may need to adjust these points)
    points_original = np.float32([[100, 200], [500, 200], [100, 700], [500, 700]])
    # Points in the output image
    width, height = 600, 800
    points_transformed = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Get the transformation matrix
    matrix = cv2.getPerspectiveTransform(points_original, points_transformed)
    # Apply perspective transformation
    flattened_image = cv2.warpPerspective(frame, matrix, (width, height))
    # Save or display the flattened image
    # cv2.imwrite('flattened_image.jpg', flattened_image)
    cv2.imshow('Flattened Image', flattened_image)
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

def detect_image_edges():
    return



def easyOCR_main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, 'test_frames/test_frame_1.jpg')

    if os.path.exists(image_file):
        frame = cv2.imread(image_file)
        
        if frame is not None:
            # Specify the language, 'en' for English
            reader = easyocr.Reader(['en'])
            # Apply OCR to the enlarged image
            results = reader.readtext(frame)
            # Combine the extracted text into a single string
            text = '\n'.join([result[1] for result in results])

            text_output_file = os.path.join(f"{script_dir}/test_output_text", 'text_output_1_easyocr.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")


