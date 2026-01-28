from __future__ import annotations
import os
import sys

from core.system import require_windows, load_settings, build_paths
from core.logger import log
from core.backup import restore_backup

from modules.osu_manager import install_or_update_lazer, open_game_folder, delete_game_files
from modules.template_manager import create_new_template, edit_template, delete_template

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def menu_manage_osu(paths, settings, debug_mode: bool) -> None:
    while True:
        _clear()
        print("=" * 40)
        print("      MANAGE OSU (BINARIES)")
        print("=" * 40)
        exe_ok = os.path.exists(os.path.join(paths.game_dir, "osu!.exe"))
        print(f"Game Folder: {'[OK]' if exe_ok else '[NOT INSTALLED]'}")
        print("-" * 40)
        print("1. Install / Update Osu!lazer (Download from GitHub)")
        print("2. Open Game Folder")
        print("3. Delete Game Files")
        print("4. Back to Main Menu")

        choice = input("\nOsu Selection > ").strip()
        if choice == "1":
            install_or_update_lazer(paths, settings, debug_mode)
            input("\n[Enter]...")
        elif choice == "2":
            open_game_folder(paths)
        elif choice == "3":
            delete_game_files(paths, debug_mode)
            input("\n[Enter]...")
        elif choice == "4":
            break

def menu_manage_template(paths, debug_mode: bool) -> None:
    while True:
        _clear()
        print("=" * 40)
        print("      MANAGE TEMPLATE (DATA)")
        print("=" * 40)
        print(f"Status: {'[VORHANDEN]' if os.path.exists(paths.template_dir) else '[FEHLT]'}")
        print("-" * 40)
        print("1. Create New Template (Overwrites existing)")
        print("2. Edit Existing Template")
        print("3. Delete Template")
        print("4. Back to Main Menu")

        choice = input("\nTemplate Selection > ").strip()
        if choice == "1":
            create_new_template(paths, debug_mode)
            input("\n[Enter]...")
        elif choice == "2":
            edit_template(paths, debug_mode)
            input("\n[Enter]...")
        elif choice == "3":
            delete_template(paths, debug_mode)
            input("\n[Enter]...")
        elif choice == "4":
            break

def main() -> None:
    require_windows()

    settings = load_settings(os.path.join(os.getcwd(), "settings.json"))
    debug_mode = bool(settings.get("debug_mode", True))
    paths = build_paths(settings)

    while True:
        _clear()
        print("=" * 40)
        print("   OSU! TRAINING TOOL v1.2 (modular)")
        print("=" * 40)
        print("1. START TRAINING SESSION")
        print("2. Manage Template (Data/AppData)")
        print("3. Manage Osu (Installation/Exe)")
        print("4. Emergency Restore")
        print("0. Exit")

        choice = input("\nMain Selection > ").strip()
        if choice == "1":
            log("TODO: Backup -> Load Template -> Import Maps -> Run Osu -> Restore", "INFO", debug_mode)
            input("\n[Enter]...")
        elif choice == "2":
            menu_manage_template(paths, debug_mode)
        elif choice == "3":
            menu_manage_osu(paths, settings, debug_mode)
        elif choice == "4":
            restore_backup(paths, debug_mode)
            input("\n[Enter]...")
        elif choice == "0":
            sys.exit(0)

if __name__ == "__main__":
    main()
