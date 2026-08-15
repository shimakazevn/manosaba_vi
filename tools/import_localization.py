"""
Compile translated JSON dialogues and repack them into the 24 Naninovel localization AssetBundles.
Includes Syntax Validator for <link="Objection_..."> tags and automatic <ruby> cleaner.
"""
import os
import re
import json
import glob
import shutil
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
BACKUP_DIR = os.path.join(STANDALONE_DIR, "backup_original")
INPUT_DIR = os.path.join(GAME_DIR, "translation", "dialogues")

def backup_bundle(bundle_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    b_name = os.path.basename(bundle_path)
    backup_path = os.path.join(BACKUP_DIR, b_name)
    if not os.path.exists(backup_path):
        shutil.copy2(bundle_path, backup_path)
        print(f"[*] Backed up {b_name} to {BACKUP_DIR}")

def clean_ruby_tags(text):
    """Remove <ruby="furigana">kanji</ruby> -> kanji/text."""
    return re.sub(r'<ruby="[^"]*">([^<]+)</ruby>', r'\1', text)

def validate_objection_links(entry, vi_text):
    """
    Ensure all objection links from original text are preserved in Vietnamese translation.
    If a link tag is missing, log a warning and safely restore it.
    """
    orig_links = entry.get("objection_links", [])
    if not orig_links:
        return vi_text
        
    for link_id in orig_links:
        expected_tag = f'<link="{link_id}">'
        if expected_tag not in vi_text:
            print(f"[!] WARNING in [{entry['id']}]: Missing link tag '{expected_tag}'. Attempting auto-fix.")
            # If the user translated without link tag, wrap the translated text in the link tag
            vi_text = f'{expected_tag}{vi_text}</link>'
            
    return vi_text

def format_entry_to_nani(entry):
    """Convert an entry dict to Naninovel localization document block."""
    block_id = entry["id"]
    speaker_tag = entry.get("speaker_tag", "")
    ja_text = entry.get("ja", "")
    zh_text = entry.get("zh", "")
    vi_text = entry.get("vi", "").strip()
    
    # Fallback to Chinese or Japanese if not translated
    target_text = vi_text if vi_text else zh_text
    
    # Process ruby tags and validate links
    if vi_text:
        target_text = clean_ruby_tags(target_text)
        target_text = validate_objection_links(entry, target_text)
    
    lines = [f"# {block_id}"]
    if speaker_tag:
        lines.append(speaker_tag)
    if ja_text:
        for ja_line in ja_text.splitlines():
            lines.append(f"; {ja_line}")
            
    if target_text:
        lines.append(target_text)
        
    return "\n".join(lines)

def import_all():
    manifest_path = os.path.join(INPUT_DIR, "_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"[!] Manifest not found at '{manifest_path}'. Run export_localization.py first.")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    total_bundles = len(manifest)
    total_scripts_updated = 0
    
    print(f"[*] Repacking {total_bundles} script bundles...")

    for b_name, script_list in manifest.items():
        b_path = os.path.join(STANDALONE_DIR, b_name)
        if not os.path.exists(b_path):
            print(f"[!] Bundle not found: {b_path}")
            continue

        backup_bundle(b_path)
        env = UnityPy.load(b_path)
        
        # Build map of script_name -> compiled .nani text
        compiled_scripts = {}
        for s_info in script_list:
            json_file = os.path.join(INPUT_DIR, s_info["file"])
            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8") as f:
                    s_data = json.load(f)
                    
                header = s_data.get("header", "")
                entries = s_data.get("entries", [])
                
                blocks = [header] if header else []
                for entry in entries:
                    blocks.append(format_entry_to_nani(entry))
                    
                compiled_text = "\n\n".join(blocks) + "\n"
                compiled_scripts[s_info["script_name"]] = compiled_text

        # Update TextAssets in UnityPy env
        bundle_updated = 0
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                d = obj.read()
                if d.m_Name in compiled_scripts:
                    d.m_Script = compiled_scripts[d.m_Name]
                    d.save()
                    bundle_updated += 1
                    total_scripts_updated += 1
                    
        with open(b_path, "wb") as f:
            f.write(env.file.save())
            
        print(f"  [+] Repacked {b_name} ({bundle_updated} scripts updated)")

    print(f"\n[SUCCESS] Repacked {total_scripts_updated} scripts across {total_bundles} bundles.")

if __name__ == "__main__":
    import_all()
