import os
import threading
from src.page_scanner import BookPageScanner
import mac_vision_extractor as mac_vision_extractor
from utils.spinner_task import spinner_task
from utils.get_user_input import get_user_input

done = False

def is_done():
    return done

def main(video_path_input):
    global done
    page_scanner = BookPageScanner(video_path_input)
    output_frames_dir = 'output_frames'

    # ----------- Output Frames
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)
    else:
        existing_files = os.listdir(output_frames_dir)
        if existing_files:
            user_response = get_user_input("There are already existing files in the output frames directory. Do you want to delete them and continue? (Y/N): ", 60)
            if user_response == 'y':
                for file in existing_files:
                    file_path = os.path.join(output_frames_dir, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Error: {e}")
            else:
                print("Operation aborted.")
                # Prompt for whether to continue with text extraction or exit
                proceed_with_text_extraction = get_user_input("Would you like to proceed with text extraction on the existing frames? (Y/N): ", 60)
                if proceed_with_text_extraction.lower() == 'y':
                    print("Proceeding with text extraction...")
                else:
                    print("Exiting program.")
                    return
        else:
            print('Continuing...')
        
# ----------- Perform actual video processing and frame simulation -----------
    done = False
    spinner_thread = threading.Thread(target=spinner_task, args=('lines', is_done))
    spinner_thread.start()

    try:
        page_scanner.process_video(output_frames_dir)
    except Exception as e:
        print(f'Error scanning video file: {e}')
    finally:
        done = True
        spinner_thread.join()
# ------------------------------------------------------------------------

    # ----------- Output Text
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

# ----------- Perform actual text extraction from image frames -----------
    done = False
    spinner_thread_dots = threading.Thread(target=spinner_task, args=('dots', is_done))
    spinner_thread_dots.start()
    
    try:
        # Update folder to 'input_videos' instead of prompting for user selection
        mac_vision_extractor.text_extractor()
    except Exception as e:
        print(f'Error extracting text from frames: {e}')
    finally:
        done = True
        spinner_thread_dots.join()
# ------------------------------------------------------------------------


# MAIN
if __name__ == "__main__":
    main('input_videos/shorter.mp4')
