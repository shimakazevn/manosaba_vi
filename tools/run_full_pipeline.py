"""
Master Pipeline Script for Mahou Shoujo no Majo Saiban Vietnamese Localization.
Runs all build steps cleanly in isolated subprocesses with UTF-8 encoding.
Usage:
  python tools/run_full_pipeline.py export    # Export all dialogues, game data, and sprites
  python tools/run_full_pipeline.py build     # Build / pack all translations into the game
"""
import os
import sys
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(GAME_DIR, "tools")

def run_step(script_name, *args):
    script_path = os.path.join(TOOLS_DIR, script_name)
    cmd = [sys.executable, script_path] + list(args)
    print(f"\n[>>>] Running: {script_name} {' '.join(args)}...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    res = subprocess.run(cmd, cwd=GAME_DIR, env=env)
    if res.returncode != 0:
        print(f"[!] Step {script_name} failed with returncode {res.returncode}")
        return False
    return True

def run_build():
    print("==================================================")
    print("      STARTING FULL VIETNAMESE LOCALIZATION BUILD ")
    print("==================================================")
    
    steps = [
        ("patch_ui_locales.py", []),
        ("patch_options_menu.py", []),
        ("patch_all_locales_aliases.py", []),
        ("patch_dropdown_ui_direct.py", []),
        ("patch_dll_all_chinese.py", []),
        ("patch_dropdown_hook.py", []),
        ("render_vietnamese_sprites.py", []),
        ("patch_all_atlases.py", []),
        ("import_localization.py", []),
        ("import_game_data.py", []),
    ]
    
    for script, args in steps:
        success = run_step(script, *args)
        if not success:
            print(f"\n[FAIL] Build aborted at step: {script}")
            return
            
    print("\n==================================================")
    print(" [SUCCESS] Full game build and localization completed cleanly!")
    print("==================================================")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tools/run_full_pipeline.py export")
        print("  python tools/run_full_pipeline.py build")
        return

    cmd = sys.argv[1].lower()
    if cmd == "export":
        print("[*] Running full export...")
        run_step("export_localization.py")
        run_step("export_game_data.py")
        run_step("export_import_sprites.py")
    elif cmd == "build":
        run_build()
    else:
        print(f"[!] Unknown command: {cmd}")

if __name__ == "__main__":
    main()
