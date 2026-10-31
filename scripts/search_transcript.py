import sys, json

sys.stdout.reconfigure(encoding='utf-8')
p = r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\.system_generated\logs\transcript.jsonl'

with open(p, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('type') == 'USER_INPUT':
            step = obj.get('step_index', 0)
            content = obj.get('content', '')
            if 3000 <= step <= 4550:
                print(f"Step {step}: {content}")
