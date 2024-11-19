import subprocess

def get_system_version(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve version information: {e}")
        return None

MAC_OS_VERSION = get_system_version('sw_vers -productVersion')
APPLE_SCRIPT_VERSION = get_system_version('osascript -e \'version of application "System Events"\'')

# Compatibility check
SUPPORTED_MAC_OS_VERSION = "14.6.1"
SUPPORTED_APPLE_SCRIPT_VERSION = "1.3.6"

def is_compatible():
    if MAC_OS_VERSION < SUPPORTED_MAC_OS_VERSION or APPLE_SCRIPT_VERSION < SUPPORTED_APPLE_SCRIPT_VERSION:
        print(f"Warning: This project has been tested with macOS {SUPPORTED_MAC_OS_VERSION} and AppleScript {SUPPORTED_APPLE_SCRIPT_VERSION}."
              f" Detected macOS {MAC_OS_VERSION} and AppleScript {APPLE_SCRIPT_VERSION}. Compatibility may vary.")
        return False
    return True

if not is_compatible():
    print("Proceed with caution: Some functionality may be unsupported on this OS or AppleScript version.")
