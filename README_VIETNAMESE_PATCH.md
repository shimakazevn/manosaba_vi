# HƯỚNG DẪN & TÀI LIỆU BẢN VIỆT HÓA MAHOU GARI WITCH TRIAL (v1.1.2)

---

## 📌 1. Tổng Quan Dự Án
Bản Việt hóa được xây dựng trực tiếp trên nền tảng **Unity Addressables & Naninovel Engine** của game, ghi đè hoàn hảo trên gói ngôn ngữ Tiếng Trung (`zh-Hans`) và hiển thị chính thức với tên **`Tiếng Việt`** trong menu Cài Đặt.

* **Quy mô dịch thuật:** 34,836 / 34,836 câu thoại (100.0%) trên toàn bộ 441 kịch bản.
* **Quy chuẩn văn phong:** Tuân thủ **Master Context Bible** (phân tầng đại từ nhân xưng 16 nhân vật).
* **Quy chuẩn hiển thị:** Tự động wrap chữ (Text Wrap) theo cơ chế native của TextMeshPro, không tự ý chèn `<br>` ngắt dòng thô thiển giữa câu.
* **Bảo toàn cơ chế:** 100% thẻ tương tác tranh luận `<link="Objection_...">` và thẻ định dạng `<color=...>`, `<b>`, `<i>`.
* **Dữ liệu gameplay:** 100% Manh mối (146 items), Truyền thuyết thế giới (24 items), Điều luật ngục (5 items), Hồ sơ nhân vật (127 items), Bản đồ (5 items).

---

## 🎮 2. Cách Chơi Game
* **Cách 1:** Nhấp đúp vào file [`Chay_Game_Tieng_Viet.bat`](file:///e:/MGWT.v1.1.2/Chay_Game_Tieng_Viet.bat) ở thư mục gốc của game.
* **Cách 2:** Chạy trực tiếp [`manosaba.exe`](file:///e:/MGWT.v1.1.2/manosaba.exe).

---

## 🛠️ 3. Cấu Trúc Pipeline & Tự Động Hóa
Toàn bộ hệ thống được tự động hóa qua các công cụ trong thư mục `tools/`:

* **`tools/run_full_pipeline.py`:** Master script biên dịch toàn bộ game data, options UI, managed text và 440 dialogue scripts thành các Unity AssetBundles.
* **`tools/patch_options_menu.py`:** Patch 45 nhãn UI trong `naninovel-ui_assets_all.bundle` và locale trong `general-managedtext_assets_all.bundle`.
* **`tools/import_gameplay_data.py`:** Nạp dữ liệu Clues, Profiles, Notes, Rules, Maps vào `general-data_assets_all.bundle`.
* **`tools/repack_scripts.py`:** Nạp 440 kịch bản đối thoại vào 24 bundles kịch bản tương ứng.
* **`tools/batch_translate_all.py`:** Engine dịch thuật tự động theo Master Glossary & Pronoun Matrix.

---

## 📚 4. Thư Mục Dữ Liệu Gốc
* `translation/MASTER_CONTEXT_BIBLE.md`: Bộ quy chuẩn bối cảnh, lore, đại từ xưng hô 16 nhân vật và từ điển thuật ngữ.
* `translation/dialogues/`: Chứa 441 file JSON kịch bản đối thoại.
* `translation/game_data/`: Chứa 7 file JSON dữ liệu gameplay (clues, notes, rules, profiles, maps, characters, authors).
* `translation/ui/`: Chứa các file JSON UI text assets.
