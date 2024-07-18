import os
import sys
import time
import threading
from src.page_extractor import BookPageExtractor
from src.text_extractor import TextExtractor


done = False
processed_frames = []
lock = threading.Lock()

def spinner_task(style='lines'):
    idx = 0
    spinner_symbols = ['-', '\\', '|', '/']
    dot_counter = 0
    prev_processed_frame = None
    BLUE = '\033[34m'
    RESET = '\033[0m'

    while not done:
        with lock:
            if style == 'lines':
                symbol = spinner_symbols[idx % len(spinner_symbols)]
                sys.stdout.write(f'\r{symbol} {processed_frames[-1] if processed_frames else f"{BLUE}Processing...{RESET}"}')
                idx += 1
            elif style == 'dots':
                if processed_frames and (not prev_processed_frame or processed_frames[-1] != prev_processed_frame):
                    dot_counter = 1
                    prev_processed_frame = processed_frames[-1]
                else:
                    dot_counter += 1
                    if dot_counter > 16:
                        dot_counter = 1
                sys.stdout.write(f'\r{BLUE}Processing{RESET}{"." * dot_counter} {processed_frames[-1] if processed_frames else ""}')
                sys.stdout.flush()

        time.sleep(0.3 if style == 'dots' else 0.1)

    with lock:
        if processed_frames and processed_frames[-1]:
            sys.stdout.write(f'\r✔ {processed_frames[-1]}\n')
            sys.stdout.flush()
       



def main():
    video_path = 'videos/test-scan.mov'
    scanner = BookPageExtractor(video_path)
    output_frames_dir = 'output_frames'

    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        existing_files = os.listdir(output_frames_dir)
        if existing_files:
            response = input("There are already existing files in the output directory. Do you want to delete them and continue? (Y/N): ").strip().lower()
            if response == 'y':
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
    spinner_thread = threading.Thread(target=spinner_task)
    spinner_thread.start()

    # ----------- Perform actual video processing and frame simulation -----------
    try:
        scanner.process_video(output_frames_dir)
    except Exception as e:
        print(f'Error scanning video file: {e}')
    finally:
        # Indicate that the processing is done
        done = True
        # Ensure the spinner thread finishes
        spinner_thread.join()

    # ----------- Perform actual text extraction from image frames -----------
    done = False
    spinner_thread_dots = threading.Thread(target=spinner_task, args=('dots',))
    spinner_thread_dots.start()
    extractor = TextExtractor()
    
    try:
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
