from __future__ import annotations
import os
import platform
from dataclasses import dataclass
from typing import Dict, Any

_DEFAULT_SETTINGS: Dict[str, Any] = {
    "debug_mode": True,
    "paths": {
        "work_root": ".",
        "osu_root_dirname": "Osu",
        "backups_dirname": "Backups",
        "backup_filename": "osu_main_system_backup.zip",
        "temp_download_filename": "osu_temp.nupkg",
        "extract_dirname": "osu_extract",
    },
    "github": {
        "latest_release_api": "https://api.github.com/repos/ppy/osu/releases/latest",
        "asset_name_suffix": "-full.nupkg",
        "exclude_keywords": [
            "linux",
            "osx",
            "mac",
            "arm",
        ],
    },
}

@dataclass(frozen=True)
class Paths:
    base_dir: str
    appdata_osu: str

    osu_base_dir: str
    game_dir: str
    template_dir: str

    backups_dir: str
    backup_file: str

    temp_download: str
    extract_path: str

def require_windows() -> None:
    if platform.system() != "Windows":
        raise SystemExit("Nur Windows.")

def load_settings(settings_path: str) -> Dict[str, Any]:
    import json
    if not os.path.exists(settings_path):
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(_DEFAULT_SETTINGS, f, indent=2, ensure_ascii=False)
    with open(settings_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_paths(settings: Dict[str, Any]) -> Paths:
    """Build paths based on current working directory (portable usage)."""
    work_root = settings.get("paths", {}).get("work_root", ".")
    base_dir = os.path.abspath(os.path.join(os.getcwd(), work_root))

    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise RuntimeError("APPDATA env var not found. Are you on Windows?")
    appdata_osu = os.path.join(appdata, "osu")

    osu_root = os.path.join(base_dir, settings["paths"].get("osu_root_dirname", "Osu"))
    game_dir = os.path.join(osu_root, "game")
    template_dir = os.path.join(osu_root, "template")

    backups_dir = os.path.join(base_dir, settings["paths"].get("backups_dirname", "Backups"))
    backup_file = os.path.join(backups_dir, settings["paths"].get("backup_filename", "osu_main_system_backup.zip"))

    temp_download = os.path.join(base_dir, settings["paths"].get("temp_download_filename", "osu_temp.nupkg"))
    extract_path = os.path.join(base_dir, settings["paths"].get("extract_dirname", "osu_extract"))

    return Paths(
        base_dir=base_dir,
        appdata_osu=appdata_osu,
        osu_base_dir=osu_root,
        game_dir=game_dir,
        template_dir=template_dir,
        backups_dir=backups_dir,
        backup_file=backup_file,
        temp_download=temp_download,
        extract_path=extract_path,
    )
