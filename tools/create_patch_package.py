"""
Create Standalone Vietnamese Localization Patch Package for Mahou Shoujo no Majo Saiban.
STRICTLY TEXT-ONLY WITH SEPARATE PATCH DATA FOLDER (Zero-Overwrite on Unzip).
- Zip extracts into 'Patch_Viet_Hoa/' folder alongside BAT files (does NOT overwrite manosaba_Data upon unzip).
- Cai_Dat_Viet_Hoa.bat safely backs up original files BEFORE copying translated files.
- Go_Cai_Dat_Viet_Hoa.bat restores 100% original files.
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
PATCH_DATA_DEST = os.path.join(RELEASE_DIR, "Patch_Viet_Hoa")

PATCHED_BUNDLES = [
    # 24 Script Bundles ONLY
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

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            vdata = json.load(f)
            return vdata.get("version", vdata.get("patch_version", "1.0.14"))
    return "1.0.14"

def create_patch():
    version = get_current_version()

    print("==================================================")
    print(f"  CREATING ZERO-OVERWRITE PATCH PACKAGE v{version} ")
    print("==================================================")

    # 1. Clean release directory
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
    os.makedirs(PATCH_DATA_DEST, exist_ok=True)

    # 2. Copy the 24 script bundles into Patch_Viet_Hoa/
    bundle_bytes = 0
    copied_count = 0
    for b_name in PATCHED_BUNDLES:
        src = os.path.join(STANDALONE_SRC, b_name)
        dst = os.path.join(PATCH_DATA_DEST, b_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            b_size = os.path.getsize(dst)
            bundle_bytes += b_size
            copied_count += 1
        else:
            print(f"[!] Warning: Missing bundle {b_name}")

    print(f"[+] Packaged {copied_count} Script AssetBundles into 'Patch_Viet_Hoa/' ({bundle_bytes:,} bytes)")

    # 3. Create installer bat (Robust ANSI script with auto-detect)
    installer_bat = f"""@echo off
chcp 65001 >nul
title Cai Dat Ban Dich Tieng Viet v{version}
echo ========================================================
echo   CAI DAT BAN DICH VIET HOA v{version} (TEXT-ONLY)
echo ========================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "GAME_DIR=%SCRIPT_DIR%.."
for %%I in ("%GAME_DIR%") do set "GAME_DIR=%%~fI"

if not exist "%GAME_DIR%\\manosaba.exe" (
    set "GAME_DIR=%CD%"
)

if not exist "%GAME_DIR%\\manosaba.exe" (
    echo [LOI] Khong tim thay manosaba.exe!
    echo       Thu muc da kiem tra: %GAME_DIR%
    echo.
    pause
    exit /b 1
)

echo [*] Thu muc game: %GAME_DIR%

set "PATCH_DIR=%SCRIPT_DIR%Patch_Viet_Hoa"
if not exist "%PATCH_DIR%" (
    if exist "%GAME_DIR%\\Patch_Viet_Hoa" (
        set "PATCH_DIR=%GAME_DIR%\\Patch_Viet_Hoa"
    )
)
if not exist "%PATCH_DIR%" (
    echo [LOI] Khong tim thay thu muc Patch_Viet_Hoa!
    echo       Duong dan kiem tra: %PATCH_DIR%
    echo.
    pause
    exit /b 1
)

set "TARGET_DIR=%GAME_DIR%\\manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"
set "BACKUP_DIR=%TARGET_DIR%\\backup_goc"

if not exist "%TARGET_DIR%" (
    echo [LOI] Khong tim thay thu muc du lieu game!
    echo       Kiem tra: %TARGET_DIR%
    echo.
    pause
    exit /b 1
)

echo.
echo [*] BUOC 1: Sao luu 24 file kich ban goc vao backup_goc...
if not exist "%BACKUP_DIR%" (
    mkdir "%BACKUP_DIR%" >nul 2>&1
    for %%F in (
"""
    for b in PATCHED_BUNDLES:
        installer_bat += f'        "{b}"\n'
    
    installer_bat += f"""    ) do (
        if exist "%TARGET_DIR%\\%%~F" (
            copy /Y "%TARGET_DIR%\\%%~F" "%BACKUP_DIR%\\%%~F" >nul
        )
    )
    echo [+] Da sao luu 24 file goc thanh cong!
) else (
    echo [*] Thu muc backup_goc da ton tai - giu nguyen ban backup dau tien.
)

echo.
echo [*] BUOC 2: Cai dat 24 file Tieng Viet...
copy /Y "%PATCH_DIR%\\*.bundle" "%TARGET_DIR%\\" >nul

