import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.session import engine, SessionLocal
from app.db.base_class import Base
from app.models.user import User
from app.models.case import Case, CaseSeverity, CaseStatus
from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.asset import Asset, AssetType, Criticality, AssetStatus
from app.models.detection import DetectionRule, RuleType, RuleStatus
from app.models.threat_intel import ThreatIndicator, IndicatorType
from app.core.security import get_password_hash
import uuid

def seed():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    print("Seeding Users...")
    admin = db.query(User).filter_by(email="admin@sentrix.local").first()
    if not admin:
        admin = User(
            email="admin@sentrix.local",
            full_name="Admin User",
            hashed_password=get_password_hash("admin"),
            is_superuser=True,
            role="ADMIN"
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

    analyst = db.query(User).filter_by(email="analyst@sentrix.local").first()
    if not analyst:
        analyst = User(
            email="analyst@sentrix.local",
            full_name="SOC Analyst",
            hashed_password=get_password_hash("analyst"),
            is_superuser=False,
            role="ANALYST"
        )
        db.add(analyst)
        db.commit()
        db.refresh(analyst)

    print("Seeding Cases & Alerts...")
    if db.query(Case).count() == 0:
        c1 = Case(
            title="Suspicious PowerShell Execution on DC01",
            description="Detected obfuscated PowerShell running from unusual directory on Domain Controller.",
            severity=CaseSeverity.CRITICAL,
            status=CaseStatus.OPEN,
            priority=1,
            source="SentinelOne",
            assigned_to_id=analyst.id,
            tags=["Ransomware", "Lateral Movement", "Active Directory"]
        )
        
        c2 = Case(
            title="Multiple Failed Logins for Admin Account",
            description="Over 500 failed login attempts from external IP targeting Administrator.",
            severity=CaseSeverity.HIGH,
            status=CaseStatus.IN_PROGRESS,
            priority=2,
            source="Okta",
            assigned_to_id=analyst.id,
            tags=["Brute Force", "Identity"]
        )
        db.add_all([c1, c2])
        db.commit()
        db.refresh(c1)
        db.refresh(c2)

        alerts = [
            Alert(
                title="Invoke-Mimikatz detected in memory",
                description="PowerShell process attempted to load Mimikatz payload.",
                severity=AlertSeverity.CRITICAL,
                status=AlertStatus.NEW,
                source="CrowdStrike",
                source_ip="10.0.1.45",
                dest_ip="10.0.1.10",
                mitre_tactic="Credential Access",
                mitre_technique="T1003",
                case_id=c1.id
            ),
            Alert(
                title="Excessive Kerberos ticket requests",
                description="Potential Golden Ticket attack behavior.",
                severity=AlertSeverity.HIGH,
                status=AlertStatus.NEW,
                source="Zeek",
                mitre_tactic="Credential Access",
                mitre_technique="T1558.001",
                case_id=c1.id
            ),
            Alert(
                title="Log4j exploitation attempt blocked",
                description="WAF caught JNDI lookup string in HTTP headers.",
                severity=AlertSeverity.CRITICAL,
                status=AlertStatus.RESOLVED,
                source="Cloudflare WAF",
                source_ip="198.51.100.12",
                dest_ip="10.0.5.55",
                mitre_tactic="Initial Access"
            )
        ]
        db.add_all(alerts)
        db.commit()

    print("Seeding Assets...")
    if db.query(Asset).count() == 0:
        assets = [
            Asset(
                hostname="DC01-PROD",
                ip_address="10.0.1.10",
                os_type="Windows Server 2022",
                asset_type=AssetType.SERVER,
                criticality=Criticality.CRITICAL,
                status=AssetStatus.ACTIVE,
                owner="IT Ops"
            ),
            Asset(
                hostname="JSMITH-LT",
                ip_address="10.0.1.45",
                os_type="Windows 11",
                asset_type=AssetType.ENDPOINT,
                criticality=Criticality.MEDIUM,
                status=AssetStatus.ACTIVE,
                owner="John Smith"
            )
        ]
        db.add_all(assets)
        db.commit()

    print("Seeding Detection Rules...")
    if db.query(DetectionRule).count() == 0:
        rules = [
            DetectionRule(
                name="Suspicious PowerShell Download Cradle",
                description="Detects PowerShell downloading payloads from internet.",
                rule_type=RuleType.SIGMA,
                severity="HIGH",
                status=RuleStatus.ACTIVE,
                content="title: Suspicious PowerShell Download Cradle\nlogsource:\n  category: process_creation",
                mitre_tactic="Execution",
                mitre_technique="T1059.001"
            )
        ]
        db.add_all(rules)
        db.commit()

    print("Seeding Threat Intel...")
    if db.query(ThreatIndicator).count() == 0:
        iocs = [
            ThreatIndicator(
                type=IndicatorType.IP,
                value="198.51.100.12",
                confidence=95,
                severity="CRITICAL",
                source="AlienVault OTX",
                description="Known Cobalt Strike C2 server."
            ),
            ThreatIndicator(
                type=IndicatorType.FILE_HASH,
                value="44d88612fea8a8f36de82e1278abb02f",
                confidence=100,
                severity="HIGH",
                source="VirusTotal",
                description="WannaCry ransomware variant."
            )
        ]
        db.add_all(iocs)
        db.commit()

    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed()
