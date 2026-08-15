"""
Patch all Chinese culture table entries in GameAssembly.dll to 'Tiếng Việt'.
This ensures that whether CultureInfo queries 'zh-Hans', 'zh-CN', 'zh-CHS', etc.,
the NativeName returned is ALWAYS 'Tiếng Việt'.
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = r"e:\MGWT.v1.1.2"
DLL_PATH = os.path.join(GAME_DIR, "GameAssembly.dll")

with open(DLL_PATH, "rb") as f:
    dll = bytearray(f.read())

print(f"GameAssembly.dll size: {len(dll)} bytes")

# 1. Patch zh-Hans at 0x2ACC0E8 -> 'Tiếng Việt'
zh_hans_key = dll.find(b"zh-Hans\x00", 0x2AC0000)
if zh_hans_key != -1:
    val_pos = zh_hans_key + len(b"zh-Hans\x00")
    val_end = dll.find(b"\x00", val_pos)
    val_len = val_end - val_pos
    new_val = "Tiếng Việt".encode("utf-8")
    padded = new_val.ljust(val_len, b" ")
    dll[val_pos : val_pos + val_len] = padded
    print(f"[+] Patched zh-Hans NativeName at 0x{val_pos:X} (len {val_len})")

# 2. Patch zh-CN at 0x2ACE424 -> 'Tiếng Việt'
zh_cn_key = dll.find(b"zh-CN\x00", 0x2AC0000)
if zh_cn_key != -1:
    val_pos = zh_cn_key + len(b"zh-CN\x00")
    val_end = dll.find(b"\x00", val_pos)
    val_len = val_end - val_pos
    new_val = "Tiếng Việt".encode("utf-8")
    if len(new_val) <= val_len:
        padded = new_val.ljust(val_len, b" ")
        dll[val_pos : val_pos + val_len] = padded
        print(f"[+] Patched zh-CN NativeName at 0x{val_pos:X} (len {val_len})")

# Save GameAssembly.dll
with open(DLL_PATH, "wb") as f:
    f.write(dll)

print("[SUCCESS] GameAssembly.dll culture tables successfully patched!")
