"""
AI Translation Engine for Mahou Shoujo no Majo Saiban (manosaba).
Integrates Master Context Bible with LLM APIs (Gemini, OpenAI, DeepSeek, Claude, OpenRouter, LocalLLM).
"""
import os
import io
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GAME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIALOGUES_DIR = os.path.join(GAME_DIR, "translation", "dialogues")
GAME_DATA_DIR = os.path.join(GAME_DIR, "translation", "game_data")
CONTEXT_BIBLE_PATH = os.path.join(GAME_DIR, "translation", "MASTER_CONTEXT_BIBLE.md")

def load_context_bible():
    if os.path.exists(CONTEXT_BIBLE_PATH):
        with open(CONTEXT_BIBLE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ""

SYSTEM_PROMPT_TEMPLATE = """Bạn là một dịch giả game chuyên nghiệp (Visual Novel / Mystery / Trial Game). Nhiệm vụ của bạn là dịch các câu thoại kịch bản game "魔法少女ノ魔女裁判 (Mahou Shoujo no Majo Saiban)" từ Tiếng Nhật (có đối chiếu Tiếng Trung) sang TIẾNG VIỆT tự nhiên, mượt mà, đúng tính cách nhân vật.

Dưới đây là BÁCH KHOA TOÀN THƯ NGỮ CẢNH BẮT BUỘC TUÂN THỦ:
{context_bible}

QUY TẮC DỊCH THUẬT QUAN TRỌNG:
1. Tuân thủ 100% Ma trận xưng hô của từng nhân vật (Ema: mình/tớ; Hiro: tôi; Hanna: bổn tiểu thư/ngươi; Alisa: tao/mày; Warden: tôi/quý vị; Margo: chị/em...).
2. BẢO TỒN NGUYÊN VẸN các thẻ phản biện tòa án `<link="Objection_...">...</link>`. Cấm xóa hoặc đổi tên ID bên trong tag link.
3. LOẠI BỎ hoàn toàn các thẻ `<ruby="... ">...</ruby>`, chỉ dịch văn bản thuần.
4. Giữ nguyên các tag icon như `<sprite name="...">`, `<color=...>`, `<size=...>`.
5. ĐỂ GAME TỰ ĐỘNG XUỐNG DÒNG (AUTO-WRAP): KHÔNG tự ý chèn thẻ `<br>` ở giữa câu. Chỉ dùng `<br>` khi câu có 2 đoạn văn/ý ngắt tách bạch rõ ràng.
6. Trả về kết quả đúng định dạng JSON: danh sách các object với `{{"id": "...", "vi": "câu dịch tiếng Việt"}}`.
"""

def call_gemini_api(api_key, model_name, prompt, system_instruction):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.3,
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            candidates = data.get("candidates", [])
            if candidates:
                text_content = candidates[0]["content"]["parts"][0]["text"]
                return text_content
    except urllib.error.HTTPError as e:
        print(f"[!] Gemini API Error: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[!] Error calling Gemini: {e}")
    return None

def call_openai_compatible_api(api_key, base_url, model_name, prompt, system_instruction):
    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        print(f"[!] API Error: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[!] Error calling OpenAI API: {e}")
    return None

def translate_batch(entries, provider, api_key, model_name, base_url, system_instruction):
    prompt_items = []
    for e in entries:
        prompt_items.append({
            "id": e["id"],
            "speaker": e.get("speaker_tag", ""),
            "ja": e.get("ja", ""),
            "zh": e.get("zh", ""),
            "objection_links": e.get("objection_links", [])
        })
        
    user_prompt = f"Hãy dịch các câu thoại sau sang Tiếng Việt chuẩn xác:\n{json.dumps(prompt_items, ensure_ascii=False, indent=2)}\n\nTrả về JSON dạng: {{\"translations\": [{{\"id\": \"...\", \"vi\": \"...\"}}]}}"
    
    if provider == "gemini":
        res = call_gemini_api(api_key, model_name, user_prompt, system_instruction)
    else:
        res = call_openai_compatible_api(api_key, base_url, model_name, user_prompt, system_instruction)
        
    if not res:
        return {}
        
    try:
        parsed = json.loads(res)
        if isinstance(parsed, dict) and "translations" in parsed:
            return {item["id"]: item["vi"] for item in parsed["translations"] if "id" in item and "vi" in item}
        elif isinstance(parsed, list):
            return {item["id"]: item["vi"] for item in parsed if "id" in item and "vi" in item}
        elif isinstance(parsed, dict):
            # sometimes model returns { "id1": "vi text", "id2": "vi text" }
            return {k: v for k, v in parsed.items() if isinstance(v, str)}
    except Exception as e:
        print(f"[!] Failed to parse JSON response: {e}\nResponse was:\n{res[:300]}")
    return {}

def process_file(json_file, provider, api_key, model_name, base_url, system_instruction, batch_size=30, force=False):
    filepath = os.path.join(DIALOGUES_DIR, json_file)
    if not os.path.exists(filepath):
        print(f"[!] File not found: {filepath}")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        file_data = json.load(f)
        
    entries = file_data.get("entries", [])
    untranslated = [e for e in entries if force or not e.get("vi")]
    
    if not untranslated:
        print(f"[*] File {json_file} is already 100% translated. Skipping.")
        return True
        
    print(f"[*] Translating {json_file}: {len(untranslated)}/{len(entries)} entries needed...")
    
    for i in range(0, len(untranslated), batch_size):
        batch = untranslated[i:i+batch_size]
        print(f"  [>] Processing batch {i//batch_size + 1}/{(len(untranslated)-1)//batch_size + 1} ({len(batch)} lines)...")
        
        translated_map = translate_batch(batch, provider, api_key, model_name, base_url, system_instruction)
        
        for e in entries:
            if e["id"] in translated_map:
                e["vi"] = translated_map[e["id"]]
                
        # Save after every batch
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)
            
        time.sleep(1) # Rate limit delay
        
    print(f"[SUCCESS] Finished translating {json_file}.")
    return True

