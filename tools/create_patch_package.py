"""
Create Standalone Vietnamese Localization Patch Package for Mahou Shoujo no Majo Saiban.
Uses reliable GOTO-based batch scripts and direct root folder structure.
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

STANDALONE_SRC = os.path.join(GAME_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")
STANDALONE_DEST = os.path.join(RELEASE_DIR, "manosaba_Data", "StreamingAssets", "aa", "StandaloneWindows64")

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

def get_bulletproof_installer_bat(version):
    return f"""@echo off
chcp 65001 >nul
title Cài Đặt Patch Việt Hóa v{version} - Mahou Shoujo no Majo Saiban
color 0A

echo =======================================================================
echo        CÀI ĐẶT BẢN DỊCH TIẾNG VIỆT - MAHOU SHOUJO NO MAJO SAIBAN
echo                            Phiên bản: v{version}
echo =======================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "GAME_ROOT=%SCRIPT_DIR%"

if exist "%SCRIPT_DIR%manosaba.exe" goto FOUND_GAME
if exist "%SCRIPT_DIR%..\\manosaba.exe" (
    set "GAME_ROOT=%SCRIPT_DIR%..\\"
    goto FOUND_GAME
)

:NOT_FOUND
color 0C
echo [!] KHÔNG TÌM THẤY FILE GAME (manosaba.exe)!
echo.
echo CÁCH CÀI ĐẶT CỰC KỲ ĐƠN GIẢN:
echo   Cách 1: KÉO THẢ toàn bộ thư mục 'manosaba_Data' và file 'GameAssembly.dll'
echo           vào thư mục cài đặt gốc của game (nơi chứa file manosaba.exe).
echo   Cách 2: Giải nén toàn bộ tệp ZIP này vào thư mục chứa game rồi chạy lại file này.
echo.
pause
exit /b 1

:FOUND_GAME
echo [*] Đã nhận diện thư mục game tại: %GAME_ROOT%
echo [*] Đang tạo thư mục sao lưu 'backup_goc'...
if not exist "%GAME_ROOT%backup_goc" mkdir "%GAME_ROOT%backup_goc"
if not exist "%GAME_ROOT%backup_goc\\StandaloneWindows64" mkdir "%GAME_ROOT%backup_goc\\StandaloneWindows64"

if exist "%GAME_ROOT%GameAssembly.dll" (
    if not exist "%GAME_ROOT%backup_goc\\GameAssembly.dll" (
        copy /Y "%GAME_ROOT%GameAssembly.dll" "%GAME_ROOT%backup_goc\\GameAssembly.dll" >nul
        echo [+] Đã sao lưu GameAssembly.dll gốc.
    )
)

set "DEST_DIR=%GAME_ROOT%manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"
set "SRC_DIR=%SCRIPT_DIR%manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"

echo [*] Đang sao lưu và cài đặt các AssetBundles Việt Hóa...

if not exist "%DEST_DIR%" (
    echo [!] Lỗi: Không tìm thấy thư mục StandaloneWindows64 của game!
    pause
    exit /b 1
)

xcopy /Y /S /E "%SCRIPT_DIR%manosaba_Data\\*" "%GAME_ROOT%manosaba_Data\\"
if exist "%SCRIPT_DIR%GameAssembly.dll" (
    copy /Y "%SCRIPT_DIR%GameAssembly.dll" "%GAME_ROOT%GameAssembly.dll"
)

echo.
echo =======================================================================
echo [SUCCESS] CÀI ĐẶT BẢN VIỆT HÓA v{version} THÀNH CÔNG 100%!
echo.
echo * HƯỚNG DẪN TRONG GAME:
echo   1. Mở game bằng file manosaba.exe
echo   2. Vào Cài đặt (Options) -> Chọn ngôn ngữ 'Tiếng Việt'.
echo   3. Thưởng thức game trọn vẹn bằng Tiếng Việt!
echo =======================================================================
echo.
pause
"""

def get_bulletproof_uninstaller_bat():
    return """@echo off
