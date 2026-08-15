"""
Backup and Restore Utility for Mahou Gari Witch Trial.
Allows creating a standalone backup of all Vietnamese translation assets and restoring them anytime.
"""
import os
import io
import sys
import shutil
import zipfile
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(GAME_DIR, "backups")

def create_translation_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = os.path.join(BACKUP_DIR, f"MGWT_Vietnamese_Translation_Backup_{timestamp}.zip")
    
    print(f"[*] Creating translation backup at: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Backup translation folder
        trans_dir = os.path.join(GAME_DIR, "translation")
        for root, dirs, files in os.walk(trans_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, GAME_DIR)
                zipf.write(full_path, rel_path)
                
        # Backup tools folder
        tools_dir = os.path.join(GAME_DIR, "tools")
        for root, dirs, files in os.walk(tools_dir):
            for f in files:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, GAME_DIR)
                zipf.write(full_path, rel_path)
                
    print(f"[SUCCESS] Backup created successfully! Size: {os.path.getsize(zip_path) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    create_translation_backup()
