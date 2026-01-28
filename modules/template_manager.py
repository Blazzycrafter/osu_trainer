from __future__ import annotations
import os
import shutil
import subprocess

from core.logger import log
from core.system import Paths
from core.backup import create_backup, restore_backup

def _osu_exe(paths: Paths) -> str:
    return os.path.join(paths.game_dir, "osu!.exe")

def create_new_template(paths: Paths, debug_mode: bool = True) -> None:
    log("=== NEW TEMPLATE WORKFLOW ===", "TEMPLATE", debug_mode)
    if not create_backup(paths, debug_mode):
        return

    if os.path.exists(paths.appdata_osu):
        shutil.rmtree(paths.appdata_osu)
    os.makedirs(paths.appdata_osu, exist_ok=True)

    exe_path = _osu_exe(paths)
    log("Starte Osu zur Einrichtung...", "INFO", debug_mode)
    if not os.path.exists(exe_path):
        log("Keine Osu-Exe gefunden! Bitte erst unter 'Manage Osu' installieren.", "ERROR", debug_mode)
    else:
        subprocess.Popen([exe_path])

    input("\nSobald Osu fertig eingerichtet und geschlossen ist: [ENTER]...")

    if os.path.exists(paths.template_dir):
        shutil.rmtree(paths.template_dir)
    os.makedirs(os.path.dirname(paths.template_dir), exist_ok=True)
    shutil.copytree(paths.appdata_osu, paths.template_dir)

    log("Template gespeichert.", "SUCCESS", debug_mode)
    restore_backup(paths, debug_mode)

def edit_template(paths: Paths, debug_mode: bool = True) -> None:
    log("=== EDIT TEMPLATE WORKFLOW ===", "EDIT", debug_mode)
    if not os.path.exists(paths.template_dir):
        log("Kein Template vorhanden!", "ERROR", debug_mode)
        return
    if not create_backup(paths, debug_mode):
        return

    if os.path.exists(paths.appdata_osu):
        shutil.rmtree(paths.appdata_osu)
    shutil.copytree(paths.template_dir, paths.appdata_osu)

    exe_path = _osu_exe(paths)
    log("Öffne Osu zur Bearbeitung...", "INFO", debug_mode)
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])

    input("\nÄnderungen fertig? Osu schließen und [ENTER] drücken...")

    if os.path.exists(paths.template_dir):
        shutil.rmtree(paths.template_dir)
    shutil.copytree(paths.appdata_osu, paths.template_dir)

    log("Änderungen am Template gesichert.", "SUCCESS", debug_mode)
    restore_backup(paths, debug_mode)

def delete_template(paths: Paths, debug_mode: bool = True) -> None:
    if os.path.exists(paths.template_dir):
        shutil.rmtree(paths.template_dir)
        log("Template gelöscht.", "SUCCESS", debug_mode)
