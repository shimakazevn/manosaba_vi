"""
Patch Locales, DefaultUI, CharacterNames, and CustomUI in general-localization-zhhans-text_assets_all.bundle.
"""
import os
import shutil
import UnityPy

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
TEXT_BUNDLE = os.path.join(STANDALONE_DIR, "general-localization-zhhans-text_assets_all.bundle")
BACKUP_DIR = os.path.join(STANDALONE_DIR, "backup_original")

VI_LOCALES = """; 日本語 <ja> to 简体中文 <zh-Hans> localization document for 'Locales' managed text document

; English
en-US: English

; 日本語
ja: 日本語

; 한국어
ko: 한국어

; 简体中文
zh-Hans: Tiếng Việt

; 繁體中文
zh-Hant: 繁體中文
"""

VI_DEFAULT_UI = """; 日本語 <ja> to 简体中文 <zh-Hans> localization document for 'DefaultUI' managed text document

; Are you sure you want to quit to the title screen?<br>Any unsaved game progress will be lost.
ControlPanelTitleButton.ConfirmationMessage: Bạn có chắc muốn quay về màn hình chính không?<br>Tiến trình chưa lưu sẽ bị mất.

; Default
GameSettingsFontDropdown.DefaultFontName: Mặc định

; Default
GameSettingsFontSizeDropdown.Default: Mặc định

; Extra Large
GameSettingsFontSizeDropdown.ExtraLarge: Rất lớn

; Large
GameSettingsFontSizeDropdown.Large: Lớn

; Small
GameSettingsFontSizeDropdown.Small: Nhỏ

; Very Low
GameSettingsGraphicsDropdown.GraphicOption1: Rất thấp

; Low
GameSettingsGraphicsDropdown.GraphicOption2: Thấp

; Medium
GameSettingsGraphicsDropdown.GraphicOption3: Trung bình

; High
GameSettingsGraphicsDropdown.GraphicOption4: Cao

; Very High
GameSettingsGraphicsDropdown.GraphicOption5: Rất cao

; Ultra
GameSettingsGraphicsDropdown.GraphicOption6: Tối đa

; Full Screen
GameSettingsScreenModeDropdown.ExclusiveFullScreen: Toàn màn hình

; Full Screen Window
GameSettingsScreenModeDropdown.FullScreenWindow: Cửa sổ không viền

; Maximized Window
GameSettingsScreenModeDropdown.MaximizedWindow: Cửa sổ phóng to

; Windowed
GameSettingsScreenModeDropdown.Windowed: Cửa sổ

; Everything
GameSettingsSkipModeDropdown.Everything: Tất cả

; Read Only
GameSettingsSkipModeDropdown.ReadOnly: Đã đọc

; Empty
GameStateSlot.EmptySlotLabel: Trống

; Are you sure you want to delete save slot?
SaveLoadMenu.DeleteSaveSlotMessage: Bạn có chắc chắn muốn xóa ô lưu này không?

; Are you sure you want to overwrite save slot?
SaveLoadMenu.OverwriteSaveSlotMessage: Bạn có chắc chắn muốn ghi đè lên ô lưu này không?
"""

VI_CHARACTER_NAMES = """; 日本語 <ja> to 简体中文 <zh-Hans> localization document for 'CharacterNames' managed text document

; 紫藤アリサ
Alisa: Shidou Alisa

; 夏目アンアン
AnAn: Natsume AnAn

; 島の大魔女
BigWitch: Đại Phù Thủy Đảo

; 沢渡ココ
Coco: Sawatari Coco

; 紫藤アリサ
CreatureAlisa: Shidou Alisa

; 夏目アンアン
CreatureAnAn: Natsume AnAn

; 沢渡ココ
CreatureCoco: Sawatari Coco

; 桜羽エマ
CreatureEma: Sakuraba Ema

; 遠野ハンナ
CreatureHanna: Touno Hanna

; 二階堂ヒロ
CreatureHiro: Nikaidou Hiro

; 蓮見レイア
CreatureLeia: Hasumi Leia

; 宝生マーゴ
CreatureMargo: Houshou Margo

; 氷上メルル
CreatureMeruru: Hikami Meruru

; 佐伯ミリア
CreatureMiria: Saeki Miria

; 黒部ナノカ
CreatureNanoka: Kurobe Nanoka

; 城ケ崎ノア
CreatureNoah: Jougasaki Noah

; 橘シェリー
CreatureSherry: Tachibana Sherry

; 桜羽エマ
Ema: Sakuraba Ema

; 桜羽エマ？
EmaFake: Sakuraba Ema?

; 少女
Girl: Thiếu nữ

; 遠野ハンナ
Hanna: Touno Hanna

; 二階堂ヒロ
Hiro: Nikaidou Hiro

; 看守
Jailer: Cai ngục

; 看守
JailerB: Cai ngục B

; 看守
JailerC: Cai ngục C

; 蓮見レイア
Leia: Hasumi Leia

; 宝生マーゴ
Margo: Houshou Margo

; 氷上メルル
Meruru: Hikami Meruru

; 佐伯ミリア
Miria: Saeki Miria

; 黒部ナノカ
Nanoka: Kurobe Nanoka

; なれはて
Narehate: Tàn tích

; 城ケ崎ノア
Noah: Jougasaki Noah

; ウサギ
Rabbit: Thỏ

; 橘シェリー
Sherry: Tachibana Sherry

; 野良のなれはて
StrayNarehate: Tàn tích hoang

; ？？？
Unknown: ? ? ?

; ゴクチョー
Warden: Cai ngục trưởng

; 魔女候補１
WitchCandidate1: Ứng viên phù thủy 1

; 魔女候補２
WitchCandidate2: Ứng viên phù thủy 2

; 魔女候補３
WitchCandidate3: Ứng viên phù thủy 3

; 月代ユキ
Yuki: Tsukishiro Yuki
"""

