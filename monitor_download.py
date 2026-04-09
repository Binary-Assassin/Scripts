import os
import time
import ctypes
import platform

# Function to prevent the system from sleeping
def prevent_sleep():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    elif platform.system() == "Linux":
        os.system("xset s off -dpms")

# Function to restore sleep settings
def restore_sleep():
    if platform.system() == "Windows":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)  # ES_CONTINUOUS
    elif platform.system() == "Linux":
        os.system("xset s on +dpms")

# Function to monitor the file in the Downloads folder
def monitor_file(file_name):
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder, file_name)

    print(f"Monitoring for file: {file_path}")
    
    # Wait until the file exists
    while not os.path.exists(file_path):
        print(f"Waiting for {file_name} to appear...")
        time.sleep(2)  # Check every 2 seconds

    print(f"File detected: {file_name}")

    # Wait for the file download to complete (file size stops changing)
    prev_size = -1
    while True:
        current_size = os.path.getsize(file_path)
        if current_size == prev_size:
            print("Download complete!")
            break
        prev_size = current_size
        print(f"File size: {current_size} bytes... still downloading.")
        time.sleep(2)  # Check every 2 seconds

# Main function
def main():
    file_name = input("Enter the file name (e.g., large_file.zip): ").strip()

    # Prevent sleep while monitoring the file
    print("Preventing system from sleeping...")
    prevent_sleep()
    
    # Monitor the Downloads folder for the file
    try:
        monitor_file(file_name)
    finally:
        # Restore sleep settings once done
        print("Restoring system sleep settings...")
        restore_sleep()

if __name__ == "__main__":
    main()
