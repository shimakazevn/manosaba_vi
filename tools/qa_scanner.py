import json
import glob
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def audit_file(file_path):
    filename = os.path.basename(file_path)
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return [f"[{filename}] JSON Parse Error: {e}"]

    entries = data.get("entries", [])
    for idx, entry in enumerate(entries):
        entry_id = entry.get("id", f"idx_{idx}")
        speaker = entry.get("speaker_tag", "")
        ja = entry.get("ja", "")
        zh = entry.get("zh", "")
        vi = entry.get("vi", "")

        # 1. Empty translation
        if not vi.strip() and (ja.strip() or zh.strip()):
            issues.append(f"[{filename}] {entry_id} - EMPTY VI TRANSLATION")

        # 2. Toast anomalies
        if "@toast" in speaker:
            if len(vi) > 60:
                issues.append(f"[{filename}] {entry_id} - TOAST TOO LONG / SUSPECTED TEXT SWAP: vi='{vi[:60]}...'")

        # 3. Alisa pronouns (should use tao/mày, never tôi/mình)
        if "Alisa" in speaker or ("Alisa" in entry_id and not "Narrative" in entry_id and not "Ema" in entry_id):
            for word in [" tôi ", "^tôi ", " tôi,", " tôi.", " tôi!", " tôi?", " bọn mình ", " chúng mình "]:
                if re.search(r'\b' + re.escape(word.strip()) + r'\b', vi, re.IGNORECASE):
                    issues.append(f"[{filename}] {entry_id} (Alisa) - SUSPECTED WRONG PRONOUN in: '{vi}'")
                    break

        # 4. Coco pronouns
        if "Coco" in speaker or ("Coco" in entry_id and not "Narrative" in entry_id):
            for word in [" tôi ", "^tôi ", " tôi,", " tôi.", " tôi!", " tôi?", " chúng mình "]:
                if re.search(r'\b' + re.escape(word.strip()) + r'\b', vi, re.IGNORECASE):
                    issues.append(f"[{filename}] {entry_id} (Coco) - SUSPECTED WRONG PRONOUN in: '{vi}'")
                    break

        # 5. Leia pronouns (should NOT use rude tao/mày)
        if "Leia" in speaker or ("Leia" in entry_id and not "Narrative" in entry_id):
            for word in [" tao ", "^tao ", " tao,", " tao.", " mày ", "^mày ", " mày?", " mày!"]:
                if re.search(r'\b' + re.escape(word.strip()) + r'\b', vi, re.IGNORECASE):
                    issues.append(f"[{filename}] {entry_id} (Leia) - SUSPECTED RUDE PRONOUN for Leia in: '{vi}'")
                    break

        # 6. Tag balance check
        for tag in ["color", "size", "link", "b", "i"]:
            open_tags = len(re.findall(r'<' + tag + r'(?:=[^>]+|\s[^>]+)?>', vi, re.IGNORECASE))
            close_tags = len(re.findall(r'</' + tag + r'>', vi, re.IGNORECASE))
            if open_tags != close_tags:
                issues.append(f"[{filename}] {entry_id} - UNBALANCED TAG <{tag}>: open={open_tags}, close={close_tags} in '{vi}'")

    return issues

all_files = sorted(glob.glob("translation/dialogues/*.json"))
all_issues = []

for f in all_files:
    if "_manifest.json" in f:
        continue
    issues = audit_file(f)
    all_issues.extend(issues)

with open("tools/qa_full_report.txt", "w", encoding="utf-8") as out:
    out.write(f"Total issues found across ALL {len(all_files)} files: {len(all_issues)}\n")
    for iss in all_issues:
        out.write(iss + "\n")
        print(iss)

print(f"\nDone! Found {len(all_issues)} issues across {len(all_files)} files.")
