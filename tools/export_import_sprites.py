"""
Export and Import 66 localized UI sprites (@ZhHans) in general-sprites_assets_all.bundle.
"""
import os
import shutil
import UnityPy
from PIL import Image

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
SPRITE_BUNDLE = os.path.join(STANDALONE_DIR, "general-sprites_assets_all.bundle")
BACKUP_DIR = os.path.join(STANDALONE_DIR, "backup_original")
OUTPUT_DIR = os.path.join(GAME_DIR, "translation", "sprites")

def backup_bundle(bundle_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    b_name = os.path.basename(bundle_path)
    backup_path = os.path.join(BACKUP_DIR, b_name)
    if not os.path.exists(backup_path):
        shutil.copy2(bundle_path, backup_path)
        print(f"[*] Backed up {b_name} to {BACKUP_DIR}")

def export_sprites():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(SPRITE_BUNDLE):
        print(f"[!] Sprite bundle not found: {SPRITE_BUNDLE}")
        return

    env = UnityPy.load(SPRITE_BUNDLE)
    count = 0
    
    print(f"[*] Scanning {os.path.basename(SPRITE_BUNDLE)} for @ZhHans sprites...")
    for obj in env.objects:
        if obj.type.name == "Sprite":
            d = obj.read()
            name = getattr(d, "m_Name", "")
            if "zh" in name.lower() or "hans" in name.lower():
                img = d.image
                out_path = os.path.join(OUTPUT_DIR, f"{name}.png")
                img.save(out_path, "PNG")
                count += 1
                
    print(f"[SUCCESS] Exported {count} sprites to '{OUTPUT_DIR}'.")

def import_sprites():
    if not os.path.exists(OUTPUT_DIR):
        print(f"[!] Sprites directory '{OUTPUT_DIR}' does not exist.")
        return

    png_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")]
    if not png_files:
        print(f"[!] No PNG files found in '{OUTPUT_DIR}'.")
        return

    backup_bundle(SPRITE_BUNDLE)
    
    env = UnityPy.load(SPRITE_BUNDLE)
    imported_count = 0
    
    # Map of filename without ext -> file path
    sprite_map = {os.path.splitext(f)[0]: os.path.join(OUTPUT_DIR, f) for f in png_files}
    
    for obj in env.objects:
        if obj.type.name == "Sprite":
            d = obj.read()
            name = getattr(d, "m_Name", "")
            if name in sprite_map:
                png_path = sprite_map[name]
                new_img = Image.open(png_path)
                d.image = new_img
                d.save()
                imported_count += 1
                
    with open(SPRITE_BUNDLE, "wb") as f:
        f.write(env.file.save())
        
    print(f"[SUCCESS] Imported {imported_count} updated sprites into '{os.path.basename(SPRITE_BUNDLE)}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "import":
        import_sprites()
    else:
        export_sprites()
