"""
Export Naninovel scripts from Unity AssetBundles to structured JSON and Nani files for translation.
"""
import os
import io
import re
import json
import glob
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
OUTPUT_DIR = os.path.join(GAME_DIR, "translation", "dialogues")

def parse_nani_doc(text):
    """
    Parse a Naninovel localization document into structured blocks.
    Each block consists of:
    - id: Label / ID (e.g. 0101Adv29_Ema001)
    - speaker_tag: raw comment line with speaker if any (e.g. '; > Ema: |#0101Adv29_Ema001|')
    - ja_text: raw comment line with original Japanese text
    - zh_text: translated Chinese text
    - objection_links: list of objection link ids
    """
    blocks = []
    current_block = []
    
    # Split by double newline or blank lines between blocks
    lines = text.splitlines()
    i = 0
    header_comment = ""
    
    while i < len(lines):
        line = lines[i].rstrip('\r\n')
        if i == 0 and line.startswith(';'):
            header_comment = line
            i += 1
            continue
            
        if line.startswith('#'):
            # Start of a new block
            block_id = line[1:].strip()
            speaker_tag = ""
            ja_lines = []
            zh_lines = []
            
            i += 1
            # Collect lines until next '#' or end of file
            while i < len(lines) and not lines[i].strip().startswith('#'):
                cur_line = lines[i].rstrip('\r\n')
                if cur_line.startswith('; >') or cur_line.startswith('; @'):
                    speaker_tag = cur_line
                elif cur_line.startswith(';'):
                    # Japanese source line
                    ja_lines.append(cur_line[1:].strip())
                elif cur_line.strip():
                    # Translated line
                    zh_lines.append(cur_line.strip())
                i += 1
                
            ja_text = "\n".join(ja_lines)
            zh_text = "\n".join(zh_lines)
            
            # Extract objection links
            objection_links = re.findall(r'<link="([^"]+)">', zh_text or ja_text)
            
            blocks.append({
                "id": block_id,
                "speaker_tag": speaker_tag,
                "ja": ja_text,
                "zh": zh_text,
                "vi": "",  # To be filled by translator
                "objection_links": objection_links
            })
        else:
            i += 1
            
    return header_comment, blocks

def export_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    bundles = sorted(glob.glob(os.path.join(STANDALONE_DIR, "general-localization-zhhans-scripts-*.bundle")))
    
    total_scripts = 0
    total_entries = 0
    manifest = {}
    
    print(f"[*] Found {len(bundles)} script bundles.")
    for b_path in bundles:
        b_name = os.path.basename(b_path)
        env = UnityPy.load(b_path)
        
        bundle_manifest = []
        
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                d = obj.read()
                script_name = d.m_Name
                script_text = d.m_Script
                
                header, blocks = parse_nani_doc(script_text)
                
                out_filename = f"{script_name}.json"
                out_filepath = os.path.join(OUTPUT_DIR, out_filename)
                
                script_data = {
                    "bundle": b_name,
                    "script_name": script_name,
                    "header": header,
                    "total_entries": len(blocks),
                    "entries": blocks
                }
                
                with open(out_filepath, "w", encoding="utf-8") as f:
                    json.dump(script_data, f, ensure_ascii=False, indent=2)
                    
                bundle_manifest.append({
                    "script_name": script_name,
                    "file": out_filename,
                    "entries_count": len(blocks)
                })
                
                total_scripts += 1
                total_entries += len(blocks)
                
        manifest[b_name] = bundle_manifest
        print(f"  [+] Processed {b_name} ({len(bundle_manifest)} scripts)")
        
    manifest_path = os.path.join(OUTPUT_DIR, "_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    print(f"\n[SUCCESS] Exported {total_scripts} Naninovel scripts ({total_entries} total dialogue entries) to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    export_all()
