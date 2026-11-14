# 02 – Assessment Methodology

## 1. Framework

The assessment uses the **NIST Cybersecurity Framework (CSF) 2.0** (NIST CSWP 29, February 2024). CSF 2.0 organizes cybersecurity outcomes into:

| Level | Count | Example |
|---|---|---|
| Functions | 6 | Govern (GV) |
| Categories | 22 | GV.SC – Cybersecurity Supply Chain Risk Management |
| Subcategories | 106 | GV.SC-04 – Suppliers are known and prioritized by criticality |

CSF 2.0 added the **Govern** function, which covers organizational context, risk strategy, roles, policy, oversight, and supply chain risk. This assessment pays particular attention to it.

## 2. Approach

The assessment followed the CSF's own profile-based process, which compares a **Current Profile** with a **Target Profile**:

1. **Scope and context.** Confirmed business objectives, regulatory obligations, and in-scope systems (see [01-company-profile.md](01-company-profile.md)).
2. **Evidence collection.** Simulated interviews with security, IT, engineering, legal, HR, and procurement stakeholders; reviewed policies, configurations, and tool outputs.
3. **Current Profile.** Scored each of the 106 subcategories on the maturity scale below.
4. **Target Profile.** Set a target score for each subcategory based on risk, regulatory requirements, and customer expectations. Not every subcategory needs to be at the same level.
5. **Gap analysis and prioritization.** Calculated gaps and weighted them by business priority.
6. **Roadmap.** Grouped recommendations into time-bound phases with owners.

## 3. Maturity scale (0–5)

CSF 2.0 Implementation Tiers (Partial, Risk Informed, Repeatable, Adaptive) describe the organization as a whole. To score individual subcategories, this assessment uses a CMMI-style capability scale, which is common practice in CSF assessments:

| Score | Level | Description |
|---|---|---|
| 0 | Not Performed | The outcome is not achieved. No process exists. |
| 1 | Initial | Ad hoc and reactive; depends on individuals; undocumented. |
| 2 | Repeatable | Performed consistently in some areas; partially documented. |
| 3 | Defined | Documented, approved, and applied consistently across the organization. |
| 4 | Managed | Measured with metrics, monitored, and enforced. |
| 5 | Optimized | Continuously improved and automated where practical. |

**Target-setting rationale.** Level 3 (Defined) is the baseline target for most subcategories; it is what a SOC 2 Type II audit and HIPAA Security Rule compliance realistically require. Level 4 (Managed) was set where PHI exposure or regulatory obligations make measurement and enforcement essential: regulatory obligations (GV.OC-03), data inventory (ID.AM-07), vulnerability management (ID.RA-01), IR planning (ID.IM-04), identity and access (PR.AA-01, PR.AA-03, PR.AA-05), data protection and backups (PR.DS-01, PR.DS-02, PR.DS-11), and breach notification (RS.CO-02). Environmental protection (PR.IR-02) is also at level 4 because it is inherited from AWS. A small number of lower-risk subcategories target level 2.

## 4. Prioritization

Each gap is weighted by business priority to produce a **Priority Score**:

```
Gap            = Target Maturity − Current Maturity
Priority Score = Gap × Business Priority Weight     (High = 3, Medium = 2, Low = 1)
```

Business priority reflects PHI exposure, regulatory requirements, customer contract requirements, and dependence of other controls on the outcome (for example, a risk register is a prerequisite for many other Govern and Identify outcomes).

| Priority Score | Roadmap Phase |
|---|---|
| 6 or higher | **Phase 1** – 0 to 90 days |
| 3 to 5 | **Phase 2** – 3 to 6 months |
| 1 to 2 | **Phase 3** – 6 to 12 months |
| 0 | **Maintain** – no gap; sustain current practice |

## 5. Tooling

- `data/csf2_assessment.csv` – the scored assessment (one row per subcategory).
- `scripts/analyze.py` – validates the data (106 unique subcategories, scores in range, target >= current), calculates gaps, priority scores, and phases, and produces the summary tables and charts in `outputs/`.

## 6. Limitations

- The organization and evidence are simulated for portfolio purposes.
- Maturity scores reflect assessor judgment; a real engagement would validate them with evidence sampling and stakeholder review.
- Averages by function and category treat every subcategory equally. The Priority Score is what drives the roadmap.
