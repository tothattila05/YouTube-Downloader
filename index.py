import os
import subprocess
from datetime import datetime
import re
import sys
import traceback

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_urls(input_source):
    try:
        if os.path.isfile(input_source) and input_source.lower().endswith(".txt"):
            with open(input_source, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        else:
            return input_source.split()
    except Exception as e:
        print(f"Error reading input: {e}")
        return []

def download_video():
    errors = []

    try:
        if len(sys.argv) > 1:
            input_source = " ".join(sys.argv[1:]).strip('"')
        else:
            input_source = input("Enter video URL(s) or drag a .txt file here:\n> ").strip()

        urls = get_urls(input_source)
        if not urls:
            print("\nNo valid URLs found.")
            input("\nPress Enter to exit...")
            return
        
        print("\nOptions:")
        print("1: Download video with audio in best quality")
        print("2: Download audio only in best quality")
        print("3: Download video without audio in best quality")
        choice = input("\nSelect download mode (1/2/3): ")

        for url in urls:
            try:
                print(f"\nFetching video metadata: {url}")
                result = subprocess.run(
                    ["yt-dlp", "--get-title", "--get-id", url],
                    capture_output=True,
                    text=True,
                    check=True
                )
                lines = result.stdout.splitlines()
                if len(lines) < 2:
                    print(f"Could not retrieve metadata for: {url}")
                    errors.append(f"Metadata error: {url}")
                    continue
                title, video_id = lines[:2]
                sanitized_title = sanitize_filename(title)
                print(f"Video title: {title}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to fetch metadata for {url}\n{e}")
                errors.append(f"Metadata fetch failed: {url}")
                continue
            except Exception as e:
                print(f"Unexpected error while fetching metadata: {e}")
                traceback.print_exc()
                errors.append(f"Unexpected metadata error: {url}")
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_dir = f"{sanitized_title}_{video_id}_{timestamp}"
            os.makedirs(output_dir, exist_ok=True)
            print(f"Download folder created: {output_dir}")

            if choice == "1":
                command = f'yt-dlp -f "bestvideo+bestaudio/best" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
                print("\nDownloading video with audio...")
                #command = f'yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
                #print("\nDownloading video with audio...")
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
                errors.append(f"Download failed: {url}")
            except Exception as e:
                print(f"\nUnexpected error during download: {e}")
                traceback.print_exc()
                errors.append(f"Unexpected download error: {url}")

            try:
                log_path = os.path.join(output_dir, "download_log.txt")
                with open(log_path, "w", encoding="utf-8") as log_file:
                    log_file.write(f"Download URL: {url}\n")
                    log_file.write(f"Download folder: {output_dir}\n")
                    log_file.write(f"Video title: {title}\n")
                    log_file.write(f"Video ID: {video_id}\n")
                    log_file.write(f"Download time: {timestamp}\n")
                print(f"\nDownload information logged: {log_path}")
            except Exception as e:
                print(f"Failed to write log file: {e}")
                errors.append(f"Log write failed: {url}")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        traceback.print_exc()
        errors.append(f"Fatal error: {e}")
    finally:
        if errors:
            print("\n========== ERRORS SUMMARY ==========")
            for err in errors:
                print(f"- {err}")
        else:
            print("\n✅ All downloads completed successfully!")
        input("\nPress Enter to close...")

if __name__ == "__main__":
    download_video()