def main():
    parser = argparse.ArgumentParser(description="AI Translation Engine for Mahou Shoujo no Majo Saiban")
    parser.add_argument("--file", type=str, help="Specific JSON file to translate (e.g. Act01_Chapter01_Adv03.json)")
    parser.add_argument("--chapter", type=str, help="Prefix of chapter to translate (e.g. Act01_Chapter01)")
    parser.add_argument("--all", action="store_true", help="Translate all files")
    parser.add_argument("--provider", type=str, default="gemini", choices=["gemini", "openai", "deepseek"], help="API Provider")
    parser.add_argument("--model", type=str, default="gemini-2.0-flash", help="Model name")
    parser.add_argument("--key", type=str, help="API Key (or set via environment variable GEMINI_API_KEY / OPENAI_API_KEY)")
    parser.add_argument("--base-url", type=str, default="https://api.openai.com/v1", help="Base URL for OpenAI-compatible API")
    parser.add_argument("--force", action="store_true", help="Re-translate already translated entries")
    
    args = parser.parse_args()
    
    api_key = args.key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("[!] No API key provided. Please pass --key <YOUR_API_KEY> or set GEMINI_API_KEY / OPENAI_API_KEY in environment.")
        return
        
    if args.provider == "deepseek":
        args.provider = "openai"
        args.base_url = "https://api.deepseek.com"
        if not args.model or args.model == "gemini-2.0-flash":
            args.model = "deepseek-chat"

    context_bible = load_context_bible()
    system_instruction = SYSTEM_PROMPT_TEMPLATE.format(context_bible=context_bible)
    
    manifest_path = os.path.join(DIALOGUES_DIR, "_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    all_files = []
    for bundle_files in manifest.values():
        for item in bundle_files:
            all_files.append(item["file"])
            
    if args.file:
        process_file(args.file, args.provider, api_key, args.model, args.base_url, system_instruction, force=args.force)
    elif args.chapter:
        matching = [f for f in all_files if f.startswith(args.chapter)]
        print(f"[*] Found {len(matching)} files for chapter {args.chapter}")
        for f in matching:
            process_file(f, args.provider, api_key, args.model, args.base_url, system_instruction, force=args.force)
    elif args.all:
        for f in all_files:
            process_file(f, args.provider, api_key, args.model, args.base_url, system_instruction, force=args.force)
    else:
        print("Please specify --file <file.json>, --chapter <chapter_name>, or --all")

if __name__ == "__main__":
    main()
