# 05 – Remediation Roadmap

Phases come from each subcategory's **Priority Score** (Gap × Business Priority weight). See [02-methodology.md](02-methodology.md). Several recommendations depend on each other, so they are grouped below into workstreams.

| Phase | Timeline | Subcategories | Projected average maturity on completion |
|---|---|---|---|
| Baseline | Today | – | 1.62 |
| Phase 1 | 0–90 days | 22 | 2.09 |
| Phase 2 | 3–6 months | 44 | 2.80 |
| Phase 3 | 6–12 months | 25 | 3.05 (target) |

---

## Phase 1: Foundations (0–90 days), 22 items

### Workstream A: Risk management foundation
| ID | Action | Owner | Done when |
|---|---|---|---|
| GV.RM-01 | Define risk management objectives; obtain executive sign-off | CISO | Signed objectives document |
| GV.RM-02 | Run a risk appetite workshop; publish risk appetite and tolerance statement | CEO / CISO | Board-approved statement |
| GV.RM-06 | Adopt a 5x5 likelihood/impact method; launch a central risk register | GRC | Register live with top 20 risks scored |
| ID.RA-05 | Perform an enterprise cyber risk assessment (NIST SP 800-30) | GRC | Assessment report and updated register |
| GV.OC-03 | Build a legal/regulatory obligations register mapped to controls | Legal / GRC | Register covering HIPAA, BAAs, state laws, contracts |

### Workstream B: Third-party risk management (TPRM)
| ID | Action | Owner | Done when |
|---|---|---|---|
| GV.SC-01 | Approve TPRM charter, policy, and procedure | GRC / Procurement | Policy approved |
| GV.SC-04 | Inventory all vendors; tier them by data access and criticality | Procurement | Tiered inventory of ~140 vendors |
| GV.SC-06 / ID.RA-10 | Require security due diligence before onboarding critical and high vendors | GRC | Intake workflow enforced in procurement |
| GV.SC-05 | Add security clauses to vendor contract templates | Legal | Updated MSA and DPA templates |
| GV.SC-07 | Assess the top 15 critical vendors; schedule annual reassessments | GRC | Assessments complete |
| GV.SC-03 | Record vendor risks in the central risk register | GRC | Vendor risks visible in the register |

### Workstream C: Know and protect PHI
| ID | Action | Owner | Done when |
|---|---|---|---|
| ID.AM-07 | Run data discovery; build a PHI/PII data inventory | Security Eng. / Privacy | Inventory covering all production data stores |
| ID.AM-05 | Classify assets by sensitivity and criticality | GRC | Classification applied to systems inventory |
| PR.AA-05 | Remove standing AWS admin; implement just-in-time access and quarterly reviews | Security Eng. | Zero standing admins; first review complete |

### Workstream D: Incident readiness
| ID | Action | Owner | Done when |
|---|---|---|---|
| ID.IM-04 / RS.MA-01 | Rewrite the IR plan to NIST SP 800-61 Rev. 3 with roles and third-party contacts (counsel, forensics, insurer) | Security Ops | Approved plan; tabletop scheduled |
| DE.AE-08 | Define incident declaration criteria and severity levels | Security Ops | Criteria included in IR plan |
| DE.AE-02 | Write triage runbooks for the top 10 alert types | Security Ops | 10 runbooks published |
| RS.CO-02 | Create breach notification procedure, templates, and contact lists | Legal / Privacy | Templates approved by counsel |
| RC.RP-01 | Develop a DR plan aligned with the IR plan | IT Ops / Cloud Eng. | Approved DR plan |
| RC.RP-03 | Add backup integrity verification to the restore procedure | Cloud Eng. | Procedure updated and tested |

---

## Phase 2: Build out the program (3–6 months), 44 items

