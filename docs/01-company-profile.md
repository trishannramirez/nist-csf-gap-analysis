# 01 – Company Profile: Bluefin Health Analytics, Inc.

> **Fictional organization.** Bluefin Health Analytics is invented for this portfolio project. Any resemblance to a real company is coincidental.

## Business overview

| Attribute | Detail |
|---|---|
| Industry | Healthcare technology (B2B SaaS) |
| Product | A cloud platform that helps mid-sized hospitals and clinic groups analyze patient flow, readmission risk, and staffing |
| Employees | 220 (Engineering 85, Sales and Customer Success 60, G&A 45, Product 30) |
| Funding stage | Series C |
| Customers | ~140 hospitals and clinic groups in the United States |
| Data handled | Protected Health Information (PHI) from customer EHR integrations, customer employee data, and internal employee PII |
| Regulatory drivers | HIPAA Security and Privacy Rules (Bluefin is a **Business Associate**), state breach notification laws, contractual Business Associate Agreements (BAAs) |
| Customer drivers | Large health systems now require a SOC 2 Type II report and completed security questionnaires before signing |

## Technology environment

| Area | Tools and services |
|---|---|
| Cloud hosting | AWS (multi-AZ, single region): EKS, RDS (PostgreSQL), S3 |
| Identity | Okta SSO with MFA, provisioned from the HR system |
| Productivity | Google Workspace, Slack |
| Endpoints | macOS laptops managed by MDM, EDR on all laptops |
| Engineering | GitHub, Terraform, GitHub Actions CI/CD, Dependabot |
| Security tooling | AWS GuardDuty, AWS Inspector, security awareness training platform |
| SaaS footprint | ~140 third-party SaaS vendors |

## Security organization

- A **Head of Security** (acting CISO) reports to the CTO.
- Team of four: acting CISO, two security engineers, one GRC analyst.
- There is no 24x7 security operations center and no on-call security rotation.
- The board of directors does not receive regular cybersecurity reporting.

## Why this assessment was commissioned

1. **Sales pressure.** Two large health-system deals stalled because Bluefin could not provide a SOC 2 report or answer vendor risk questionnaires with confidence.
2. **Regulatory exposure.** As a HIPAA Business Associate, Bluefin is directly liable for Security Rule compliance and breach notification.
3. **Threat environment.** Healthcare is consistently among the most targeted industries for ransomware, and third-party breaches at healthcare vendors have caused major outages across the sector.
4. **Board request.** The board asked leadership for a baseline of cybersecurity maturity and a funded plan to improve it.

## Assessment scope

- **In scope:** All six NIST CSF 2.0 Functions (Govern, Identify, Protect, Detect, Respond, Recover), all 22 Categories and all 106 Subcategories, across corporate IT and the production SaaS platform.
- **Out of scope:** Customer-hosted components, physical security of customer sites, and detailed technical testing (penetration testing is recommended as a follow-up).
