import os
import threading

def get_user_input(prompt, timeout):
    print(prompt)
    response = [None]  # Use a mutable object to allow updates from the thread

    def timeout_input():
        response[0] = 'y'  # Default response if timeout occurs

    timer = threading.Timer(timeout, timeout_input)
    timer.start()

    try:
        response[0] = input().strip().lower()  # Get user input
    finally:
        timer.cancel()  # Cancel the timer regardless of input

    return response[0]