if %errorlevel% neq 0 (
    echo [LOI] Copy file that bai! Kiem tra quyen ghi vao thu muc game.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo [THANH CONG] Da cai dat Tieng Viet va Sao luu hoan tat!
echo ========================================================
echo.
echo - Go bo Viet Hoa / Khoi phuc ban goc: Chay [Go_Cai_Dat_Viet_Hoa.bat]
echo - Vao game (manosaba.exe) -^> Cai dat -^> Ngon ngu -^> Chon [Gian the Trung] de choi.
echo.
pause
"""
    with open(os.path.join(RELEASE_DIR, "Cai_Dat_Viet_Hoa.bat"), "w", encoding="ascii", errors="ignore") as f:
        f.write(installer_bat)

    # 4. Create uninstaller / restore bat
    uninstaller_bat = """@echo off
chcp 65001 >nul
title Khoi Phuc Kich Ban Goc (Go Bo Viet Hoa)
echo ========================================================
echo   KHOI PHUC KICH BAN GOC (RESTORE ORIGINAL SCRIPTS)
echo ========================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "GAME_DIR=%SCRIPT_DIR%.."
for %%I in ("%GAME_DIR%") do set "GAME_DIR=%%~fI"

if not exist "%GAME_DIR%\\manosaba.exe" (
    set "GAME_DIR=%CD%"
)

if not exist "%GAME_DIR%\\manosaba.exe" (
    echo [LOI] Khong tim thay manosaba.exe!
    echo       Thu muc da kiem tra: %GAME_DIR%
    echo.
    pause
    exit /b 1
)

set "TARGET_DIR=%GAME_DIR%\\manosaba_Data\\StreamingAssets\\aa\\StandaloneWindows64"
set "BACKUP_DIR=%TARGET_DIR%\\backup_goc"

if not exist "%BACKUP_DIR%" (
    echo [THONG BAO] Khong tim thay thu muc backup_goc.
    echo             Game dang o ban goc (chua cai Viet Hoa).
    echo.
    pause
    exit /b 0
)

echo [*] Dang khoi phuc 24 kich ban goc tu backup_goc...
copy /Y "%BACKUP_DIR%\\*.bundle" "%TARGET_DIR%\\" >nul

echo.
echo ========================================================
echo [THANH CONG] Game da duoc khoi phuc 100%% ve ban goc sach!
echo ========================================================
echo.
pause
"""
    with open(os.path.join(RELEASE_DIR, "Go_Cai_Dat_Viet_Hoa.bat"), "w", encoding="ascii", errors="ignore") as f:
        f.write(uninstaller_bat)

    readme_txt = f"""============================================================
BẢN DỊCH VIỆT HÓA THUẦN KỊCH BẢN (TEXT-ONLY) v{version}
Mahou Shoujo no Majo Saiban
============================================================

* ĐẶC ĐIỂM BẢN TEXT-ONLY NÀY:
- Giải nén KHÔNG BAO GIỜ bị ghi đè dữ liệu game (file dịch nằm riêng trong thư mục Patch_Viet_Hoa).
- An toàn tuyệt đối 100%, không gây crash game (không đụng DLL, không đụng Texture UI).
- TỰ ĐỘNG SAO LƯU (BACKUP) các file gốc khi chạy file Cai_Dat_Viet_Hoa.bat.

* CÁCH CÀI ĐẶT:
1. Giải nén file ZIP vào thư mục game (nơi có file manosaba.exe).
2. Chạy file `Cai_Dat_Viet_Hoa.bat` (Script sẽ tự động copy file gốc vào backup_goc, sau đó mới cài đặt Tiếng Việt).
3. Mở game -> Cài đặt -> Ngôn ngữ -> Chọn [简体中文] để chơi bằng Tiếng Việt.

* CÁCH GỠ BỎ / KHÔI PHỤC BẢN GỐC:
- Chạy file `Go_Cai_Dat_Viet_Hoa.bat` bất kỳ lúc nào để khôi phục 100% nguyên bản gốc của game.
"""
    with open(os.path.join(RELEASE_DIR, "HUONG_DAN_SU_DUNG.txt"), "w", encoding="utf-8") as f:
        f.write(readme_txt)

    # 5. Create ZIP package
    zip_filename = f"Mahou_Shoujo_VietHoa_Patch_v{version}.zip"
    zip_path = os.path.join(GAME_DIR, zip_filename)
    print(f"[*] Compressing into ZIP archive: {zip_path}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, RELEASE_DIR)
                zipf.write(abs_file, rel_file)

    zip_size = os.path.getsize(zip_path)
    print("==================================================")
    print(f"[SUCCESS] Safe Patch Package created successfully!")
    print(f"  - Release Folder: {RELEASE_DIR}")
    print(f"  - Release ZIP:    {zip_path} ({zip_size:,} bytes / {zip_size/(1024*1024):.2f} MB)")
    print("==================================================")

if __name__ == "__main__":
    create_patch()
