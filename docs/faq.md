# Frequently Asked Questions (FAQ)

### What is Sentrix?
Sentrix is an open-source Security Operations Center (SOC) platform designed for modern incident response, threat intelligence, and automation (SOAR).

### Can I use Sentrix in production?
Yes. Sentrix is built on battle-tested enterprise technologies (PostgreSQL, FastAPI, Next.js). However, we strongly recommend deploying behind a hardened reverse proxy, enforcing strict firewall rules, and using managed database services.

### Does Sentrix replace my SIEM?
Sentrix is primarily a SOAR and Case Management platform. It is designed to *ingest* alerts from your SIEM (like Elastic, Splunk, or Microsoft Sentinel) and coordinate the response.

### How do I add a new Threat Intelligence Feed?
You can create a new service module in the backend under `app/services/integrations/` and expose the configuration via environment variables.

### Is there an Enterprise version?
Sentrix is 100% open-source under the MIT license. There is no paywalled enterprise version. All features are available to the community.
