"""
Create Clean Text-Only Vietnamese Patch Package for Mahou Shoujo no Majo Saiban.
Only packages the 24 Naninovel script bundles (no GameAssembly.dll, no UI sprites).
100% Safe, zero crash risk with game engine.
"""
import os
import sys
import json
import shutil
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASE_DIR = os.path.join(GAME_DIR, "release_patch")
PATCH_VIET_HOA_DIR = os.path.join(RELEASE_DIR, "Patch_Viet_Hoa")
STANDALONE_SRC = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")

VERSION = "v1.0.15"
ZIP_NAME = f"Mahou_Shoujo_VietHoa_Patch_{VERSION}.zip"

SCRIPT_BUNDLES = [
    "general-localization-zhhans-scripts-act01_chapter01_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter01_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter02_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter02_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter03_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter03_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter04_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter04_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter05_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter05_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter01_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter01_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter02_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter02_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter03_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter03_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter04_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter04_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter05_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter05_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter06_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-common_assets_all.bundle",
    "general-localization-zhhans-scripts-debug_assets_all.bundle",
    "general-localization-zhhans-scripts-system_assets_all.bundle",
]

def create_text_only_patch():
    print("==================================================")
    print("   UPDATING release_patch/Patch_Viet_Hoa/         ")
    print("==================================================")

    # Ensure Patch_Viet_Hoa dir exists (don't wipe the whole release_patch - keep BAT/README)
    os.makedirs(PATCH_VIET_HOA_DIR, exist_ok=True)

    # Remove stale release_text_patch if it exists
    stale_dir = os.path.join(GAME_DIR, "release_text_patch")
    if os.path.exists(stale_dir):
        shutil.rmtree(stale_dir)
        print("[*] Removed stale 'release_text_patch' folder.")

    # 1. Copy 24 Script Bundles into Patch_Viet_Hoa/
    copied_count = 0
    total_bytes = 0
    for b_name in SCRIPT_BUNDLES:
        src = os.path.join(STANDALONE_SRC, b_name)
        dst = os.path.join(PATCH_VIET_HOA_DIR, b_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            b_size = os.path.getsize(dst)
            total_bytes += b_size
            copied_count += 1
        else:
            print(f"[!] Warning: missing bundle {b_name}")

    print(f"[+] Copied {copied_count} bundles into Patch_Viet_Hoa/ ({total_bytes:,} bytes)")

    # 2. Create ZIP with versioned name — clean up stale ZIPs first
    for f in os.listdir(GAME_DIR):
        if f.endswith(".zip") and "VietHoa" in f and f != ZIP_NAME:
            old_zip = os.path.join(GAME_DIR, f)
            os.remove(old_zip)
            print(f"[*] Removed old ZIP: {f}")

    zip_path = os.path.join(GAME_DIR, ZIP_NAME)
    print(f"[*] Compressing into ZIP: {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, RELEASE_DIR)
                zipf.write(abs_f, rel_f)

    zip_size = os.path.getsize(zip_path)
    print("==================================================")
    print(f"[SUCCESS] Patch {VERSION} created successfully!")
    print(f"  - Release Folder: {RELEASE_DIR}")
    print(f"  - Release ZIP:    {zip_path} ({zip_size:,} bytes / {zip_size/(1024*1024):.2f} MB)")
    print("==================================================")

if __name__ == "__main__":
    create_text_only_patch()
