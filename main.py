import os
import cv2
from src.page_extractor import BookPageExtractor

def check_existing_files(output_dir):
    files = os.listdir(output_dir)
    return len(files) > 0

def main():
    # Directory to save the extracted frames
    output_frames_dir = 'output_frames'
    # Ensure the output directory exists
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        # Check if there are existing files in the output directory
        existing_files = check_existing_files(output_frames_dir)
        if existing_files:
            response = input("There are already existing files in the output directory. Do you want to continue and overwrite them? (Y/N): ").strip().lower()
            if response != 'y':
                print("Operation aborted.")
                return

    # Video Path
    video_path = 'test/test-scan.mov'
    cap = cv2.VideoCapture(video_path)

    scanner = BookPageExtractor(video_path)
    scanner.process_video(output_frames_dir)

if __name__ == "__main__":
    main()
