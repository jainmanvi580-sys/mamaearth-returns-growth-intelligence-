import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FINDINGS_FILE = BASE_DIR / "narrator" / "findings.json"
OUTPUT_FILE = BASE_DIR / "narrator" / "narrative.json"


def load_findings():
    with open(FINDINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def offline_narrative(findings):
    # Read verified numbers from findings.json
    total_revenue = findings["cleaned_total_revenue_inr"]
    duplicate_delta = findings["duplicate_reconciliation_delta_inr"]

    cod_return_rate = findings["return_rate_by_payment"]["COD"]

    risk_segment = findings["highest_risk_segment"]
    risk_rate = risk_segment["return_rate_pct"]
    risk_payment = risk_segment["payment_method"]
    risk_tier = risk_segment["city_tier"]

    peak = findings["true_peak_month"]
    peak_month = peak["month"]
    peak_revenue = peak["revenue_inr"]

    month_name = {
        "2026-01": "January",
        "2026-02": "February",
        "2026-03": "March",
        "2026-04": "April",
        "2026-05": "May",
        "2026-06": "June",
        "2026-07": "July",
        "2026-08": "August",
        "2026-09": "September",
        "2026-10": "October",
        "2026-11": "November",
        "2026-12": "December",
    }.get(peak_month, peak_month)

    situation = (
        f"The cleaned total revenue was INR {total_revenue:,.2f}. "
        f"The true peak month was {month_name} {peak_month[:4]}, "
        f"with revenue of INR {peak_revenue:,.2f}."
    )

    complication = (
        f"The COD return rate was {cod_return_rate:.1f}%. "
        f"The highest-risk segment was {risk_payment} customers "
        f"in Tier-{risk_tier} cities, with a return rate of "
        f"{risk_rate:.1f}%. Duplicate-driven reconciliation "
        f"delta was INR {duplicate_delta:,.2f}."
    )

    resolution = (
        "The business should investigate COD returns, review "
        "duplicate records, and use cleaned revenue figures "
        "to make future business decisions."
    )

    return {
        "mode": "offline",
        "situation": situation,
        "complication": complication,
        "resolution": resolution,
        "metrics": {
            "cleaned_total_revenue_inr": total_revenue,
            "cod_return_rate_pct": cod_return_rate,
            "highest_risk_segment_return_rate_pct": risk_rate,
            "duplicate_reconciliation_delta_inr": duplicate_delta,
            "true_peak_month": month_name,
            "true_peak_month_revenue_inr": peak_revenue,
        },
    }


def main():
    findings = load_findings()
    result = offline_narrative(findings)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    print("Offline fallback completed successfully.")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()

