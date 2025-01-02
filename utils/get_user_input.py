import os
import threading
import time

def get_user_input(prompt, timeout=60):

    print(prompt)
    start_time = time.time()
    while True:
        try:
            user_input = input().strip().lower()
            return user_input
        except KeyboardInterrupt:
            print("\nOperation interrupted by user.")
            return None
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print(f"\nTimeout: No input received within {timeout} seconds.")
            return None
        elif elapsed_time > timeout - 10:
            if elapsed_time % 1 == 0:
                print(f"Exiting in {int(timeout - elapsed_time)} seconds...")
        elif elapsed_time > 0 and elapsed_time % 15 == 0:
            print("Are you there?")
