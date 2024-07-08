import os
import sys
import time
import threading
from tqdm import tqdm
import itertools
from threading import Thread
import cv2
from src.page_extractor import BookPageExtractor


# Global variables with synchronization
done = False
processed_frames = []
lock = threading.Lock()

def spinner_task():
    idx = 0
    spinner_symbols = ['-', '\\', '|', '/']
    global done

    while not done:
        symbol = spinner_symbols[idx % len(spinner_symbols)]
        with lock:
            sys.stdout.write(f'\r{symbol} {processed_frames[-1] if processed_frames else "Processing..."}')
            sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

    with lock:
        if processed_frames:
            sys.stdout.write(f'\r✔ {processed_frames[-1]}\n')
            sys.stdout.flush()

def check_existing_files(output_dir):
    files = os.listdir(output_dir)
    return len(files) > 0


def main():
    # Video Path and Scanner Object
    video_path = 'videos/test-scan.mov'
    scanner = BookPageExtractor(video_path)
    output_frames_dir = 'output_frames'

    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        # Check if there are existing files
        existing_files = os.listdir(output_frames_dir)
        if existing_files:
            response = input("There are already existing files in the output directory. Do you want to delete them and continue? (Y/N): ").strip().lower()
            if response == 'y':
                # Delete existing files in the directory
                for file in existing_files:
                    file_path = os.path.join(output_frames_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Error: {e}")
            else:
                print("Operation aborted.")
                return
            
    global done
    done = False

    # Start the spinner thread
    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    try:
        # Perform actual video processing and frame simulation
        scanner.process_video(output_frames_dir)
    finally:
        # Indicate that the processing is done
        done = True
        # Ensure the spinner thread finishes
        spinner_thread.join()



# MAIN
if __name__ == "__main__":
    main()
