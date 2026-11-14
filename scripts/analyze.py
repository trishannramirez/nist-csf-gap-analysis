"""
NIST CSF 2.0 Gap Assessment - analysis script

Reads the subcategory-level assessment (data/csf2_assessment.csv), validates it,
computes gaps and priority scores, assigns remediation phases, and writes
summary tables and charts to outputs/.

Usage (from the repository root):
    pip install -r scripts/requirements.txt
    python scripts/analyze.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "csf2_assessment.csv"
OUT = ROOT / "outputs"

FUNCTIONS = {
    "GV": "Govern",
    "ID": "Identify",
    "PR": "Protect",
    "DE": "Detect",
    "RS": "Respond",
    "RC": "Recover",
}

CATEGORIES = {
    "GV.OC": "Organizational Context",
    "GV.RM": "Risk Management Strategy",
    "GV.RR": "Roles, Responsibilities, and Authorities",
    "GV.PO": "Policy",
    "GV.OV": "Oversight",
    "GV.SC": "Cybersecurity Supply Chain Risk Management",
    "ID.AM": "Asset Management",
    "ID.RA": "Risk Assessment",
    "ID.IM": "Improvement",
    "PR.AA": "Identity Management, Authentication, and Access Control",
    "PR.AT": "Awareness and Training",
    "PR.DS": "Data Security",
    "PR.PS": "Platform Security",
    "PR.IR": "Technology Infrastructure Resilience",
    "DE.CM": "Continuous Monitoring",
    "DE.AE": "Adverse Event Analysis",
    "RS.MA": "Incident Management",
    "RS.AN": "Incident Analysis",
    "RS.CO": "Incident Response Reporting and Communication",
    "RS.MI": "Incident Mitigation",
    "RC.RP": "Incident Recovery Plan Execution",
    "RC.CO": "Incident Recovery Communication",
}

MATURITY_LEVELS = {
    0: "Not Performed",
    1: "Initial",
    2: "Repeatable",
    3: "Defined",
    4: "Managed",
    5: "Optimized",
}

PRIORITY_WEIGHT = {"High": 3, "Medium": 2, "Low": 1}

# Colors (validated reference palette, light mode)
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
CURRENT = "#2a78d6"   # categorical slot 1
TARGET = "#eb6834"    # categorical slot 2


def phase_for(score: int) -> str:
    """Map a priority score (gap x business weight) to a roadmap phase."""
    if score >= 6:
        return "Phase 1 (0-90 days)"
    if score >= 3:
        return "Phase 2 (3-6 months)"
    if score >= 1:
        return "Phase 3 (6-12 months)"
    return "Maintain"


def load_and_validate() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    errors = []
    if len(df) != 106:
        errors.append(f"Expected 106 subcategories, found {len(df)}")
    if df["Subcategory_ID"].duplicated().any():
        errors.append("Duplicate subcategory IDs found")
    for col in ("Current_Maturity", "Target_Maturity"):
        if not df[col].between(0, 5).all():
            errors.append(f"{col} must be between 0 and 5")
    if (df["Target_Maturity"] < df["Current_Maturity"]).any():
        errors.append("Target maturity is below current maturity for some rows")
    if not df["Business_Priority"].isin(PRIORITY_WEIGHT).all():
        errors.append("Business_Priority must be High, Medium, or Low")
    if errors:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(errors))
    return df


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Function"] = df["Subcategory_ID"].str[:2].map(FUNCTIONS)
    df["Category_ID"] = df["Subcategory_ID"].str.split("-").str[0]
    df["Category"] = df["Category_ID"].map(CATEGORIES)
    df["Current_Level"] = df["Current_Maturity"].map(MATURITY_LEVELS)
    df["Target_Level"] = df["Target_Maturity"].map(MATURITY_LEVELS)
    df["Gap"] = df["Target_Maturity"] - df["Current_Maturity"]
    df["Priority_Score"] = df["Gap"] * df["Business_Priority"].map(PRIORITY_WEIGHT)
    df["Roadmap_Phase"] = df["Priority_Score"].apply(phase_for)
    cols = [
        "Function", "Category_ID", "Category", "Subcategory_ID", "Outcome",
        "Current_Maturity", "Current_Level", "Target_Maturity", "Target_Level",
        "Gap", "Business_Priority", "Priority_Score", "Roadmap_Phase",
        "Observation", "Recommendation", "Owner",
    ]
    return df[cols]


def summarize(df: pd.DataFrame, by: str) -> pd.DataFrame:
    order = list(FUNCTIONS.values()) if by == "Function" else list(CATEGORIES)
    g = df.groupby(by, sort=False).agg(
        Subcategories=("Subcategory_ID", "count"),
        Avg_Current=("Current_Maturity", "mean"),
        Avg_Target=("Target_Maturity", "mean"),
        Total_Priority_Score=("Priority_Score", "sum"),
        Phase_1_Items=("Roadmap_Phase", lambda s: (s.str.startswith("Phase 1")).sum()),
    )
    g["Avg_Gap"] = g["Avg_Target"] - g["Avg_Current"]
    g = g.reindex(order)
    if by == "Category_ID":
        g.insert(0, "Category", [CATEGORIES[c] for c in g.index])
    return g.round(2).reset_index()


def style_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9)


def radar_chart(func: pd.DataFrame, path: Path):
    labels = func["Function"].tolist()
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    cur = func["Avg_Current"].tolist() + func["Avg_Current"].tolist()[:1]
    tgt = func["Avg_Target"].tolist() + func["Avg_Target"].tolist()[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color=INK_2, fontsize=8)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color=INK, fontsize=11)
    ax.grid(color=GRID, linewidth=1)
    ax.spines["polar"].set_color(GRID)

    ax.plot(angles, tgt, color=TARGET, linewidth=2, linestyle="--", label="Target profile")
    ax.plot(angles, cur, color=CURRENT, linewidth=2, label="Current profile")
    ax.fill(angles, cur, color=CURRENT, alpha=0.15)
    ax.scatter(angles[:-1], cur[:-1], color=CURRENT, s=40, zorder=3,
               edgecolor="white", linewidth=2)

    ax.set_rlabel_position(90 / 2)
    ax.tick_params(axis="x", pad=10)
    fig.suptitle("Current vs. target maturity by CSF 2.0 function (average, 0-5 scale)",
                 color=INK, fontsize=12, y=0.97)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False,
              labelcolor=INK_2, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)


def category_dumbbell(cat: pd.DataFrame, path: Path):
    cat = cat.sort_values("Avg_Gap", ascending=True).reset_index(drop=True)
    labels = [f"{cid}  {name}" for cid, name in zip(cat["Category_ID"], cat["Category"])]
    y = np.arange(len(cat))

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.hlines(y, cat["Avg_Current"], cat["Avg_Target"], color=GRID, linewidth=4, zorder=1)
    ax.scatter(cat["Avg_Target"], y, color=TARGET, s=110, zorder=3,
               edgecolor="white", linewidth=2, label="Target (avg)")
    ax.scatter(cat["Avg_Current"], y, color=CURRENT, s=60, zorder=4,
               edgecolor="white", linewidth=2, label="Current (avg)")
    for yi, g, t in zip(y, cat["Avg_Gap"], cat["Avg_Target"]):
        ax.text(max(t, 0) + 0.12, yi, f"gap {g:.1f}" if g > 0 else "at target", va="center", fontsize=8, color=INK_2)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9, color=INK)
    ax.set_xlim(0, 5)
    ax.set_xticks(range(6))
    ax.set_xticklabels([f"{k}\n{v}" for k, v in MATURITY_LEVELS.items()], fontsize=8)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    style_axes(ax)
    ax.set_title("Maturity gap by CSF 2.0 category (largest gaps at top)",
                 color=INK, fontsize=13, loc="left", pad=30)
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False,
              labelcolor=INK_2, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)


def phase_chart(df: pd.DataFrame, path: Path):
    order = ["Phase 1 (0-90 days)", "Phase 2 (3-6 months)",
             "Phase 3 (6-12 months)", "Maintain"]
    counts = df["Roadmap_Phase"].value_counts().reindex(order, fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 3.6))
    bars = ax.barh(order[::-1], counts[order[::-1]], color=CURRENT, height=0.55)
    for b in bars:
        ax.text(b.get_width() + 0.6, b.get_y() + b.get_height() / 2,
                f"{int(b.get_width())}", va="center", fontsize=10, color=INK)
    style_axes(ax)
    ax.set_xlabel("Number of subcategories", color=INK_2, fontsize=9)
    ax.set_title("Subcategories by remediation phase", color=INK, fontsize=13,
                 loc="left", pad=12)
    ax.set_xlim(0, counts.max() * 1.15)
    fig.tight_layout()
    fig.savefig(path, dpi=160, facecolor="white")
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    df = enrich(load_and_validate())
    func = summarize(df, "Function")
    cat = summarize(df, "Category_ID")

    top = (df[df["Gap"] > 0]
           .sort_values(["Priority_Score", "Gap"], ascending=False)
           .head(15)[["Subcategory_ID", "Category", "Current_Maturity",
                      "Target_Maturity", "Gap", "Business_Priority",
                      "Priority_Score", "Recommendation", "Owner"]])

    df.to_csv(OUT / "scored_assessment.csv", index=False)
    func.to_csv(OUT / "function_summary.csv", index=False)
    cat.to_csv(OUT / "category_summary.csv", index=False)
    top.to_csv(OUT / "top_15_gaps.csv", index=False)

    radar_chart(func, OUT / "function_radar.png")
    category_dumbbell(cat, OUT / "category_gaps.png")
    phase_chart(df, OUT / "roadmap_phases.png")

    overall_cur = df["Current_Maturity"].mean()
    overall_tgt = df["Target_Maturity"].mean()
    print(f"Subcategories assessed: {len(df)}")
    print(f"Overall current maturity: {overall_cur:.2f}")
    print(f"Overall target maturity:  {overall_tgt:.2f}")
    print(f"Subcategories with a gap: {(df['Gap'] > 0).sum()}")
    print(f"Subcategories at 0 (not performed): {(df['Current_Maturity'] == 0).sum()}")
    print("\nPhase counts:")
    print(df["Roadmap_Phase"].value_counts().to_string())
    print("\nFunction summary:")
    print(func.to_string(index=False))
    print("\nCategory summary:")
    print(cat.to_string(index=False))
    print("\nTop 15 gaps:")
    print(top[["Subcategory_ID", "Gap", "Business_Priority", "Priority_Score", "Owner"]]
          .to_string(index=False))
    print(f"\nOutputs written to {OUT}")


if __name__ == "__main__":
    main()
