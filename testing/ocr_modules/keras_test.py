import keras_ocr
import os
import cv2


def keras_ocr_main():
    print('KERAS')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file = os.path.join(script_dir, 'test_frames/test_frame_1.jpg')

    if image_file:
        print('FOUND it') 
    else:
        print('NOPE')

    if os.path.exists(image_file):
        # Load the image with OpenCV
        frame = cv2.imread(image_file)

        # Check if the image was successfully loaded
        if frame is not None:
            # Initialize the Keras OCR pipeline
            pipeline = keras_ocr.pipeline.Pipeline()

            # Convert the image to RGB format as Keras OCR works with RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run the OCR pipeline on the image
            prediction_groups = pipeline.recognize([rgb_frame])

            # Combine the extracted text into a single string
            text = '\n'.join([' '.join([text for text, _ in predictions]) for predictions in prediction_groups])

            # Save extracted text to a file
            text_output_file = os.path.join(f"{script_dir}/test_output_text", 'text_output_keras_ocr.txt')
            with open(text_output_file, 'w') as file:
                file.write(text)
                
            print(f"Extracted text saved to: {text_output_file}")
        else:
            print(f"CV2 failed to load image frame: {image_file}")
    else:
        print(f"File not found: {image_file}")
  