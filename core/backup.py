from __future__ import annotations
import os
import shutil
import zipfile

from .logger import log
from .system import Paths

def create_backup(paths: Paths, debug_mode: bool = True) -> bool:
    """Zips %APPDATA%\osu into backups_dir/backup_file."""
    if not os.path.exists(paths.appdata_osu):
        log("Kein Osu-AppData vorhanden, kein Backup nötig.", "DEBUG", debug_mode)
        return True

    os.makedirs(paths.backups_dir, exist_ok=True)
    log("Erstelle System-Backup...", "INFO", debug_mode)
    try:
        with zipfile.ZipFile(paths.backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _dirs, files in os.walk(paths.appdata_osu):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, paths.appdata_osu)
                    zipf.write(full_path, rel_path)
        log("Backup erfolgreich.", "SUCCESS", debug_mode)
        return True
    except Exception as e:
        log(f"Backup fehlgeschlagen: {e}", "ERROR", debug_mode)
        return False

def restore_backup(paths: Paths, debug_mode: bool = True) -> None:
    """Restores %APPDATA%\osu from the backup zip."""
    if not os.path.exists(paths.backup_file):
        log("Kein Backup-File gefunden!", "ERROR", debug_mode)
        return

    if os.path.exists(paths.appdata_osu):
        shutil.rmtree(paths.appdata_osu)

    log("Stelle Original-System wieder her...", "INFO", debug_mode)
    try:
        os.makedirs(paths.appdata_osu, exist_ok=True)
        with zipfile.ZipFile(paths.backup_file, "r") as zipf:
            zipf.extractall(paths.appdata_osu)
        log("System erfolgreich wiederhergestellt.", "SUCCESS", debug_mode)
    except Exception as e:
        log(f"Fehler beim Restore: {e}", "ERROR", debug_mode)