VI_CUSTOM_UI = """; 日本語 <ja> to 简体中文 <zh-Hans> localization document for 'CustomUI' managed text document

; <cspace=-0.125em>アリサ
WitchBook.Map.Alisa: Alisa

; <cspace=-0.125em>アンアン
WitchBook.Map.AnAn: AnAn

; 監房
WitchBook.Map.BasementHallway: Phòng giam

; 地<cspace=-0.1em>精<size=0.8em>の</size>間</cspace>
WitchBook.Map.ChamberGnome: Phòng Địa Tinh

; 火<cspace=-0.1em>精<size=0.8em>の</size>間</cspace>
WitchBook.Map.ChamberSalamander: Phòng Hỏa Tinh

; 水<cspace=-0.1em>精<size=0.8em>の</size>間</cspace>
WitchBook.Map.ChamberUndine: Phòng Thủy Tinh

; <cspace=-0.125em>ココ
WitchBook.Map.Coco: Coco

; 裁判所
WitchBook.Map.Courtroom: Tòa án

; 裁判所前通路
WitchBook.Map.CourtroomHallway: Hành lang trước tòa

; 中庭
WitchBook.Map.Courtyard: Sân trong

; <cspace=-0.125em>エマ
WitchBook.Map.Ema: Ema

; 玄関<cspace=-0.1em>ホール
WitchBook.Map.EntranceHall: Sảnh tiền sảnh

; 花畑方面
WitchBook.Map.FlowerFields: Hướng vườn hoa

; <cspace=-0.1em>ゲストハウス</cspace>前
WitchBook.Map.FrontGuesthouse: Nhà khách

; <cspace=-0.125em>ハンナ
WitchBook.Map.Hanna: Hanna

; <cspace=-0.125em>ヒロ
WitchBook.Map.Hiro: Hiro

; 焼却炉
WitchBook.Map.Incinerator: Lò thiêu

; 医務室
WitchBook.Map.Infirmary: Phòng y tế

; 厨房
WitchBook.Map.Kitchen: Nhà bếp

; 湖方面
WitchBook.Map.Lake: Hướng hồ nước

; <cspace=-0.125em>レイア
WitchBook.Map.Leia: Leia

; 図書室
WitchBook.Map.Library: Thư viện

; <cspace=-0.1em>ラウンジ
WitchBook.Map.Lounge: Phòng chờ

; <cspace=-0.125em>マーゴ
WitchBook.Map.Margo: Margo

; <cspace=-0.125em>メルル
WitchBook.Map.Meruru: Meruru

; 食堂
WitchBook.Map.MessHall: Nhà ăn

; <cspace=-0.125em>ミリア
WitchBook.Map.Miria: Miria

; <cspace=-0.125em>ナノカ
WitchBook.Map.Nanoka: Nanoka

; <cspace=-0.125em>ノア
WitchBook.Map.Noah: Noah

; <cspace=-0.1em>ノア<size=0.8em>の</size>アトリエ
WitchBook.Map.NoahStudio: Xưởng vẽ Noah

; 応接間
WitchBook.Map.Parlor: Phòng tiếp khách

; 牢屋敷前
WitchBook.Map.PrisonEntrance: Cổng nhà tù

; 娯楽室
WitchBook.Map.RecreationRoom: Phòng giải trí

; WWC
WitchBook.Map.Restroom: Nhà vệ sinh

; 2F<cspace=-0.1em>ホール
WitchBook.Map.SecondFloorHallway: Hành lang tầng 2

; <cspace=-0.125em>シェ<space=-0.2em>リー
WitchBook.Map.Sherry: Sherry

; <cspace=-0.1em>シャワールーム
WitchBook.Map.Showers: Phòng tắm

; 懲罰房
WitchBook.Map.SolitaryConfinement: Phòng kỷ luật

; 物置
WitchBook.Map.StorageRoom: Kho chứa đồ

; <cspace=-0.1em>サンルーム
WitchBook.Map.Sunroom: Phòng tắm nắng

; <cspace=-0.2em>？？？
WitchBook.Map.UnknownArea: <cspace=-0.2em><space=4>？？？

; 塀
WitchBook.Map.Wall: Tường bao

; 倉庫
WitchBook.Map.Warehouse: Nhà kho

; 規則
WitchBook.Rule.Rule: Quy tắc
"""

def backup_bundle(bundle_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    b_name = os.path.basename(bundle_path)
    backup_path = os.path.join(BACKUP_DIR, b_name)
    if not os.path.exists(backup_path):
        shutil.copy2(bundle_path, backup_path)
        print(f"[*] Backed up {b_name} to {BACKUP_DIR}")

def patch_ui():
    if not os.path.exists(TEXT_BUNDLE):
        print(f"[!] Text bundle not found: {TEXT_BUNDLE}")
        return

    backup_bundle(TEXT_BUNDLE)
    env = UnityPy.load(TEXT_BUNDLE)
    
    patches = {
        "Locales": VI_LOCALES,
        "DefaultUI": VI_DEFAULT_UI,
        "CharacterNames": VI_CHARACTER_NAMES,
        "CustomUI": VI_CUSTOM_UI
    }
    
    count = 0
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            d = obj.read()
            if d.m_Name in patches:
                d.m_Script = patches[d.m_Name]
                d.save()
                count += 1
                print(f"  [+] Patched {d.m_Name}")
                
    with open(TEXT_BUNDLE, "wb") as f:
        f.write(env.file.save())
        
    print(f"[SUCCESS] Patched {count} UI text assets in '{os.path.basename(TEXT_BUNDLE)}'.")

if __name__ == "__main__":
    patch_ui()
