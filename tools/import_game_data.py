"""
Import translated gameplay data (Clues, Profiles, Notes, Rules, Characters, Authors, Maps) into general-data_assets_all.bundle.
"""
import os
import json
import shutil
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
DATA_BUNDLE = os.path.join(STANDALONE_DIR, "general-data_assets_all.bundle")
BACKUP_DIR = os.path.join(STANDALONE_DIR, "backup_original")
INPUT_DIR = os.path.join(GAME_DIR, "translation", "game_data")

def backup_bundle(bundle_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    b_name = os.path.basename(bundle_path)
    backup_path = os.path.join(BACKUP_DIR, b_name)
    if not os.path.exists(backup_path):
        shutil.copy2(bundle_path, backup_path)
        print(f"[*] Backed up {b_name} to {BACKUP_DIR}")

def set_text_by_locale(locale_list, text, target_locale=2):
    """Update or append localized text for target locale."""
    for item in locale_list:
        if item.get("_locale") == target_locale:
            item["_text"] = text
            return
    locale_list.append({"_locale": target_locale, "_text": text})

def load_json(filename):
    path = os.path.join(INPUT_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def import_game_data():
    if not os.path.exists(DATA_BUNDLE):
        print(f"[!] Data bundle not found: {DATA_BUNDLE}")
        return

    clues_data = load_json("clues.json")
    profiles_data = load_json("profiles.json")
    notes_data = load_json("notes.json")
    rules_data = load_json("rules.json")
    characters_data = load_json("characters.json")
    authors_data = load_json("authors.json")
    maps_data = load_json("maps.json")

    backup_bundle(DATA_BUNDLE)
    env = UnityPy.load(DATA_BUNDLE)
    updated_counts = {}

    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            tree = obj.read_typetree()
            asset_name = tree.get("m_Name", "")
            items = tree.get("_items", [])
            
            if asset_name == "ClueData" and clues_data:
                clue_map = {c["id"]: c for c in clues_data}
                for item in items:
                    cid = item.get("_id")
                    if cid in clue_map:
                        trans = clue_map[cid]
                        vi_name = trans["name"].get("vi") or trans["name"].get("zh")
                        vi_desc = trans["description"].get("vi") or trans["description"].get("zh")
                        item_data = item.get("_item", {})
                        set_text_by_locale(item_data.get("_name", []), vi_name, target_locale=2)
                        set_text_by_locale(item_data.get("_description", []), vi_desc, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["ClueData"] = len(items)

            elif asset_name == "ProfileData" and profiles_data:
                profile_map = {p["id"]: p for p in profiles_data}
                for item in items:
                    pid = item.get("_id")
                    if pid in profile_map:
                        trans = profile_map[pid]
                        vi_desc = trans["description"].get("vi") or trans["description"].get("zh")
                        item_data = item.get("_item", {})
                        set_text_by_locale(item_data.get("_description", []), vi_desc, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["ProfileData"] = len(items)

            elif asset_name == "NoteData" and notes_data:
                note_map = {n["id"]: n for n in notes_data}
                for item in items:
                    nid = item.get("_id")
                    if nid in note_map:
                        trans = note_map[nid]
                        vi_title = trans["title"].get("vi") or trans["title"].get("zh")
                        vi_desc = trans["description"].get("vi") or trans["description"].get("zh")
                        item_data = item.get("_item", {})
                        set_text_by_locale(item_data.get("_title", []), vi_title, target_locale=2)
                        set_text_by_locale(item_data.get("_description", []), vi_desc, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["NoteData"] = len(items)

            elif asset_name == "RuleData" and rules_data:
                rule_map = {r["id"]: r for r in rules_data}
                for item in items:
                    rid = item.get("_id")
                    if rid in rule_map:
                        trans = rule_map[rid]
                        vi_sub = trans["subtitle"].get("vi") or trans["subtitle"].get("zh")
                        vi_desc = trans["description"].get("vi") or trans["description"].get("zh")
                        item_data = item.get("_item", {})
                        set_text_by_locale(item_data.get("_subtitle", []), vi_sub, target_locale=2)
                        set_text_by_locale(item_data.get("_description", []), vi_desc, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["RuleData"] = len(items)

            elif asset_name == "CharacterData" and characters_data:
                char_map = {c["id"]: c for c in characters_data}
                for item in items:
                    cid = item.get("_id")
                    if cid in char_map:
                        trans = char_map[cid]
                        vi_name = trans["name"].get("vi") or trans["name"].get("zh")
                        vi_fam = trans["familyName"].get("vi") or trans["familyName"].get("zh")
                        set_text_by_locale(item.get("_name", []), vi_name, target_locale=2)
                        set_text_by_locale(item.get("_familyName", []), vi_fam, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["CharacterData"] = len(items)

            elif asset_name == "AuthorData" and authors_data:
                author_map = {a["id"]: a for a in authors_data}
                for item in items:
                    aid = item.get("_id")
                    if aid in author_map:
                        trans = author_map[aid]
                        vi_tag = trans["taggedText"].get("vi") or trans["taggedText"].get("zh")
                        set_text_by_locale(item.get("_taggedText", []), vi_tag, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["AuthorData"] = len(items)

            elif asset_name == "MapData" and maps_data:
                map_map = {m["id"]: m for m in maps_data}
                for item in items:
                    mid = item.get("_id")
                    if mid in map_map:
                        trans = map_map[mid]
                        vi_btn = trans["buttonText"].get("vi") or trans["buttonText"].get("zh")
                        item_data = item.get("_item", {})
                        set_text_by_locale(item_data.get("_buttonText", []), vi_btn, target_locale=2)
                obj.save_typetree(tree)
                updated_counts["MapData"] = len(items)

    with open(DATA_BUNDLE, "wb") as f:
        f.write(env.file.save())

    print(f"\n[SUCCESS] Imported Gameplay Data into '{os.path.basename(DATA_BUNDLE)}':")
    for k, v in updated_counts.items():
        print(f"  - {k}: {v} items updated")

if __name__ == "__main__":
    import_game_data()
