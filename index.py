import os
import subprocess
from datetime import datetime
import re

def tisztit_fajlnev(fajlnev):
    return re.sub(r'[\\/*?:"<>|]', "_", fajlnev)

def video_letoltes():
    url = input("Add meg a videó URL-jét: ")
    print("\nOpciók:")
    print("1: Videó letöltése a legjobb minőségben hanggal")
    print("2: Hang letöltése videó nélkül a legjobb minőségben")
    print("3: Videó letöltése hang nélkül a legjobb minőségben")
    
    valasztas = input("\nVálaszd ki a letöltési módot (1/2/3): ")

    try:
        print("\nVideó metaadatok lekérése...")
        result = subprocess.run(
            ["yt-dlp", "--get-title", "--get-id", url],
            capture_output=True,
            text=True,
            check=True
        )
        cim, video_id = result.stdout.splitlines()
        tisztitott_cim = tisztit_fajlnev(cim)
        print(f"\nVideó címe: {cim}")
    except subprocess.CalledProcessError as e:
        print(f"\nHiba történt a metaadatok lekérése során: {e}")
        return
    
    idobelyeg = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    kimeneti_mappa = f"{tisztitott_cim}_{video_id}_{idobelyeg}"
    os.makedirs(kimeneti_mappa, exist_ok=True)
    print(f"\nLetöltési mappa létrehozva: {kimeneti_mappa}")
    
    if valasztas == "1":
        parancs = f'yt-dlp -f "bestvideo+bestaudio/best" -o "{kimeneti_mappa}/%(title)s.%(ext)s" "{url}"'
        print("\nVideó letöltése hanggal...")
    elif valasztas == "2":
        parancs = f'yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 -o "{kimeneti_mappa}/%(title)s.%(ext)s" "{url}"'
        print("\nCsak a hang letöltése...")
    elif valasztas == "3":
        parancs = f'yt-dlp -f "bestvideo[ext=mp4]" -o "{kimeneti_mappa}/%(title)s.%(ext)s" "{url}"'
        print("\nVideó letöltése hang nélkül...")
    else:
        print("\nÉrvénytelen választás! Próbáld újra.")
        return

    try:
        subprocess.run(parancs, shell=True, check=True)
        print("\nLetöltés sikeres!")
    except subprocess.CalledProcessError as e:
        print(f"\nHiba történt a letöltés során: {e}")
    
    with open(f"{kimeneti_mappa}/letoltesi_naplo.txt", "w", encoding="utf-8") as naplo:
        naplo.write(f"Letöltési URL: {url}\n")
        naplo.write(f"Letöltési mappa: {kimeneti_mappa}\n")
        naplo.write(f"Videó címe: {cim}\n")
        naplo.write(f"Videó azonosítója: {video_id}\n")
        naplo.write(f"Letöltés ideje: {idobelyeg}\n")
    print(f"\nLetöltési információk naplózva: {kimeneti_mappa}/letoltesi_naplo.txt")

if __name__ == "__main__":
    video_letoltes()
