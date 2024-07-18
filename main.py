import os
import sys
import time
import threading
import cv2
from src.page_extractor import BookPageExtractor
from src.text_extractor import TextExtractor


done = False
processed_frames = []
lock = threading.Lock()

def spinner_task(style='lines'):
    idx = 0
    spinner_symbols = ['-', '\\', '|', '/']
    dot_counter = 0
    BLUE = '\033[34m'
    RESET = '\033[0m'

    while not done:
        with lock:
            if style == 'lines':
                symbol = spinner_symbols[idx % len(spinner_symbols)]
                sys.stdout.write(f'\r{symbol} {processed_frames[-1] if processed_frames else f"{BLUE}Processing...{RESET}"}')
                idx += 1
            elif style == 'dots':
                if processed_frames and len(processed_frames) > 1 and processed_frames[-1] != processed_frames[-2]:
                    dot_counter = 1  # Reset dot_counter to 1 for each new "Processing" line
                else:
                    dot_counter += 1
                    if dot_counter > 10:
                        dot_counter = 1
                sys.stdout.write(f'\r{BLUE}Processing{RESET}{"." * dot_counter} {processed_frames[-1] if processed_frames else ""}')
                sys.stdout.flush()

        time.sleep(1 if style == 'dots' else 0.1)  # 1 second for dots, 0.1 seconds for lines

    with lock:
        if processed_frames and processed_frames[-1]:
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

    output_text_dir = 'output_text'
    if not os.path.exists(output_text_dir):
        os.makedirs(output_text_dir)
          
    global done
    done = False

    # Start the first spinner thread
    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    try:
        # Perform actual video processing and frame simulation
        scanner.process_video(output_frames_dir)
    except Exception as e:
        print(f'Error scanning video file: {e}')
    finally:
        # Indicate that the processing is done
        done = True
        # Ensure the spinner thread finishes
        spinner_thread.join()

    done = False
    spinner_thread_dots = threading.Thread(target=spinner_task, args=('dots',))
    spinner_thread_dots.start()
    extractor = TextExtractor()
    
    try:
        # Perform actual text extraction from image frames
        scanned_frames = os.listdir(output_frames_dir)
        for frame in scanned_frames:
            extractor.extract_text(f'{output_frames_dir}/{frame}')
    except Exception as e:
        print(f'Error extracting text from frames: {e}')
    finally:
        done = True
        spinner_thread_dots.join()



# MAIN
if __name__ == "__main__":
    main()
