"""
Patch TMP_Dropdown in naninovel-ui_assets_all.bundle so that its default serialized options and texts are '日本語' and 'Tiếng Việt'.
"""
import UnityPy
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
UI_BUNDLE = os.path.join(STANDALONE_DIR, "naninovel-ui_assets_all.bundle")

def patch_dropdown_ui():
    env = UnityPy.load(UI_BUNDLE)
    for obj in env.objects:
        if obj.path_id == -3713666709872201093:
            tree = obj.read_typetree()
            tree["m_Options"] = {
                "m_Options": [
                    {
                        "m_Text": "日本語",
                        "m_Image": {"m_FileID": 0, "m_PathID": 0},
                        "m_Color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}
                    },
                    {
                        "m_Text": "Tiếng Việt",
                        "m_Image": {"m_FileID": 0, "m_PathID": 0},
                        "m_Color": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0}
                    }
                ]
            }
            obj.save_typetree(tree)
            print("[+] Patched TMP_Dropdown m_Options with '日本語' and 'Tiếng Việt'")
        elif obj.path_id == -5810437037574999429:
            tree = obj.read_typetree()
            tree["m_text"] = "Tiếng Việt"
            obj.save_typetree(tree)
            print("[+] Patched CaptionText with 'Tiếng Việt'")
        elif obj.path_id == -4789770608708373893:
            tree = obj.read_typetree()
            tree["m_text"] = "Tiếng Việt"
            obj.save_typetree(tree)
            print("[+] Patched ItemText with 'Tiếng Việt'")

    with open(UI_BUNDLE, "wb") as f:
        f.write(env.file.save())
    print("[SUCCESS] naninovel-ui_assets_all.bundle updated!")

if __name__ == "__main__":
    patch_dropdown_ui()
