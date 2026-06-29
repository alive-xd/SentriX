const BASE_URL = "http://localhost:8000/api/v1";

async function main() {
    // Login
    let res = await fetch(`${BASE_URL}/auth/login`, {
        method: "POST",
        body: new URLSearchParams({username: "admin@stark.com", password: "password123"})
    });
    if (!res.ok) { console.error("LOGIN FAILED", await res.text()); process.exit(1); }
    const token = (await res.json()).access_token;
    const h = { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" };
    console.log("Login OK");

    // Cases CRUD
    console.log("--- Testing Cases CRUD ---");
    res = await fetch(`${BASE_URL}/cases`, {headers: h});
    if (!res.ok) console.error("List cases failed", await res.text());
    
    res = await fetch(`${BASE_URL}/cases`, {
        method: "POST", headers: h,
        body: JSON.stringify({
            title: "Suspicious Login Activity", description: "Multiple failed login attempts",
            severity: "HIGH", priority: 1, status: "OPEN", tags: ["brute_force"]
        })
    });
    if (!res.ok) { console.error("Create Case Failed", await res.text()); }
    else {
        const case_id = (await res.json()).id;
        console.log("Created Case:", case_id);
        
        res = await fetch(`${BASE_URL}/cases/${case_id}`, {headers: h});
        if (!res.ok) console.error("View Case Failed", await res.text());
        
        res = await fetch(`${BASE_URL}/cases/${case_id}`, {
            method: "PATCH", headers: h,
            body: JSON.stringify({status: "INVESTIGATING", severity: "CRITICAL"})
        });
        if (!res.ok) console.error("Edit Case Failed", await res.text());
        else console.log("Edit Case OK");
        
        res = await fetch(`${BASE_URL}/cases/${case_id}`, { method: "DELETE", headers: h });
        console.log("Delete Case Returned:", res.status);
    }

    // Alerts
    console.log("--- Testing Alerts ---");
    res = await fetch(`${BASE_URL}/alerts`, {headers: h});
    let items = (await res.json()).items;
    if (items && items.length > 0) {
        const alert_id = items[0].id;
        res = await fetch(`${BASE_URL}/alerts/${alert_id}`, {headers: h});
        if (!res.ok) console.error("View Alert Failed", await res.text());
        
        res = await fetch(`${BASE_URL}/alerts/${alert_id}`, {
            method: "PATCH", headers: h,
            body: JSON.stringify({status: "ACKNOWLEDGED"})
        });
        if (!res.ok) console.error("Edit Alert Failed", await res.text());
        else console.log("Edit Alert OK");
    }

    // Assets
    console.log("--- Testing Assets ---");
    res = await fetch(`${BASE_URL}/assets`, {headers: h});
    items = (await res.json()).items;
    if (items && items.length > 0) {
        const asset_id = items[0].id;
        res = await fetch(`${BASE_URL}/assets/${asset_id}`, {
            method: "PATCH", headers: h,
            body: JSON.stringify({criticality: "HIGH"})
        });
        if (!res.ok) console.error("Edit Asset Failed", await res.text());
        else console.log("Edit Asset OK");
    }

    // Threat Intel
    console.log("--- Testing Threat Intel ---");
    res = await fetch(`${BASE_URL}/threat-intel/indicators`, {
        method: "POST", headers: h,
        body: JSON.stringify({
            type: "IP", value: "198.51.100.12", severity: "HIGH", confidence: 85, source: "Custom"
        })
    });
    if (!res.ok) { console.error("Create IOC Failed", await res.text()); }
    else {
        const ioc_id = (await res.json()).id;
        console.log("Created IOC:", ioc_id);
        
        res = await fetch(`${BASE_URL}/threat-intel/indicators/${ioc_id}`, {
            method: "PATCH", headers: h,
            body: JSON.stringify({severity: "CRITICAL"})
        });
        if (!res.ok) console.error("Edit IOC Failed", await res.text());
        
        res = await fetch(`${BASE_URL}/threat-intel/indicators/${ioc_id}`, { method: "DELETE", headers: h });
        console.log("Delete IOC Returned:", res.status);
    }
}
main();
