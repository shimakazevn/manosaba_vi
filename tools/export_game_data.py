"""
Export gameplay data (Clues, Profiles, Notes, Rules, Characters, Authors, Maps) from general-data_assets_all.bundle.
"""
import os
import json
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
DATA_BUNDLE = os.path.join(STANDALONE_DIR, "general-data_assets_all.bundle")
OUTPUT_DIR = os.path.join(GAME_DIR, "translation", "game_data")

LOCALE_MAP = {
    0: "ja",
    1: "en",
    2: "zh-Hans",
    3: "zh-Hant"
}

def get_text_by_locale(locale_list, target_locale=2):
    for item in locale_list:
        if item.get("_locale") == target_locale:
            return item.get("_text", "")
    return ""

def export_game_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(DATA_BUNDLE):
        print(f"[!] Data bundle not found: {DATA_BUNDLE}")
        return

    env = UnityPy.load(DATA_BUNDLE)
    print(f"[*] Loaded {os.path.basename(DATA_BUNDLE)}")
    
    extracted_counts = {}

    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            tree = obj.read_typetree()
            asset_name = tree.get("m_Name", "")
            items = tree.get("_items", [])
            
            if asset_name == "ClueData":
                clues = []
                for item in items:
                    cid = item.get("_id")
                    item_data = item.get("_item", {})
                    names = item_data.get("_name", [])
                    descs = item_data.get("_description", [])
                    
                    clues.append({
                        "id": cid,
                        "version": item.get("_version", 1),
                        "name": {
                            "ja": get_text_by_locale(names, 0),
                            "zh": get_text_by_locale(names, 2),
                            "vi": ""
                        },
                        "description": {
                            "ja": get_text_by_locale(descs, 0),
                            "zh": get_text_by_locale(descs, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "clues.json"), "w", encoding="utf-8") as f:
                    json.dump(clues, f, ensure_ascii=False, indent=2)
                extracted_counts["ClueData"] = len(clues)

            elif asset_name == "ProfileData":
                profiles = []
                for item in items:
                    pid = item.get("_id")
                    item_data = item.get("_item", {})
                    descs = item_data.get("_description", [])
                    
                    profiles.append({
                        "id": pid,
                        "version": item.get("_version", 1),
                        "description": {
                            "ja": get_text_by_locale(descs, 0),
                            "zh": get_text_by_locale(descs, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "profiles.json"), "w", encoding="utf-8") as f:
                    json.dump(profiles, f, ensure_ascii=False, indent=2)
                extracted_counts["ProfileData"] = len(profiles)

            elif asset_name == "NoteData":
                notes = []
                for item in items:
                    nid = item.get("_id")
                    item_data = item.get("_item", {})
                    titles = item_data.get("_title", [])
                    descs = item_data.get("_description", [])
                    
                    notes.append({
                        "id": nid,
                        "version": item.get("_version", 1),
                        "title": {
                            "ja": get_text_by_locale(titles, 0),
                            "zh": get_text_by_locale(titles, 2),
                            "vi": ""
                        },
                        "description": {
                            "ja": get_text_by_locale(descs, 0),
                            "zh": get_text_by_locale(descs, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "notes.json"), "w", encoding="utf-8") as f:
                    json.dump(notes, f, ensure_ascii=False, indent=2)
                extracted_counts["NoteData"] = len(notes)

            elif asset_name == "RuleData":
                rules = []
                for item in items:
                    rid = item.get("_id")
                    item_data = item.get("_item", {})
                    subtitles = item_data.get("_subtitle", [])
                    descs = item_data.get("_description", [])
                    
                    rules.append({
                        "id": rid,
                        "numbering": item_data.get("_numbering", ""),
                        "subtitle": {
                            "ja": get_text_by_locale(subtitles, 0),
                            "zh": get_text_by_locale(subtitles, 2),
                            "vi": ""
                        },
                        "description": {
                            "ja": get_text_by_locale(descs, 0),
                            "zh": get_text_by_locale(descs, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "rules.json"), "w", encoding="utf-8") as f:
                    json.dump(rules, f, ensure_ascii=False, indent=2)
                extracted_counts["RuleData"] = len(rules)

            elif asset_name == "CharacterData":
                characters = []
                for item in items:
                    cid = item.get("_id")
                    names = item.get("_name", [])
                    families = item.get("_familyName", [])
                    
                    characters.append({
                        "id": cid,
                        "name": {
                            "ja": get_text_by_locale(names, 0),
                            "zh": get_text_by_locale(names, 2),
                            "vi": ""
                        },
                        "familyName": {
                            "ja": get_text_by_locale(families, 0),
                            "zh": get_text_by_locale(families, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "characters.json"), "w", encoding="utf-8") as f:
                    json.dump(characters, f, ensure_ascii=False, indent=2)
                extracted_counts["CharacterData"] = len(characters)

            elif asset_name == "AuthorData":
                authors = []
                for item in items:
                    aid = item.get("_id")
                    tagged = item.get("_taggedText", [])
                    
                    authors.append({
                        "id": aid,
                        "taggedText": {
                            "ja": get_text_by_locale(tagged, 0),
                            "zh": get_text_by_locale(tagged, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "authors.json"), "w", encoding="utf-8") as f:
                    json.dump(authors, f, ensure_ascii=False, indent=2)
                extracted_counts["AuthorData"] = len(authors)

            elif asset_name == "MapData":
                maps = []
                for item in items:
                    mid = item.get("_id")
                    item_data = item.get("_item", {})
                    buttons = item_data.get("_buttonText", [])
                    
                    maps.append({
                        "id": mid,
                        "buttonText": {
                            "ja": get_text_by_locale(buttons, 0),
                            "zh": get_text_by_locale(buttons, 2),
                            "vi": ""
                        }
                    })
                with open(os.path.join(OUTPUT_DIR, "maps.json"), "w", encoding="utf-8") as f:
                    json.dump(maps, f, ensure_ascii=False, indent=2)
                extracted_counts["MapData"] = len(maps)

    print("\n[SUCCESS] Extracted Gameplay Datasets:")
    for k, v in extracted_counts.items():
        print(f"  - {k}: {v} items")

if __name__ == "__main__":
    export_game_data()
