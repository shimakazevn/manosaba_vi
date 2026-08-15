"""
Patch GameAssembly.dll to redirect LocalizationDropdown.SetOptions to our hook function,
forcing option1 (Chinese) to always be 'Tiếng Việt'.
"""
import os
import sys
import struct

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GAME_DIR = r"e:\MGWT.v1.1.2"
DLL_PATH = os.path.join(GAME_DIR, "GameAssembly.dll")

with open(DLL_PATH, "rb") as f:
    dll = bytearray(f.read())

# PE Sections info
image_base = 0x180000000
il2cpp_foff = 0x30A800
il2cpp_rva = 0x30C000
data_foff = 0x2D3B000
data_rva = 0x2D3D000

hook_va = 0x1825168D0
hook_foff = il2cpp_foff + (hook_va - (image_base + il2cpp_rva))

static_str_va = 0x182D3D010
static_str_foff = data_foff + (static_str_va - (image_base + data_rva))

add_options_va = 0x181ED8600

call_site_va = 0x180CE647D
call_site_foff = il2cpp_foff + (call_site_va - (image_base + il2cpp_rva))

print(f"Hook VA: 0x{hook_va:X}, File: 0x{hook_foff:X}")
print(f"Static String VA: 0x{static_str_va:X}, File: 0x{static_str_foff:X}")
print(f"Call Site VA: 0x{call_site_va:X}, File: 0x{call_site_foff:X}")

# 1. Write static string object at static_str_foff
# Il2CppString:
# +0x00: klass (0 initially, set at runtime)
# +0x08: monitor (0)
# +0x10: length = 10 (int32)
# +0x14: u"Tiếng Việt\0"
str_text = "Tiếng Việt\x00"
str_u16 = str_text.encode("utf-16-le")

static_str_bytes = bytearray(36)
struct.pack_into('<Q', static_str_bytes, 0, 0)
struct.pack_into('<Q', static_str_bytes, 8, 0)
struct.pack_into('<I', static_str_bytes, 16, 10)
static_str_bytes[20 : 20 + len(str_u16)] = str_u16

dll[static_str_foff : static_str_foff + len(static_str_bytes)] = static_str_bytes
print(f"[+] Written static Il2CppString for 'Tiếng Việt' at File 0x{static_str_foff:X}")

# 2. Build and write hook code at hook_foff
def build_hook():
    b = bytearray()
    
    b += b'\x53' # push rbx
    b += b'\x41\x54' # push r12
    b += b'\x41\x55' # push r13
    
    b += b'\x48\x85\xF6' # test rsi, rsi
    jz1_pos = len(b); b += b'\x74\x00' # jz do_call
    
    b += b'\x83\x7E\x18\x02' # cmp dword ptr [rsi+0x18], 2
    jl1_pos = len(b); b += b'\x7C\x00' # jl do_call
    
    b += b'\x48\x8B\x46\x10' # mov rax, [rsi+0x10]
    b += b'\x48\x85\xC0' # test rax, rax
    jz2_pos = len(b); b += b'\x74\x00' # jz do_call
    
    b += b'\x4C\x8B\x60\x20' # mov r12, [rax+0x20]
    b += b'\x4C\x8B\x68\x28' # mov r13, [rax+0x28]
    b += b'\x4D\x85\xED' # test r13, r13
    jz3_pos = len(b); b += b'\x74\x00' # jz do_call
    
    b += b'\x31\xDB' # xor ebx, ebx
    b += b'\x4D\x85\xE4' # test r12, r12
    jz_opt1_pos = len(b); b += b'\x74\x00' # jz check_opt1
    
    b += b'\x49\x8B\x5C\x24\x10' # mov rbx, [r12+0x10]
    b += b'\x48\x85\xDB' # test rbx, rbx
    jz_opt1_2_pos = len(b); b += b'\x74\x00' # jz check_opt1
    b += b'\x48\x8B\x1B' # mov rbx, [rbx]
    jmp_got_pos = len(b); b += b'\xEB\x00' # jmp got_klass
    
    # check_opt1:
    check_opt1_target = len(b)
    b[jz_opt1_pos+1] = check_opt1_target - (jz_opt1_pos + 2)
    b[jz_opt1_2_pos+1] = check_opt1_target - (jz_opt1_2_pos + 2)
    
    b += b'\x49\x8B\x5D\x10' # mov rbx, [r13+0x10]
    b += b'\x48\x85\xDB' # test rbx, rbx
    jz4_pos = len(b); b += b'\x74\x00' # jz do_call
    b += b'\x48\x8B\x1B' # mov rbx, [rbx]
    
    # got_klass:
    got_klass_target = len(b)
    b[jmp_got_pos+1] = got_klass_target - (jmp_got_pos + 2)
    
    b += b'\x48\x85\xDB' # test rbx, rbx
    jz5_pos = len(b); b += b'\x74\x00' # jz do_call
    
    b += b'\x49\xBB' + struct.pack('<Q', static_str_va) # mov r11, static_str_va
    b += b'\x49\x89\x1B' # mov [r11], rbx
    b += b'\x4D\x89\x5D\x10' # mov qword ptr [r13+0x10], r11
    
    # do_call:
    do_call_target = len(b)
    b[jz1_pos+1] = do_call_target - (jz1_pos + 2)
    b[jl1_pos+1] = do_call_target - (jl1_pos + 2)
    b[jz2_pos+1] = do_call_target - (jz2_pos + 2)
    b[jz3_pos+1] = do_call_target - (jz3_pos + 2)
    b[jz4_pos+1] = do_call_target - (jz4_pos + 2)
    b[jz5_pos+1] = do_call_target - (jz5_pos + 2)
    
    b += b'\x41\x5D' # pop r13
    b += b'\x41\x5C' # pop r12
    b += b'\x5B'     # pop rbx
    b += b'\x45\x31\xC0' # xor r8d, r8d
    b += b'\x48\x89\xF2' # mov rdx, rsi
    b += b'\x48\xB8' + struct.pack('<Q', add_options_va) # mov rax, add_options_va
    b += b'\xFF\xE0' # jmp rax
    
    return bytes(b)

hook_bytes = build_hook()
dll[hook_foff : hook_foff + len(hook_bytes)] = hook_bytes
print(f"[+] Written {len(hook_bytes)} bytes of hook code at File 0x{hook_foff:X}")

# 3. Patch call site at call_site_foff
# 0x180CE647D: call hook_va (E8 [rel]) + 3 NOPs
rel_call = hook_va - (call_site_va + 5)
call_patch = b'\xE8' + struct.pack('<i', rel_call) + b'\x90\x90\x90'
dll[call_site_foff : call_site_foff + 8] = call_patch
print(f"[+] Patched call site at File 0x{call_site_foff:X} -> call 0x{hook_va:X}")

# Save GameAssembly.dll
with open(DLL_PATH, "wb") as f:
    f.write(dll)

print("[SUCCESS] GameAssembly.dll dropdown hook applied cleanly!")

if __name__ == "__main__":
    pass
