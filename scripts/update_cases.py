import re

with open(r"x:\Sentrix\frontend\app\cases\page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Remove MockCase interface
content = re.sub(r'interface MockCase extends Case \{.*?\}', '', content, flags=re.DOTALL)

# Replace mc with c and MockCase with Case
content = content.replace("const mc = c as MockCase;", "const mc = c as any; // fallback")
content = content.replace("as MockCase", "as Case")
content = content.replace("<CaseExpanded c={found}", "<CaseExpanded c={found as any}")

with open(r"x:\Sentrix\frontend\app\cases\page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
