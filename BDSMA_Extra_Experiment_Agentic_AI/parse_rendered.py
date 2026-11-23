with open('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/rendered_streamlit.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
tabs = re.findall(r'<button[^>]*role="tab"[^>]*>.*?</button>', html, re.DOTALL)
print(f"Role='tab' buttons found: {len(tabs)}")
for t in tabs:
    clean = re.sub(r'<[^>]+>', ' ', t).strip()
    print("Tab label:", clean)

if not tabs:
    # Check if there is an exception or error message in html
    errors = re.findall(r'<div[^>]*class="[^"]*stException[^"]*"[^>]*>.*?</div>', html, re.DOTALL)
    print(f"stException found: {len(errors)}")
    for e in errors:
        print("Error:", e[:200])
