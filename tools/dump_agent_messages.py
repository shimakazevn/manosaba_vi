import json

transcript_path = r'C:\Users\Shimakaze\.gemini\antigravity\brain\0a5b7075-667b-4b86-a07c-d61a49098dec\.system_generated\logs\transcript.jsonl'

with open("tools/agent_messages.txt", "w", encoding="utf-8") as out:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            idx = data.get('step_index')
            stype = data.get('type')
            content = data.get('content', '')
            # If there's content text in planner response
            if stype == 'PLANNER_RESPONSE' and content:
                out.write(f"=== [Step {idx}] AGENT RESPONSE ===\n")
                out.write(str(content) + "\n\n")
            elif stype == 'USER_INPUT':
                out.write(f"=== [Step {idx}] USER INPUT ===\n")
                out.write(str(content) + "\n\n")
