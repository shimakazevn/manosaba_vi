"""
Add all possible aliases of Locales TextAsset to ensure Naninovel ITextManager finds it under any category name.
"""
import os
import sys
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")

ZH_BUNDLE = os.path.join(STANDALONE_DIR, "general-localization-zhhans-text_assets_all.bundle")
MANAGED_BUNDLE = os.path.join(STANDALONE_DIR, "general-managedtext_assets_all.bundle")

LOCALES_TEXT = """en-US: English
ja: 日本語
ko: 한국어
zh-Hans: Tiếng Việt
zh-Hant: 繁體中文
zh-CN: Tiếng Việt
zh: Tiếng Việt
Chinese (Simplified): Tiếng Việt
Simplified Chinese: Tiếng Việt
Japanese: 日本語
English: English
"""

DEFAULT_UI_EXTRA = """
GameSettingsLanguageDropdown.zh-Hans: Tiếng Việt
GameSettingsLanguageDropdown.zh-CN: Tiếng Việt
GameSettingsLanguageDropdown.zh: Tiếng Việt
GameSettingsLanguageDropdown.Chinese: Tiếng Việt
GameSettingsLanguageDropdown.SimplifiedChinese: Tiếng Việt
GameSettingsLanguageDropdown.ja: 日本語
GameSettingsLanguageDropdown.Japanese: 日本語
GameSettingsLanguageDropdown.en-US: English
GameSettingsLanguageDropdown.English: English
zh-Hans: Tiếng Việt
zh-CN: Tiếng Việt
zh: Tiếng Việt
ja: 日本語
"""

def patch_bundle(bpath, is_zh=False):
    env = UnityPy.load(bpath)
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            d = obj.read()
            if d.m_Name == "Locales":
                if is_zh:
                    d.m_Script = "; 日本語 <ja> to Tiếng Việt <zh-Hans> localization document for 'Locales' managed text document\n\n" + LOCALES_TEXT
                else:
                    d.m_Script = LOCALES_TEXT
                d.save()
                print(f"  [+] Updated Locales TextAsset in {os.path.basename(bpath)}")
            elif d.m_Name == "DefaultUI":
                if "GameSettingsLanguageDropdown" not in d.m_Script:
                    d.m_Script = d.m_Script + DEFAULT_UI_EXTRA
                    d.save()
                    print(f"  [+] Added LanguageDropdown keys to DefaultUI in {os.path.basename(bpath)}")
            elif d.m_Name == "CustomUI":
                if "GameSettingsLanguageDropdown" not in d.m_Script:
                    d.m_Script = d.m_Script + DEFAULT_UI_EXTRA
                    d.save()
                    print(f"  [+] Added LanguageDropdown keys to CustomUI in {os.path.basename(bpath)}")

    with open(bpath, "wb") as f:
        f.write(env.file.save())
    print(f"[SUCCESS] Patched {os.path.basename(bpath)}")

if __name__ == "__main__":
    patch_bundle(MANAGED_BUNDLE, is_zh=False)
    patch_bundle(ZH_BUNDLE, is_zh=True)