| Workstream | Key actions | Subcategories |
|---|---|---|
| **Governance and oversight** | Executive risk review; risk response policy; complete and approve the policy suite with annual review; define KPIs/KRIs; quarterly board briefing; strategy reviews | GV.RM-03, GV.RM-04, GV.PO-01, GV.PO-02, GV.OV-01–03, GV.RR-01 |
| **TPRM maturity** | Shared responsibility matrix; vendor offboarding checklist; supplier services inventory; monitor third-party access and OAuth grants | GV.SC-02, GV.SC-10, ID.AM-04, DE.CM-06 |
| **Asset and risk management** | Internal dependency mapping (BIA input); AWS tagging and SaaS discovery; PHI data flow diagrams; risk treatment tracking; remediation register; vulnerability disclosure policy | GV.OC-05, ID.AM-02, ID.AM-03, ID.RA-04, ID.RA-06, ID.IM-01, ID.RA-08 |
| **Detection (SIEM)** | Deploy SIEM or MDR; centralize logs with 1-year retention; route GuardDuty findings; monitor identity logs; container runtime security; severity matrix | PR.PS-04, DE.AE-03, DE.CM-01, DE.CM-03, DE.CM-09, DE.AE-04 |
| **Incident response** | Severity classification; escalation matrix; recovery criteria; incident ticket template; evidence handling; PHI impact estimation; information sharing; containment playbooks; first tabletop exercise | RS.MA-03–05, RS.AN-06–08, RS.CO-03, RS.MI-01, ID.IM-02 |
| **Recovery** | Minimum viable operations; recovery communication plan; pre-approved public statements | RC.RP-04, RC.CO-03, RC.CO-04 |
| **Technical hardening** | Annual pen test and remediation SLAs; SSO for remaining apps and secrets vault; key rotation; immutable backups with quarterly restore tests; patch SLAs and EOL replacement; SAST and secret scanning on all repos; role-based training | ID.RA-01, PR.AA-01, PR.DS-01, PR.DS-11, PR.PS-02, PR.PS-06, PR.AT-02 |

## Phase 3: Refine and sustain (6–12 months), 25 items

| Workstream | Key actions | Subcategories |
|---|---|---|
| **Governance refinements** | Stakeholder register; customer-facing services mapping; escalation paths; opportunity discussion; RACI; risk-based budgeting; vendor KPIs; vendors included in IR planning | GV.OC-02, GV.OC-04, GV.RM-05, GV.RM-07, GV.RR-02, GV.RR-03, GV.SC-08, GV.SC-09 |
| **Identify refinements** | Life cycle procedures; Health-ISAC membership and KEV feed; threat profile; formal exception process; SBOM and artifact signing; security postmortems | ID.AM-08, ID.RA-02, ID.RA-03, ID.RA-07, ID.RA-09, ID.IM-03 |
| **Protect refinements** | PHI masking in logs; CIS hardening baselines; remove local admin | PR.DS-10, PR.PS-01, PR.PS-05 |
| **Detect and respond operations** | On-call paging; threat intel enrichment; triage rotation; root cause analysis for SEV1/2; eradication steps in playbooks | DE.AE-06, DE.AE-07, RS.MA-02, RS.AN-03, RS.MI-02 |
| **Recovery refinements** | Restoration priority order; IOC sweep before go-live; recovery closure criteria | RC.RP-02, RC.RP-05, RC.RP-06 |

---

## Resource and budget considerations (estimates)

| Need | Rationale |
|---|---|
| +1 GRC/TPRM analyst | TPRM workstream and risk register operations |
| SIEM or MDR service | No 24x7 coverage with a four-person team; MDR is usually more cost-effective at this size |
| GRC platform (optional) | Automates evidence collection for SOC 2 and vendor assessments |
| Third-party pen test | Annual requirement for customers and SOC 2 |
| Outside counsel and IR retainer | Pre-arranged support for breach response |

## Governance of the roadmap

- **Monthly:** The GRC analyst reports roadmap progress and KPIs to the CISO.
- **Quarterly:** The CISO briefs the executive team and board, and maturity scores are re-assessed.
- **Annually:** Full CSF 2.0 re-assessment; the target profile is updated as the business changes.

## Success metrics

| KPI | Baseline | 6-month target | 12-month target |
|---|---|---|---|
| Average CSF maturity | 1.62 | 2.80 | 3.05 |
| Critical vendors assessed | 0% | 100% | 100% (annual) |
| Standing privileged AWS accounts | 12 | 0 | 0 |
| IR tabletop exercises completed | 0 | 1 | 2 |
| Log retention (days) | 14 | 365 | 365 |
| Restore tests performed | 1 (2024) | 2 | Quarterly |
| Policies reviewed within 12 months | 0% | 100% | 100% |
