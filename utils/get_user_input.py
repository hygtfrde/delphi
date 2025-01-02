import sys
import select
import time

def get_user_input(prompt, timeout=60):
    print(prompt, flush=True)
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = timeout - elapsed_time

        if remaining_time <= 0:
            print(f"\nTimeout: No input received within {timeout} seconds.")
            return None

        if remaining_time <= 10 and int(remaining_time) % 2 == 0:
            print(f"Exiting in {int(remaining_time)} seconds...", flush=True)

        if int(elapsed_time) % 15 == 0 and int(elapsed_time) != 0:
            print("Are you there?", flush=True)

        ready, _, _ = select.select([sys.stdin], [], [], 1)
        if ready:
            user_input = sys.stdin.readline().strip().lower()
            return user_input

        time.sleep(0.5)
