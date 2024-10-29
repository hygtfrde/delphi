import os
import threading
from src.page_extractor import BookPageExtractor
from src.text_extractor import TextExtractor
from utils.spinner_task import spinner_task

done = False

def is_done():
    return done

def main(video_path_input):
    global done
    
    scanner = BookPageExtractor(video_path_input)
    extractor = TextExtractor()
    
    output_frames_dir = 'output_frames'
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        existing_files = os.listdir(output_frames_dir)
        if existing_files:
            response = input("There are already existing files in the output frames directory. Do you want to delete them and continue? (Y/N): ").strip().lower()
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
        else:
            print('Continuing...')
        
    # ----------- Perform actual video processing and frame simulation -----------
    done = False
    spinner_thread = threading.Thread(target=spinner_task, args=('lines', is_done))
    spinner_thread.start()

    try:
        scanner.process_video(output_frames_dir)
    except Exception as e:
        print(f'Error scanning video file: {e}')
    finally:
        done = True
        spinner_thread.join()
        
    # ----------- Perform actual text extraction from image frames -----------

    output_text_dir = 'output_text'
    if not os.path.exists(output_text_dir):
        os.makedirs(output_text_dir)
    else:
        existing_files = os.listdir(output_text_dir)
        if existing_files:
            response = input("There are already existing files in the output text directory. Do you want to delete them and continue? (Y/N): ").strip().lower()
            if response == 'y':
                for file in existing_files:
                    file_path = os.path.join(output_text_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Error: {e}")
            else:
                print("Operation aborted.")
                return
        else:
            print('No existing files found in output text, continuing...')

    done = False
    spinner_thread_dots = threading.Thread(target=spinner_task, args=('dots', is_done))
    spinner_thread_dots.start()
    
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
    main('input_videos/shorter.mp4')
