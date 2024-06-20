import os
import cv2
import pytesseract

def main():
    """
        Combines script_dir (the directory of the current script) with 'test_frame_1.jpg',
        to create the full path to your image file relative to the script's location.
    """
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to the image file
    image_file = os.path.join(script_dir, 'test_frame_1.jpg')
    
    # Check if the file exists
    if os.path.exists(image_file):
        # Load the image
        frame = cv2.imread(image_file)
        
        # Check if the image was successfully loaded
        if frame is not None:
            # Apply OCR to the image
            text = pytesseract.image_to_string(frame)
            
            # Print extracted text
            # print(f"Text extracted from {image_file}:")
            # print(text)

            # Save extracted text to a file
            text_output_file = os.path.join(script_dir, 'text_output_1.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")

if __name__ == "__main__":
    main()
