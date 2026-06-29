import asyncio
import uuid
import random
import sys
import os
from datetime import datetime, timedelta, UTC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.db.session import AsyncSessionLocal, engine
from app.db.base_class import Base

# Import all models
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User
from app.models.asset import Asset, AssetType, AssetCriticality, AssetStatus
from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.case import Case, CaseStatus, CaseSeverity
from app.models.case_activity import CaseTimeline, TimelineEventType
from app.models.investigation import Investigation, InvestigationStatus
from app.models.threat_intel import ThreatIndicator, IndicatorType
from app.models.malware_sample import MalwareSample, MalwareVerdict
from app.models.playbook import Playbook, PlaybookStatus
from app.models.audit_log import AuditLog
from app.models.api_key import ApiKey
from app.core.security import get_password_hash

try:
    from faker import Faker
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Faker"])
    from faker import Faker

fake = Faker()

async def clear_data(session):
    print("Clearing existing data...")
    tables = [
        "audit_logs", "case_timeline", "investigations", "malware_samples", 
        "threat_indicators", "playbooks", "alerts", "cases", "assets", 
        "user", "roles", "organizations"
    ]
    for table in tables:
        await session.execute(text(f'TRUNCATE TABLE "{table}" CASCADE;'))
    await session.commit()

async def seed_data():
    async with AsyncSessionLocal() as session:
        await clear_data(session)

        print("Seeding Organizations & Roles...")
        org_id = uuid.uuid4()
        org = Organization(id=org_id, name="Stark Industries", description="Global Defense Contractor")
        
        role_admin_id = uuid.uuid4()
        role_admin = Role(id=role_admin_id, name="Admin", permissions=["read", "write", "admin"])
        
        role_analyst_id = uuid.uuid4()
        role_analyst = Role(id=role_analyst_id, name="Analyst", permissions=["read", "write"])
        
        session.add_all([org, role_admin, role_analyst])
        await session.commit()

        print("Seeding Users...")
        users = []
        hashed_pw = get_password_hash("password123")
        for i in range(10):
            user = User(
                id=uuid.uuid4(),
                email=f"analyst{i}@stark.com" if i > 0 else "admin@stark.com",
                hashed_password=hashed_pw,
                full_name=fake.name(),
                is_active=True,
                is_superuser=(i == 0),
                role="ADMIN" if i == 0 else "ANALYST",
                organization_id=org_id,
                role_id=role_admin_id if i == 0 else role_analyst_id
            )
            users.append(user)
        session.add_all(users)
        await session.commit()

        print("Seeding Assets...")
        assets = []
        asset_types = list(AssetType)
        asset_criticalities = list(AssetCriticality)
        for i in range(150):
            asset = Asset(
                id=uuid.uuid4(),
                hostname=f"stark-{fake.word()}-{i}",
                ip_address=fake.ipv4(),
                mac_address=fake.mac_address(),
                asset_type=random.choice(asset_types),
                criticality=random.choice(asset_criticalities),
                status=AssetStatus.ACTIVE,
                os_type=random.choice(["Windows", "Linux", "macOS"]),
                os_version=random.choice(["10", "11", "Ubuntu 22.04", "Sonoma"]),
                risk_score=random.randint(0, 100)
            )
            assets.append(asset)
        session.add_all(assets)
        await session.commit()

        print("Seeding Playbooks...")
        playbooks = []
        for i in range(15):
            playbook = Playbook(
                id=uuid.uuid4(),
                name=f"Playbook: {fake.catch_phrase()}",
                description=fake.text(),
                trigger_type=random.choice(["ON_ALERT_CREATED", "ON_CASE_UPDATED", "MANUAL"]),
                status=PlaybookStatus.ACTIVE
            )
            playbooks.append(playbook)
        session.add_all(playbooks)
        await session.commit()

        print("Seeding Threat Intel IOCs...")
        iocs = []
        for i in range(300):
            ioc = ThreatIndicator(
                id=uuid.uuid4(),
                value=fake.ipv4() if random.random() > 0.5 else fake.domain_name(),
                type=random.choice([IndicatorType.IP, IndicatorType.DOMAIN]),
                source=random.choice(["CrowdStrike", "AlienVault", "Custom"]),
                severity=random.choice([AlertSeverity.HIGH, AlertSeverity.CRITICAL, AlertSeverity.MEDIUM]),
                confidence=random.randint(50, 100),
                is_active=True
            )
            iocs.append(ioc)
        session.add_all(iocs)
        await session.commit()

        print("Seeding Malware Samples...")
        malware = []
        verdicts = [MalwareVerdict.MALICIOUS, MalwareVerdict.SUSPICIOUS, MalwareVerdict.UNKNOWN]
        for i in range(40):
            sample = MalwareSample(
                id=uuid.uuid4(),
                file_name=f"sample_{i}.exe",
                file_size=random.randint(1000, 5000000),
                md5=fake.md5(),
                sha1=fake.sha1(),
                sha256=fake.sha256(),
                verdict=random.choice(verdicts)
            )
            malware.append(sample)
        session.add_all(malware)
        await session.commit()

        print("Seeding Cases and Alerts...")
        cases = []
        alerts = []
        for i in range(120):
            case = Case(
                id=uuid.uuid4(),
                title=f"Incident: {fake.bs()}",
                description=fake.text(),
                status=random.choice(list(CaseStatus)),
                severity=random.choice(list(CaseSeverity)),
                priority=random.randint(1, 5),
                assigned_to_id=random.choice(users).id,
                created_by_id=random.choice(users).id
            )
            cases.append(case)

            for _ in range(random.randint(1, 5)):
                alert = Alert(
                    id=uuid.uuid4(),
                    title=f"Alert: {fake.catch_phrase()}",
                    description=fake.text(),
                    severity=random.choice(list(AlertSeverity)),
                    status=AlertStatus.IN_PROGRESS,
                    source=random.choice(["CrowdStrike", "Splunk", "Defender"]),
                    source_ip=random.choice(assets).ip_address,
                    case_id=case.id,
                    mitre_tactic=random.choice(["Initial Access", "Execution", "Persistence"]),
                    mitre_technique=random.choice(["T1078", "T1059", "T1098"])
                )
                alerts.append(alert)

        session.add_all(cases)
        session.add_all(alerts)
        await session.commit()
        
        # Add a few unlinked alerts
        unlinked_alerts = []
        for _ in range(140):
             alert = Alert(
                id=uuid.uuid4(),
                title=f"Alert: {fake.catch_phrase()}",
                description=fake.text(),
                severity=random.choice(list(AlertSeverity)),
                status=AlertStatus.NEW,
                source=random.choice(["CrowdStrike", "Splunk", "Defender"]),
                source_ip=random.choice(assets).ip_address,
                case_id=None,
                mitre_tactic=random.choice(["Initial Access", "Execution", "Persistence"]),
                mitre_technique=random.choice(["T1078", "T1059", "T1098"])
            )
             unlinked_alerts.append(alert)
        session.add_all(unlinked_alerts)
        await session.commit()

        print("Seeding Investigations & Timeline...")
        investigations = []
        activities = []
        for case in cases:
            inv = Investigation(
                id=uuid.uuid4(),
                case_id=case.id,
                title=f"Investigation for {case.title}",
                status=random.choice(list(InvestigationStatus)),
                findings={"notes": fake.text()}
            )
            investigations.append(inv)
            
            for _ in range(random.randint(0, 2)):
                act = CaseTimeline(
                    id=uuid.uuid4(),
                    case_id=case.id,
                    actor_id=random.choice(users).id,
                    event_type=random.choice(list(TimelineEventType)),
                    description=fake.sentence()
                )
                activities.append(act)
                
        session.add_all(investigations)
        session.add_all(activities)
        await session.commit()

        print("Seeding Audit Logs...")
        logs = []
        for i in range(1000):
            log = AuditLog(
                id=uuid.uuid4(),
                user_id=random.choice(users).id,
                action=random.choice(["CREATE", "UPDATE", "DELETE", "LOGIN"]),
                entity_type=random.choice(["ALERT", "CASE", "ASSET", "USER"]),
                entity_id=str(uuid.uuid4()),
                ip_address=fake.ipv4()
            )
            logs.append(log)
        session.add_all(logs)
        await session.commit()

        print("Database seeding completed successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
