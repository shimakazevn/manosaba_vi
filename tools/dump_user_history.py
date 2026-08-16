import json
import sys

transcript_path = r'C:\Users\Shimakaze\.gemini\antigravity\brain\0a5b7075-667b-4b86-a07c-d61a49098dec\.system_generated\logs\transcript.jsonl'

with open("tools/user_history.txt", "w", encoding="utf-8") as out:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            if data.get('type') == 'USER_INPUT':
                content = data.get('content', '')
                out.write(f"=== [Step {data.get('step_index')}] USER_INPUT ===\n")
                out.write(content + "\n\n")

