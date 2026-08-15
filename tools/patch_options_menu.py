"""
Patch Options Menu, Dialogs, and Language Dropdown directly in naninovel-ui_assets_all.bundle and general-managedtext_assets_all.bundle.
"""
import os
import sys
import io
import shutil
import UnityPy

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDALONE_DIR = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
UI_BUNDLE = os.path.join(STANDALONE_DIR, "naninovel-ui_assets_all.bundle")
MANAGEDTEXT_BUNDLE = os.path.join(STANDALONE_DIR, "general-managedtext_assets_all.bundle")
BACKUP_DIR = os.path.join(STANDALONE_DIR, "backup_original")

def backup_bundle(bundle_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    b_name = os.path.basename(bundle_path)
    backup_path = os.path.join(BACKUP_DIR, b_name)
    if not os.path.exists(backup_path):
        shutil.copy2(bundle_path, backup_path)
        print(f"[*] Backed up {b_name} to {BACKUP_DIR}")

UI_TRANSLATIONS = {
    "メッセージの表示速度": "Tốc độ hiển thị chữ",
    "オートモード時の待ち時間": "Thời gian chờ tự động đọc",
    "スキップモード": "Chế độ tua nhanh (Skip)",
    "すべて": "Tất cả",
    "既読のみ": "Đã đọc",
    "重要選択肢のヒント表示": "Hiển thị gợi ý lựa chọn quan trọng",
    "オフ": "Tắt",
    "オン": "Bật",
    "言語 / Language": "Ngôn ngữ / Language",
    "初期設定に戻す": "Khôi phục mặc định",
    "画面モード": "Chế độ màn hình",
    "フルスクリーン": "Toàn màn hình",
    "ウィンドウ": "Cửa sổ",
    "画面解像度": "Độ phân giải",
    "最大フレームレート": "Tốc độ khung hình (FPS)",
    "マスターボリューム": "Âm lượng tổng",
    "BGM": "Nhạc nền (BGM)",
    "効果音": "Hiệu ứng âm thanh (SFX)",
    "ボイス": "Giọng lồng tiếng (Voice)",
    "再生完了まで待つ": "Chờ đọc hết câu thoại",
    "ゲームを終了します。": "Bạn có chắc muốn thoát game không?",
    "終了する": "Thoát game",
    "キャンセル": "Hủy",
    "タイトル画面へ戻ります。": "Bạn có chắc muốn quay về màn hình chính?",
    "タイトルへ": "Về màn hình chính",
    "セーブデータを上書きします。": "Bạn có chắc muốn ghi đè lên file lưu này không?",
    "セーブデータを削除します。": "Bạn có chắc muốn xóa file lưu này không?",
    "OK": "Đồng ý",
    "提示する証拠品はこれで良いですか？": "Bạn có chắc muốn xuất trình bằng chứng này không?",
    "いいえ": "Không",
    "はい": "Có",
    "ご意見・ご感想フォームを開きます。\n※ ブラウザが起動します。": "Mở biểu mẫu gửi ý kiến đóng góp & phản hồi.\n※ Sẽ mở trình duyệt web của bạn."
}

def patch_naninovel_ui():
    if not os.path.exists(UI_BUNDLE):
        print(f"[!] UI bundle not found: {UI_BUNDLE}")
        return

    backup_bundle(UI_BUNDLE)
    env = UnityPy.load(UI_BUNDLE)
    updated_count = 0

    def update_dict(d):
        nonlocal updated_count
        if isinstance(d, dict):
            if "_localizableText" in d:
                lt = d["_localizableText"]
                def_txt = lt.get("_defaultText", "")
                loc_txts = lt.get("_localizedTexts", [])
                
                # Check if we have a translation for this default text
                if def_txt in UI_TRANSLATIONS:
                    vi_text = UI_TRANSLATIONS[def_txt]
                    # Update or add for locale 2 (zh-Hans)
                    found = False
                    for item in loc_txts:
                        if item.get("_locale") == 2:
                            item["_text"] = vi_text
                            found = True
                            break
                    if not found:
                        loc_txts.append({"_locale": 2, "_text": vi_text})
                    updated_count += 1
            for v in d.values():
                update_dict(v)
        elif isinstance(d, list):
            for item in d:
                update_dict(item)

    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            tree = obj.read_typetree()
            update_dict(tree)
            obj.save_typetree(tree)

    with open(UI_BUNDLE, "wb") as f:
        f.write(env.file.save())

    print(f"[SUCCESS] Patched {updated_count} Options UI elements in '{os.path.basename(UI_BUNDLE)}'.")

def patch_base_managedtext():
    if not os.path.exists(MANAGEDTEXT_BUNDLE):
        print(f"[!] ManagedText bundle not found: {MANAGEDTEXT_BUNDLE}")
        return

    backup_bundle(MANAGEDTEXT_BUNDLE)
    env = UnityPy.load(MANAGEDTEXT_BUNDLE)
    
    for obj in env.objects:
        if obj.type.name == "TextAsset" and obj.read().m_Name == "Locales":
            d = obj.read()
            d.m_Script = """en-US: English
ja: 日本語
ko: 한국어
zh-Hans: Tiếng Việt
zh-Hant: 繁體中文
"""
            d.save()
            print("  [+] Patched base Locales to display 'Tiếng Việt'")

    with open(MANAGEDTEXT_BUNDLE, "wb") as f:
        f.write(env.file.save())

    print(f"[SUCCESS] Patched '{os.path.basename(MANAGEDTEXT_BUNDLE)}'.")

if __name__ == "__main__":
    patch_naninovel_ui()
    patch_base_managedtext()
