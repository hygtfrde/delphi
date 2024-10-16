import threading
import sys
import time

processed_frames = []
lock = threading.Lock()

def spinner_task(style='lines', done_flag=None):
    idx = 0
    spinner_symbols = ['-', '\\', '|', '/']
    dot_counter = 0
    prev_processed_frame = None
    BLUE = '\033[34m'
    RESET = '\033[0m'

    while not done_flag():
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
