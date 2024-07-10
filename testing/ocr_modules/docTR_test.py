from doctr.models import ocr_predictor
import cv2
import os


def docTR_main():
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Relative path to the image file
    image_file = os.path.join(script_dir, 'test_frames/test_frame_1.jpg')

    if os.path.exists(image_file):
        # Load the image with OpenCV
        frame = cv2.imread(image_file)

        # Check if the image was successfully loaded
        if frame is not None:
            # Convert the image to RGB format as docTR expects RGB input
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Initialize the docTR OCR Predictor
            predictor = ocr_predictor(pretrained=True)

            # Perform OCR on the image
            doc = predictor([rgb_frame])

            # Extract text from the OCR results
            text = '\n'.join(block['text'] for page in doc.pages for block in page['blocks'])

            # Save the extracted text to a file
            text_output_file = os.path.join(f"{script_dir}/test_output_text", 'text_output_1_doctr.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")
