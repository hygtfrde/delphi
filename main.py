import os
import cv2
from src.page_extractor import BookPageExtractor

def check_existing_files(output_dir):
    files = os.listdir(output_dir)
    return len(files) > 0

def main():
    output_frames_dir = 'output_frames'
    
    # USER OPTIONS:
    # A) Raw Video Extraction
    # B) Hardware-assisted extraction (tripod, book holder)
    
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        existing_files = check_existing_files(output_frames_dir)
        if existing_files:
            response = input("There are already existing files in the output directory. Do you want to continue and overwrite them? (Y/N): ").strip().lower()
            if response != 'y':
                print("Operation aborted.")
                return

    # LOADING GRAPHIC .........

    # Video Path
    video_path = 'videos/test-scan.mov'

    scanner = BookPageExtractor(video_path)
    scanner.process_video(output_frames_dir)

if __name__ == "__main__":
    main()