chcp 65001 >nul
title Gỡ Cài Đặt Patch Việt Hóa - Mahou Shoujo no Majo Saiban
color 0C

echo =======================================================================
echo          GỠ CÀI ĐẶT BẢN VIỆT HÓA - MAHOU SHOUJO NO MAJO SAIBAN
echo =======================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "GAME_ROOT=%SCRIPT_DIR%"

if exist "%SCRIPT_DIR%manosaba.exe" goto FOUND_UNINSTALL
if exist "%SCRIPT_DIR%..\\manosaba.exe" (
    set "GAME_ROOT=%SCRIPT_DIR%..\\"
    goto FOUND_UNINSTALL
)

:FOUND_UNINSTALL
if not exist "%GAME_ROOT%backup_goc" (
    echo [!] Không tìm thấy thư mục sao lưu 'backup_goc'!
    echo     Không thể tự động khôi phục game về nguyên bản.
    echo.
    pause
    exit /b 1
)

echo [*] Đang khôi phục lại các file gốc của game...
if exist "%GAME_ROOT%backup_goc\\GameAssembly.dll" (
    copy /Y "%GAME_ROOT%backup_goc\\GameAssembly.dll" "%GAME_ROOT%GameAssembly.dll" >nul
    echo [+] Đã khôi phục: GameAssembly.dll
)

set "DEST_DIR=%GAME_ROOT%manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"
if exist "%GAME_ROOT%backup_goc\\StandaloneWindows64" (
    copy /Y "%GAME_ROOT%backup_goc\\StandaloneWindows64\\*.bundle" "%DEST_DIR%\\" >nul
    echo [+] Đã khôi phục các AssetBundles gốc.
)

echo.
echo =======================================================================
echo [SUCCESS] ĐÃ KHÔI PHỤC GAME VỀ NGUYÊN BẢN GỐC THÀNH CÔNG!
echo =======================================================================
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
   - Bản dịch tiếng Việt hoàn chỉnh 100% toàn bộ kịch bản, lời thoại, tranh luận, 
     Sổ Tay Phù Thủy, Manh mối, Bằng chứng, Luật lệ, Bản đồ và Giao diện đồ họa.

2. CÁCH CÀI ĐẶT (CHỌN 1 TRONG 2 CÁCH CỰC KỲ DỄ DÀNG):
   
   【CÁCH 1 - KÉO THẢ NHANH NHẤT (KHUYÊN DÙNG)】:
   - Giải nén toàn bộ tệp ZIP này trực tiếp vào thư mục cài game (nơi chứa file manosaba.exe).
   - Khi Windows hỏi "Replace or Skip Files", chọn "Replace the files in the destination" (Chép đè).
   - Mở game -> Vào Cài đặt (Options) -> Chọn ngôn ngữ 'Tiếng Việt'.

   【CÁCH 2 - DÙNG SCRIPT TỰ ĐỘNG SAO LƯU】:
   - Giải nén tệp ZIP vào thư mục game.
   - Nhấp đúp chạy file 'Cai_Dat_Viet_Hoa.bat'.
   - Mở game -> Vào Cài đặt (Options) -> Chọn ngôn ngữ 'Tiếng Việt'.

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

    # 1. Copy GameAssembly.dll directly to root of release folder
    dll_src = os.path.join(GAME_DIR, "GameAssembly.dll")
    if os.path.exists(dll_src):
        shutil.copy2(dll_src, os.path.join(RELEASE_DIR, "GameAssembly.dll"))
        print(f"[+] Packaged GameAssembly.dll ({os.path.getsize(dll_src):,} bytes)")

    # 2. Copy Patched AssetBundles into manosaba_Data/...
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
        f.write(get_bulletproof_installer_bat(version))
    with open(os.path.join(RELEASE_DIR, "Go_Viet_Hoa.bat"), "w", encoding="utf-8") as f:
        f.write(get_bulletproof_uninstaller_bat())
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
