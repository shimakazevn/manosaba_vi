"""
Create Standalone Vietnamese Localization Patch Package for Mahou Shoujo no Majo Saiban.
Packages all modified binaries, bundles, installer scripts, and guides into a clean zip & directory.
Supports automated semantic versioning and changelog tracking.
"""
import os
import sys
import json
import shutil
import zipfile
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(GAME_DIR, "version.json")
RELEASE_DIR = os.path.join(GAME_DIR, "release_patch")
PATCH_DATA_DIR = os.path.join(RELEASE_DIR, "patch_data")

STANDALONE_SRC = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
STANDALONE_DEST = os.path.join(PATCH_DATA_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")

PATCHED_BUNDLES = [
    # 1. Gameplay data
    "general-data_assets_all.bundle",
    # 2. UI & Text
    "general-sprites_assets_all.bundle",
    "naninovel-ui_assets_all.bundle",
    "general-managedtext_assets_all.bundle",
    "general-localization-zhhans-text_assets_all.bundle",
    # 3. 24 Script Bundles
    "general-localization-zhhans-scripts-act01_chapter01_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter01_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter02_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter02_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter03_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter03_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter04_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter04_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter05_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act01_chapter05_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter01_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter01_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter02_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter02_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter03_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter03_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter04_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter04_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter05_advbad_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter05_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-act02_chapter06_trial_assets_all.bundle",
    "general-localization-zhhans-scripts-common_assets_all.bundle",
    "general-localization-zhhans-scripts-debug_assets_all.bundle",
    "general-localization-zhhans-scripts-system_assets_all.bundle",
]

def load_or_bump_version(bump=False):
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            vdata = json.load(f)
    else:
        vdata = {"version": "1.0.0", "name": "Mahou Shoujo no Majo Saiban Vietnamese Patch", "changelog": []}

    if bump:
        parts = vdata["version"].split(".")
        if len(parts) == 3:
            parts[2] = str(int(parts[2]) + 1)
        elif len(parts) == 2:
            parts.append("1")
        else:
            parts = ["1", "0", "1"]
        vdata["version"] = ".".join(parts)
        vdata["updated_at"] = datetime.now().isoformat()
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            json.dump(vdata, f, ensure_ascii=False, indent=2)
        print(f"[*] Bumped patch version to: v{vdata['version']}")

    return vdata["version"]

def get_installer_bat(version):
    return f"""@echo off
chcp 65001 >nul
title Cài Đặt Patch Việt Hóa - Mahou Shoujo no Majo Saiban v{version}
color 0A

echo =======================================================================
echo          CÀI ĐẶT BẢN VIỆT HÓA - MAHOU SHOUJO NO MAJO SAIBAN
echo                             Phiên bản: v{version}
echo =======================================================================
echo.

if not exist "manosaba.exe" (
    echo [!] LỖI: Vui lòng chép toàn bộ file trong thư mục patch vào thư mục gốc của game!
    echo     (Nơi chứa file manosaba.exe và thư mục manosaba_Data)
    echo.
    pause
    exit /b
)

echo [*] Đang sao lưu các file gốc của game vào thư mục 'backup_goc'...
if not exist "backup_goc" mkdir "backup_goc"
if not exist "backup_goc\\StandaloneWindows64" mkdir "backup_goc\\StandaloneWindows64"

if exist "GameAssembly.dll" (
    if not exist "backup_goc\\GameAssembly.dll" copy /y "GameAssembly.dll" "backup_goc\\GameAssembly.dll" >nul
)

set "SA_DIR=manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"
for %%F in (
    general-data_assets_all.bundle
    general-sprites_assets_all.bundle
    naninovel-ui_assets_all.bundle
    general-managedtext_assets_all.bundle
    general-localization-zhhans-text_assets_all.bundle
) do (
    if exist "%SA_DIR%\\%%F" (
        if not exist "backup_goc\\StandaloneWindows64\\%%F" copy /y "%SA_DIR%\\%%F" "backup_goc\\StandaloneWindows64\\%%F" >nul
    )
)

echo [*] Đang cài đặt các file Việt Hóa v{version} vào game...
copy /y "patch_data\\GameAssembly.dll" "GameAssembly.dll" >nul
xcopy /s /e /y "patch_data\\manosaba_Data\\*" "manosaba_Data\\" >nul

echo.
echo =======================================================================
echo [SUCCESS] CÀI ĐẶT BẢN VIỆT HÓA v{version} THÀNH CÔNG!
echo.
echo * HƯỚNG DẪN TRONG GAME:
echo   1. Mở game manosaba.exe
echo   2. Vào Cài đặt (Options/Config) -> Ngôn ngữ (Language) -> Chọn 'Tiếng Việt'.
echo   3. Thưởng thức game trọn vẹn bằng Tiếng Việt!
echo =======================================================================
echo.
pause
"""

UNINSTALLER_BAT = """@echo off
chcp 65001 >nul
title Gỡ Cài Đặt Patch Việt Hóa - Mahou Shoujo no Majo Saiban
color 0C

echo =======================================================================
echo          GỠ CÀI ĐẶT BẢN VIỆT HÓA - MAHOU SHOUJO NO MAJO SAIBAN
echo =======================================================================
echo.

if not exist "backup_goc" (
    echo [!] Không tìm thấy thư mục sao lưu 'backup_goc'. Không thể tự động khôi phục!
    pause
    exit /b
)

echo [*] Đang khôi phục lại các file gốc của game...
if exist "backup_goc\\GameAssembly.dll" copy /y "backup_goc\\GameAssembly.dll" "GameAssembly.dll" >nul
if exist "backup_goc\\StandaloneWindows64\\*" (
    copy /y "backup_goc\\StandaloneWindows64\\*" "manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64\\" >nul
)

echo.
echo [SUCCESS] Đã khôi phục game về nguyên bản thành công!
echo.
pause
"""

def get_readme_txt(version):
    return f"""===============================================================================
               BẢN DỊCH VIỆT NGỮ - MAHOU SHOUJO NO MAJO SAIBAN
                    (Phiên Tòa Xét Xử Ma Nữ Của Ma Pháp Thiếu Nữ)
                                Phiên bản: v{version}
===============================================================================

1. GIỚI THIỆU:
   - Bản dịch tiếng Việt hoàn chỉnh toàn bộ kịch bản, lời thoại, tranh luận, 
     Sổ Tay Phù Thủy, Manh mối, Bằng chứng, Luật lệ, Bản đồ và Giao diện đồ họa.

2. HƯỚNG DẪN CÀI ĐẶT:
   Bước 1: Giải nén toàn bộ tệp ZIP patch này.
   Bước 2: Chép tất cả các file và thư mục:
           - Cai_Dat_Viet_Hoa.bat
           - Go_Viet_Hoa.bat
           - patch_data/
           vào thư mục cài đặt gốc của game (nơi chứa file manosaba.exe).
   Bước 3: Chạy file 'Cai_Dat_Viet_Hoa.bat' và đợi vài giây cho đến khi hiện thông báo thành công.
   Bước 4: Mở game -> Vào Cài đặt (Options) -> Chọn ngôn ngữ 'Tiếng Việt'.

3. CÁCH GỠ PATCH (NẾU MUỐN):
   - Chạy file 'Go_Viet_Hoa.bat' trong thư mục game để khôi phục lại game gốc.

Chúc các bạn có những giây phút trải nghiệm game thật tuyệt vời!
===============================================================================
"""

def create_patch(bump=False):
    version = load_or_bump_version(bump)
    print("==================================================")
    print(f"       CREATING VIETNAMESE PATCH PACKAGE v{version} ")
    print("==================================================")
    
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
    os.makedirs(STANDALONE_DEST, exist_ok=True)

    # 1. Copy GameAssembly.dll
    dll_src = os.path.join(GAME_DIR, "GameAssembly.dll")
    if os.path.exists(dll_src):
        shutil.copy2(dll_src, os.path.join(PATCH_DATA_DIR, "GameAssembly.dll"))
        print(f"[+] Packaged GameAssembly.dll ({os.path.getsize(dll_src):,} bytes)")

    # 2. Copy Patched AssetBundles
    cnt = 0
    total_size = 0
    for b_name in PATCHED_BUNDLES:
        src_bundle = os.path.join(STANDALONE_SRC, b_name)
        if os.path.exists(src_bundle):
            dest_bundle = os.path.join(STANDALONE_DEST, b_name)
            shutil.copy2(src_bundle, dest_bundle)
            sz = os.path.getsize(src_bundle)
            total_size += sz
            cnt += 1
        else:
            print(f"[!] Warning: Bundle not found: {b_name}")

    print(f"[+] Packaged {cnt} AssetBundles ({total_size:,} bytes)")

    # 3. Write Installer, Uninstaller, Readme
    with open(os.path.join(RELEASE_DIR, "Cai_Dat_Viet_Hoa.bat"), "w", encoding="utf-8") as f:
        f.write(get_installer_bat(version))
    with open(os.path.join(RELEASE_DIR, "Go_Viet_Hoa.bat"), "w", encoding="utf-8") as f:
        f.write(UNINSTALLER_BAT)
    with open(os.path.join(RELEASE_DIR, "HUONG_DAN_SU_DUNG.txt"), "w", encoding="utf-8") as f:
        f.write(get_readme_txt(version))

    print(f"[+] Created Installer & Documentation scripts for v{version}.")

    # 4. Create ZIP Archive
    zip_filename = os.path.join(GAME_DIR, f"Mahou_Shoujo_VietHoa_Patch_v{version}.zip")
    print(f"[*] Compressing into ZIP archive: {zip_filename}...")
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, RELEASE_DIR)
                zipf.write(abs_path, rel_path)

    zip_size = os.path.getsize(zip_filename)
    print(f"\n==================================================")
    print(f"[SUCCESS] Patch v{version} created successfully!")
    print(f"  - Release Folder: {RELEASE_DIR}")
    print(f"  - Release ZIP:    {zip_filename} ({zip_size:,} bytes / {zip_size/(1024*1024):.2f} MB)")
    print(f"==================================================")

if __name__ == "__main__":
    bump = "--bump" in sys.argv
    create_patch(bump=bump)
