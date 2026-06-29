import requests
import sys
import json
from uuid import uuid4

BASE_URL = "http://localhost:8000/api/v1"

session = requests.Session()

def login():
    res = session.post(f"{BASE_URL}/auth/login", data={"username": "admin@stark.com", "password": "password123"})
    if res.status_code != 200:
        print("LOGIN FAILED", res.text)
        sys.exit(1)
    token = res.json()["access_token"]
    session.headers.update({"Authorization": f"Bearer {token}"})
    print("Login OK")

def test_cases():
    print("--- Testing Cases CRUD ---")
    res = session.get(f"{BASE_URL}/cases")
    if res.status_code != 200:
        print("List cases failed:", res.text)
        return
    
    new_case = {
        "title": "Suspicious Login Activity",
        "description": "Multiple failed login attempts from unknown IP",
        "severity": "HIGH",
        "priority": "HIGH",
        "status": "OPEN",
        "tags": ["brute_force", "identity"]
    }
    res = session.post(f"{BASE_URL}/cases", json=new_case)
    if res.status_code != 201:
        print("Create Case Failed:", res.status_code, res.text)
    else:
        case_id = res.json()["id"]
        print(f"Created Case: {case_id}")
        
        res = session.get(f"{BASE_URL}/cases/{case_id}")
        if res.status_code != 200: print("View Case Failed:", res.text)
        
        res = session.patch(f"{BASE_URL}/cases/{case_id}", json={"status": "INVESTIGATING", "severity": "CRITICAL"})
        if res.status_code != 200: print("Edit Case Failed:", res.text)
        
        res = session.delete(f"{BASE_URL}/cases/{case_id}")
        if res.status_code not in (200, 204, 403, 405, 404): print("Delete Case returned unexpected:", res.status_code, res.text)

def test_alerts():
    print("--- Testing Alerts ---")
    res = session.get(f"{BASE_URL}/alerts")
    if res.status_code != 200:
        print("List alerts failed:", res.text)
        return
    
    items = res.json()["items"]
    if items:
        alert_id = items[0]["id"]
        r = session.get(f"{BASE_URL}/alerts/{alert_id}")
        if r.status_code != 200: print("View alert failed:", r.text)
        r = session.patch(f"{BASE_URL}/alerts/{alert_id}", json={"status": "ACKNOWLEDGED"})
        if r.status_code != 200: print("Edit alert failed:", r.text)

def test_threat_intel():
    print("--- Testing Threat Intel ---")
    new_ioc = {
        "type": "IP_ADDRESS",
        "value": "198.51.100.12",
        "severity": "HIGH",
        "confidence": 85,
        "source": "Custom Upload"
    }
    res = session.post(f"{BASE_URL}/threat-intel/indicators", json=new_ioc)
    if res.status_code != 201:
        print("Create IOC Failed:", res.text)
    else:
        ioc_id = res.json()["id"]
        print("Created IOC:", ioc_id)
        r = session.patch(f"{BASE_URL}/threat-intel/indicators/{ioc_id}", json={"severity": "CRITICAL"})
        if r.status_code != 200: print("Edit IOC failed:", r.text)
        
        r = session.delete(f"{BASE_URL}/threat-intel/indicators/{ioc_id}")
        if r.status_code not in (200, 204, 405, 403): print("Delete IOC returned:", r.status_code, r.text)


if __name__ == "__main__":
    login()
    test_cases()
    test_alerts()
    test_threat_intel()
    print("Phase 1 Tests Completed.")
