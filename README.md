# Mahou Shoujo no Majo Saiban (MGWT) - Vietnamese Localization Patch

Dự án bản dịch Tiếng Việt cho tựa game **Mahou Shoujo no Majo Saiban (Mahosaba / MGWT)** - v1.1.2.

---

## 📌 1. Tổng Quan Dự Án
Bản Việt hóa được xây dựng trên nền tảng **Unity Addressables & Naninovel Engine**, can thiệp trực tiếp qua IL2CPP Hook và AssetBundle Injector để hiển thị tùy chọn **`Tiếng Việt`** trong menu Cài Đặt.

* **Quy mô dịch thuật:** 34,836 / 34,836 câu thoại (100.0%) trên toàn bộ 441 kịch bản.
* **Quy chuẩn văn phong:** Tuân thủ `MASTER_CONTEXT_BIBLE.md` (phân tầng đại từ nhân xưng 16 nhân vật chính xác theo bối cảnh).
* **Quy chuẩn hiển thị:** Tự động wrap chữ (Text Wrap) theo cơ chế native của TextMeshPro, không làm vỡ giao diện.
* **Bảo toàn cơ chế:** 100% thẻ tương tác tranh luận `<link="Objection_...">` và thẻ định dạng `<color=...>`, `<b>`, `<i>`.
* **Dữ liệu gameplay:** 100% Manh mối (146 items), Truyền thuyết thế giới (24 items), Điều luật ngục (5 items), Hồ sơ nhân vật (127 items), Bản đồ (5 items).
* **Đồ họa & Sprite UI:** Đã vẽ lại & render 66 Sprite tiếng Việt (Logo, Nút bấm, Tab, Tranh luận, Chiêu thức Ma thuật).

---

## 📁 Cấu Trúc Repository

```text
├── .gitignore
├── README.md
├── README_VIETNAMESE_PATCH.md
├── Chay_Game_Tieng_Viet.bat
├── Play_Game_VN.bat
├── LICENSE.md
├── tools/                                # Bộ công cụ đóng gói & kiểm thử
│   ├── run_full_pipeline.py              # Master build & export pipeline
│   ├── export_localization.py            # Xuất hội thoại từ game
│   ├── import_localization.py            # Đóng gói hội thoại vào game
│   ├── export_game_data.py               # Xuất data gameplay từ game
│   ├── import_game_data.py               # Đóng gói data gameplay vào game
│   ├── export_import_sprites.py          # Trích xuất / quản lý Sprite
│   ├── render_vietnamese_sprites.py      # Render chữ tiếng Việt lên Sprite
│   ├── patch_all_atlases.py              # Đóng gói Sprite vào SpriteAtlases
│   ├── patch_ui_locales.py               # Patch UI locale bundles
│   ├── patch_options_menu.py             # Patch nhãn UI Options
│   ├── patch_all_locales_aliases.py      # Patch alias zh-Hans sang vi-VN
│   ├── patch_dropdown_ui_direct.py       # Patch trực tiếp nhãn dropdown
│   ├── patch_dll_all_chinese.py          # Patch chuỗi ngôn ngữ trong GameAssembly
│   ├── patch_dropdown_hook.py            # Cài IL2CPP Hook dropdown tiếng Việt
│   ├── ai_translate_engine.py            # Engine dịch thuật
│   ├── batch_translate_all.py            # Script dịch hàng loạt
│   ├── backup_restore_tool.py            # Sao lưu & phục hồi
│   └── deep_game_integrity_checker.py    # Kiểm tra toàn vẹn game (Zero-Bug)
└── translation/                          # Tài nguyên dịch thuật nguồn
    ├── MASTER_CONTEXT_BIBLE.md           # Kinh thánh bối cảnh, xưng hô & thuật ngữ
    ├── cache/                            # Bộ nhớ đệm dịch thuật
    ├── dialogues/                        # 441 kịch bản hội thoại JSON
    ├── game_data/                        # 7 tệp JSON gameplay data
    └── sprites/                          # 66 Sprite tiếng Việt đã qua xử lý
```

---

## 🛠️ Hướng Dẫn Build & Đóng Gói Patch

### Yêu cầu:
- Python 3.10+
- Thư viện Python: `pip install UnityPy pillow`

### Build toàn bộ bản dịch vào game:
```bash
python tools/run_full_pipeline.py build
```

### Kiểm tra toàn vẹn bản dịch:
```bash
python tools/deep_game_integrity_checker.py
```

---

## 🎮 Cách Cài Đặt & Chơi Game
1. Chạy lệnh build để nạp bản dịch vào game.
2. Khởi động game qua file `Chay_Game_Tieng_Viet.bat` hoặc `manosaba.exe`.
3. Vào **Options (Cài đặt)** -> Mục **Language (Ngôn ngữ)** -> Chọn **Tiếng Việt**.
