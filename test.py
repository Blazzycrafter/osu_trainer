import os
import requests
import zipfile
import shutil

# Pfade definieren
BASE_DIR = os.getcwd()
TEMP_DOWNLOAD = os.path.join(BASE_DIR, "osu_temp.nupkg")
EXTRACT_PATH = os.path.join(BASE_DIR, "osu_extract")
TARGET_DIR = os.path.join(BASE_DIR, "Osu", "template")


def get_portable_lazer():
    # 1. API Abfrage (wie in deinem Test)
    url = "https://api.github.com/repos/ppy/osu/releases/latest"
    print("Suche nach portablem Release (.nupkg)...")

    response = requests.get(url)
    data = response.json()
    assets = data.get("assets", [])

    # Suche die 'full.nupkg' für Windows (nicht die delta oder linux/osx Varianten)
    download_url = None
    for asset in assets:
        name = asset["name"]
        if name.endswith("-full.nupkg") and "linux" not in name and "osx" not in name:
            download_url = asset["browser_download_url"]
            break

    if not download_url:
        print("Kein passendes .nupkg Asset gefunden!")
        return

    # 2. Download
    print(f"Downloade: {download_url}...")
    with requests.get(download_url, stream=True) as r:
        with open(TEMP_DOWNLOAD, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # 3. Entpacken
    print("Entpacke Dateien...")
    with zipfile.ZipFile(TEMP_DOWNLOAD, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_PATH)

    # 4. Spieldateien isolieren
    # In .nupkg liegen die ausführbaren Dateien meist unter lib/net6.0/
    # Wir suchen den Ordner, der die 'osu!.exe' enthält
    source_folder = None
    for root, dirs, files in os.walk(EXTRACT_PATH):
        if "osu!.exe" in files:
            source_folder = root
            break

    if source_folder:
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)

        # Alles aus dem Source-Ordner in unser Template kopieren
        for item in os.listdir(source_folder):
            s = os.path.join(source_folder, item)
            d = os.path.join(TARGET_DIR, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        # Portable-Modus erzwingen
        with open(os.path.join(TARGET_DIR, "portable.txt"), "w") as f:
            f.write("Lazer portable mode")

        print(f"Erfolg! Portable Instanz bereit in: {TARGET_DIR}")
    else:
        print("osu!.exe wurde innerhalb der nupkg nicht gefunden!")

    # 5. Cleanup
    print("Aufräumen...")
    if os.path.exists(TEMP_DOWNLOAD): os.remove(TEMP_DOWNLOAD)
    if os.path.exists(EXTRACT_PATH): shutil.rmtree(EXTRACT_PATH)


if __name__ == "__main__":
    get_portable_lazer()