import os
import subprocess
from datetime import datetime
import re

def sanitize_filename(filename):
    """Eltávolítja a nem megfelelő karaktereket a fájlnévből."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_video():
    url = input("Add meg a videó URL-jét: ")
    print("\nOpciók:")
    print("1: Videó letöltése a legjobb minőségben hanggal")
    print("2: Hang letöltése videó nélkül a legjobb minőségben")
    print("3: Videó letöltése hang nélkül a legjobb minőségben")
    
    choice = input("\nVálaszd ki a letöltési módot (1/2/3): ")

    # Videó metaadatok lekérése (cím és azonosító)
    try:
        print("\nVideó metaadatok lekérése...")
        result = subprocess.run(
            ["yt-dlp", "--get-title", "--get-id", url],
            capture_output=True,
            text=True,
            check=True
        )
        title, video_id = result.stdout.splitlines()
        sanitized_title = sanitize_filename(title)
        print(f"\nVideó címe: {title}")
    except subprocess.CalledProcessError as e:
        print(f"\nHiba történt a metaadatok lekérése során: {e}")
        return
    
    # Egyedi mappa létrehozása
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = f"{sanitized_title}_{video_id}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nLetöltési mappa létrehozva: {output_dir}")
    
    # Letöltési parancs kiválasztása
    if choice == "1":
        command = f'yt-dlp -f "bestvideo+bestaudio/best" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nVideó letöltése hanggal...")
    elif choice == "2":
        command = f'yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nCsak a hang letöltése...")
    elif choice == "3":
        command = f'yt-dlp -f "bestvideo[ext=mp4]" -o "{output_dir}/%(title)s.%(ext)s" "{url}"'
        print("\nVideó letöltése hang nélkül...")
    else:
        print("\nÉrvénytelen választás! Próbáld újra.")
        return

    # Letöltési parancs futtatása
    try:
        subprocess.run(command, shell=True, check=True)
        print("\nLetöltés sikeres!")
    except subprocess.CalledProcessError as e:
        print(f"\nHiba történt a letöltés során: {e}")
    
    # Napló mentése
    with open(f"{output_dir}/download_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write(f"Letöltési URL: {url}\n")
        log_file.write(f"Letöltési mappa: {output_dir}\n")
        log_file.write(f"Videó címe: {title}\n")
        log_file.write(f"Videó azonosítója: {video_id}\n")
        log_file.write(f"Letöltés ideje: {timestamp}\n")
    print(f"\nLetöltési információk naplózva: {output_dir}/download_log.txt")

if __name__ == "__main__":
    download_video()
