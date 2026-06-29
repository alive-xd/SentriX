from typing import List, Dict, Any
from app.schemas.ai import AIChatRequest, AIChatResponse, ReasoningStep, CodeSnippet

AI_RESPONSES = [
    {
        "trigger": ["alert", "analyze", "al-"],
        "response": {
            "content": "I've analyzed the alert and correlated it with threat intelligence. This appears to be a **Cobalt Strike Beacon** deployment attempt using a PowerShell download cradle. The destination IP has been seen in 3 prior incidents.",
            "reasoningSteps": [
                {"title": "Fetching alert details and raw log", "status": "done"},
                {"title": "Extracting process tree for PID 9021", "status": "done"},
                {"title": "Analyzing PowerShell arguments vs. known malware signatures", "status": "done", "details": "Matched: Suspicious Download Cradle (T1059.001) — confidence 94%"},
                {"title": "Correlating destination IP 198.51.100.12 with Threat Intel", "status": "done", "details": "IP found in AlienVault OTX, MISP, VirusTotal (Confidence: HIGH)"},
                {"title": "Generating YARA rule for incident", "status": "done"},
            ],
            "codeSnippet": {
                "label": "Generated YARA Rule",
                "language": "plaintext",
                "code": 'rule CobaltStrike_PowerShell_Cradle {\n  meta:\n    description = "Detects Cobalt Strike PowerShell download cradle"\n    author      = "Sentrix AI"\n    severity    = "CRITICAL"\n    mitre       = "T1059.001"\n  strings:\n    $ps1 = "powershell.exe -nop -w hidden -c" ascii nocase\n    $ps2 = "IEX (New-Object Net.WebClient).DownloadString" ascii nocase\n    $ps3 = "-EncodedCommand" ascii nocase\n  condition:\n    any of them\n}'
            }
        }
    },
    {
        "trigger": ["yara", "rule", "mimikatz", "generate"],
        "response": {
            "content": "Generated a high-confidence YARA rule for **Mimikatz** targeting the `sekurlsa` and `lsadump` modules. This rule detects both in-memory and on-disk variants with minimal false positives.",
            "reasoningSteps": [
                {"title": "Loading Mimikatz signature database", "status": "done"},
                {"title": "Extracting PE headers and string signatures", "status": "done", "details": "Found 12 unique byte patterns across 4 Mimikatz variants"},
                {"title": "Optimizing rule for low false positive rate", "status": "done", "details": "FP rate estimated at <0.1% on enterprise endpoints"},
            ],
            "codeSnippet": {
                "label": "Generated YARA Rule — Mimikatz",
                "language": "plaintext",
                "code": 'rule Mimikatz_InMemory_Sekurlsa {\n  meta:\n    description = "Detects Mimikatz sekurlsa module in memory or on disk"\n    author      = "Sentrix AI"\n    severity    = "CRITICAL"\n    mitre       = "T1003.001"\n  strings:\n    $mz        = { 4D 5A }\n    $sekurlsa  = "sekurlsa" ascii wide nocase\n    $lsadump   = "lsadump" ascii wide nocase\n    $privilege = "privilege::debug" ascii wide nocase\n    $logonpass = "logonpasswords" ascii wide nocase\n  condition:\n    $mz at 0 and 2 of ($sekurlsa, $lsadump, $privilege, $logonpass)\n}'
            }
        }
    },
    {
        "trigger": ["hunt", "ip", "ioc", "indicator"],
        "response": {
            "content": "Threat hunt complete. The IP **198.51.100.12** was observed in **3 endpoints** over the last 7 days. Network telemetry shows C2 beacon traffic patterns (periodic 60s intervals, small payloads). Recommend immediate isolation.",
            "reasoningSteps": [
                {"title": "Querying EDR telemetry for IP 198.51.100.12", "status": "done", "details": "3 unique hosts contacted this IP in the last 7 days"},
                {"title": "Analyzing beacon interval timing", "status": "done", "details": "Interval: ~60s ±3s — consistent with Cobalt Strike default"},
                {"title": "Cross-referencing with AlienVault OTX", "status": "done", "details": "Tagged: C2, Cobalt Strike — 47 threat reports"},
                {"title": "Checking DNS resolutions for reverse lookup", "status": "done", "details": "PTR: malicious-hosting.net (ASN: 12345)"},
            ]
        }
    },
    {
        "trigger": ["sigma", "kql", "detection"],
        "response": {
            "content": "Here's a **Sigma rule** that detects this attack pattern. It maps to MITRE ATT&CK T1055 (Process Injection) and has been tested against 50K+ events with a 0.2% FP rate.",
            "codeSnippet": {
                "label": "Generated Sigma Rule",
                "language": "yaml",
                "code": "title: Suspicious Process Injection via CreateRemoteThread\nid: 8a7f3d21-b4c9-4e1a-b2d4-9e3c4f5a6b7c\nstatus: experimental\nauthor: Sentrix AI\ndate: 2026/06/28\ntags:\n  - attack.defense_evasion\n  - attack.privilege_escalation\n  - attack.t1055\nlogsource:\n  category: process_creation\n  product: windows\ndetection:\n  selection:\n    EventID: 8\n    TargetImage|endswith:\n      - '\\lsass.exe'\n      - '\\svchost.exe'\n      - '\\explorer.exe'\n    SourceImage|contains:\n      - '\\temp\\'\n      - '\\appdata\\'\n  condition: selection\nlevel: high"
            }
        }
    }
]

class AIService:
    async def chat(self, request: AIChatRequest) -> AIChatResponse:
        lower_query = request.query.lower()
        for r in AI_RESPONSES:
            if any(t in lower_query for t in r["trigger"]):
                return AIChatResponse(**r["response"])
                
        return AIChatResponse(
            content=f"I've processed your request: **\"{request.query}\"**\n\nBased on current telemetry and threat intelligence, I've identified several relevant data points. Would you like me to:\n• Generate a detection rule for this threat pattern\n• Hunt for related IOCs across your environment\n• Create a case and assign it to the on-call analyst",
            reasoningSteps=[
                ReasoningStep(title="Parsing request and extracting entities", status="done"),
                ReasoningStep(title="Querying internal telemetry", status="done", details="Searched 2.4M events in the last 24h"),
                ReasoningStep(title="Cross-referencing threat intelligence feeds", status="done", details="Checked AlienVault OTX, MISP, VirusTotal"),
            ]
        )

ai_service = AIService()
