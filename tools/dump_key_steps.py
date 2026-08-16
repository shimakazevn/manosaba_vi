import json

transcript_path = r'C:\Users\Shimakaze\.gemini\antigravity\brain\0a5b7075-667b-4b86-a07c-d61a49098dec\.system_generated\logs\transcript.jsonl'

steps_to_check = [0, 1, 2, 430, 450, 451, 1153, 1171, 1172, 1185, 1186]

with open("tools/key_steps.txt", "w", encoding="utf-8") as out:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            idx = data.get('step_index')
            stype = data.get('type')
            if idx in steps_to_check or (stype == 'PLANNER_RESPONSE' and idx in [1, 2, 451, 452, 1172]):
                content = data.get('content', '')
                out.write(f"=== [Step {idx}] {stype} ===\n")
                out.write(str(content)[:2000] + "\n\n")
