import os
import subprocess
from datetime import datetime
import re

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_video():
    url = input("Enter the video URL: ")
    print("\nOptions:")
    print("1: Download video with audio in best quality")
    print("2: Download audio only in best quality")
    print("3: Download video without audio in best quality")
    
    choice = input("\nSelect download mode (1/2/3): ")

    try:
        print("\nFetching video metadata...")
        result = subprocess.run(
            ["yt-dlp", "--get-title", "--get-id", url],
            capture_output=True,
            text=True,
            check=True
        )
        title, video_id = result.stdout.splitlines()
        sanitized_title = sanitize_filename(title)
        print(f"\nVideo title: {title}")
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred while fetching metadata: {e}")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = f"{sanitized_title}_{video_id}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nDownload folder created: {output_dir}")
    
    if choice == "1":
        command = f'yt-dlp -f "bestvideo+bestaudio/best" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nDownloading video with audio...")
    elif choice == "2":
        command = f'yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nDownloading audio only...")
    elif choice == "3":
        command = f'yt-dlp -f "bestvideo[ext=mp4]" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nDownloading video without audio...")
    else:
        print("\nInvalid choice! Please try again.")
        return

    try:
        subprocess.run(command, shell=True, check=True)
        print("\nDownload successful!")
    except subprocess.CalledProcessError as e:
        print(f"\nError occurred during download: {e}")
    
    with open(f"{output_dir}/download_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(f"Download URL: {url}\n")
        log_file.write(f"Download folder: {output_dir}\n")
        log_file.write(f"Video title: {title}\n")
        log_file.write(f"Video ID: {video_id}\n")
        log_file.write(f"Download time: {timestamp}\n")
    print(f"\nDownload information logged: {output_dir}/download_log.txt")

if __name__ == "__main__":
    download_video()
