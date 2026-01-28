from __future__ import annotations
import os
import shutil
import zipfile
from typing import Dict, Any, Optional

import requests

from core.logger import log
from core.system import Paths

def _select_asset_url(release_json: Dict[str, Any], settings: Dict[str, Any], debug_mode: bool) -> Optional[str]:
    assets = release_json.get("assets", []) or []
    suffix = settings.get("github", {}).get("asset_name_suffix", "-full.nupkg")
    exclude = [k.lower() for k in settings.get("github", {}).get("exclude_keywords", [])]

    for asset in assets:
        name = str(asset.get("name", ""))
        lname = name.lower()
        if not lname.endswith(suffix):
            continue
        if any(k in lname for k in exclude):
            continue
        url = asset.get("browser_download_url")
        if url:
            log(f"Asset gefunden: {name}", "DEBUG", debug_mode)
            return url
    return None

def install_or_update_lazer(paths: Paths, settings: Dict[str, Any], debug_mode: bool = True) -> bool:
    """Download latest osu!lazer Windows 'full.nupkg' and extract osu!.exe into paths.game_dir."""
    log("Starte Osu!lazer Download-Prozess...", "INSTALL", debug_mode)
    api_url = settings.get("github", {}).get("latest_release_api")

    try:
        log("Frage GitHub API nach neuestem Release...", "DEBUG", debug_mode)
        r = requests.get(api_url, timeout=30)
        r.raise_for_status()
        data = r.json()

        download_url = _select_asset_url(data, settings, debug_mode)
        if not download_url:
            log("Kein passendes .nupkg Asset gefunden!", "ERROR", debug_mode)
            return False

        log(f"Downloade: {download_url}...", "INFO", debug_mode)
        with requests.get(download_url, stream=True, timeout=120) as rr:
            rr.raise_for_status()
            with open(paths.temp_download, "wb") as f:
                for chunk in rr.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)

        log("Entpacke Dateien...", "DEBUG", debug_mode)
        os.makedirs(paths.extract_path, exist_ok=True)
        with zipfile.ZipFile(paths.temp_download, "r") as zip_ref:
            zip_ref.extractall(paths.extract_path)

        source_folder = None
        for root, _dirs, files in os.walk(paths.extract_path):
            if "osu!.exe" in files:
                source_folder = root
                break

        if not source_folder:
            log("osu!.exe wurde innerhalb der nupkg nicht gefunden!", "ERROR", debug_mode)
            return False

        os.makedirs(paths.game_dir, exist_ok=True)

        log(f"Kopiere Binärdateien nach {paths.game_dir}...", "DEBUG", debug_mode)
        for item in os.listdir(source_folder):
            s = os.path.join(source_folder, item)
            d = os.path.join(paths.game_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        with open(os.path.join(paths.game_dir, "portable.txt"), "w", encoding="utf-8") as f:
            f.write("Lazer portable mode")

        log("Osu!lazer erfolgreich installiert/aktualisiert.", "SUCCESS", debug_mode)
        return True

    except requests.RequestException as e:
        log(f"Netzwerk/HTTP Fehler während der Installation: {e}", "ERROR", debug_mode)
        return False
    except Exception as e:
        log(f"Fehler während der Installation: {e}", "ERROR", debug_mode)
        return False
    finally:
        log("Cleanup der temporären Dateien...", "DEBUG", debug_mode)
        try:
            if os.path.exists(paths.temp_download):
                os.remove(paths.temp_download)
            if os.path.exists(paths.extract_path):
                shutil.rmtree(paths.extract_path)
        except Exception:
            pass

def open_game_folder(paths: Paths) -> None:
    os.makedirs(paths.game_dir, exist_ok=True)
    os.startfile(paths.game_dir)

def delete_game_files(paths: Paths, debug_mode: bool = True) -> None:
    if os.path.exists(paths.game_dir):
        shutil.rmtree(paths.game_dir)
        log("Game Files gelöscht.", "SUCCESS", debug_mode)
