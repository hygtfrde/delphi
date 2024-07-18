import os
import cv2
import pytesseract

def pytesseract_main(frame_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    image_file = os.path.join(parent_dir, f'test_frames/{frame_path}')

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

            # Extract the base name of the image file without extension
            base_name = os.path.splitext(os.path.basename(image_file))[0]
            text_output_file = os.path.join(parent_dir, 'test_output_text', f'pytesseract_{base_name}_output.txt')
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
