"""
Complete, robust Sprite Atlas Patcher for general-sprites_assets_all.bundle.
Pastes translated images directly onto Texture2D atlases using SpriteAtlas metadata.
Supports both @ZhHans and @Ja sprites!
"""
import os
import sys
import io
import UnityPy
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GAME_DIR = r"e:\MGWT.v1.1.2"
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
SPRITE_BUNDLE = os.path.join(STANDALONE_DIR, "general-sprites_assets_all.bundle")
TRANSLATION_SPRITES_DIR = os.path.join(GAME_DIR, "translation", "sprites")

def patch_all_atlases():
    # 1. Collect all translation PNGs
    png_files = [f for f in os.listdir(TRANSLATION_SPRITES_DIR) if f.endswith(".png")]
    trans_map = {}
    for f in png_files:
        name_no_ext = os.path.splitext(f)[0]
        base_name = name_no_ext.replace("@ZhHans", "").replace("@Ja", "")
        img_path = os.path.join(TRANSLATION_SPRITES_DIR, f)
        trans_map[name_no_ext] = img_path
        trans_map[base_name] = img_path

    print(f"Loaded {len(png_files)} translated images.")

    # 2. Load bundle
    env = UnityPy.load(SPRITE_BUNDLE)

    # Map texture PathID -> UnityPy object
    tex_objs = {}
    tex_images = {}
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            tex_objs[obj.path_id] = obj
            # Read image and convert to RGBA
            tex_images[obj.path_id] = obj.read().image.convert("RGBA")

    print(f"Loaded {len(tex_objs)} Atlas Textures.")

    patched_sprites_count = 0
    modified_textures = set()

    # 3. Iterate over SpriteAtlases
    for obj in env.objects:
        if obj.type.name == "SpriteAtlas":
            tree = obj.read_typetree()
            atlas_name = tree.get("m_Name", "Unknown")
            sprite_names = tree.get("m_PackedSpriteNamesToIndex", [])
            render_data_list = tree.get("m_RenderDataMap", [])

            print(f"\nProcessing SpriteAtlas '{atlas_name}' ({len(sprite_names)} sprites)...")

            for idx, item in enumerate(render_data_list):
                if idx >= len(sprite_names):
                    break
                sname = sprite_names[idx]
                
                # item is either (key, value) or dict with 'texture'
                val = item[1] if isinstance(item, (list, tuple)) else item
                tex_ptr = val.get("texture", {})
                tex_pid = tex_ptr.get("m_PathID")
                tex_rect = val.get("textureRect", {})

                if not tex_pid or tex_pid not in tex_images or not tex_rect:
                    continue

                rx = int(tex_rect.get("x", 0))
                ry = int(tex_rect.get("y", 0))
                rw = int(tex_rect.get("width", 0))
                rh = int(tex_rect.get("height", 0))

                # Check if we have a replacement for sname
                base_name = sname.replace("@ZhHans", "").replace("@Ja", "")
                target_png = trans_map.get(sname) or trans_map.get(base_name)

                if target_png and os.path.exists(target_png):
                    # Paste into atlas texture
                    atlas_img = tex_images[tex_pid]
                    atlas_w, atlas_h = atlas_img.size

                    # Unity texture coordinates: (0,0) is bottom-left, PIL is top-left
                    pil_y = atlas_h - (ry + rh)

                    sprite_img = Image.open(target_png).convert("RGBA")
                    if sprite_img.size != (rw, rh):
                        sprite_img = sprite_img.resize((rw, rh), Image.LANCZOS)

                    # Paste with alpha
                    atlas_img.paste(sprite_img, (rx, pil_y), sprite_img)
                    modified_textures.add(tex_pid)
                    patched_sprites_count += 1
                    print(f"  [+] Patched '{sname}' onto {tex_objs[tex_pid].read().m_Name} at ({rx}, {ry}, {rw}x{rh})")

    # 4. Save modified textures back to bundle
    print(f"\nSaving {len(modified_textures)} modified textures...")
    for tex_pid in modified_textures:
        tobj = tex_objs[tex_pid]
        tdata = tobj.read()
        tdata.image = tex_images[tex_pid]
        tdata.save()
        print(f"  [SAVED] {tdata.m_Name}")

    with open(SPRITE_BUNDLE, "wb") as f:
        f.write(env.file.save())

    print(f"\n[SUCCESS] Successfully patched {patched_sprites_count} sprites across {len(modified_textures)} atlases in {os.path.basename(SPRITE_BUNDLE)}!")

if __name__ == "__main__":
    patch_all_atlases()
