# Mamaearth Returns & Growth Intelligence Pipeline

## 1. Project Overview

This project analyzes Mamaearth's customer, product, and order data using SQL and Python. It cleans the data, analyzes revenue and return trends, creates visualizations, and generates a business narrative using the Gemini API or an offline fallback.

## 2. Step 1 — Load SQL Data and Run Reports

Open MySQL Workbench and connect to your MySQL server.

Execute the SQL files in this order:

1. `sql/schema.sql` — creates the database tables and their constraints.
2. `sql/seed_data.sql` — loads the supplied customer, product, and order data.
3. `sql/reports.sql` — runs the required SQL reporting queries.

Run each file in MySQL Workbench and verify the query results before proceeding.

## 3. Step 2 — Data Cleaning and Visualization

Run these Python scripts from the project root directory:

```bash
python analysis/clean_and_eda.py
python analysis/visualize.py
```

The `clean_and_eda.py` script cleans the data and performs exploratory data analysis. The `visualize.py` script creates the required charts.

Task 5 of Part 2 writes the verified analysis results to:

`narrator/findings.json`

Confirm that this file exists and contains the expected metrics before generating the narrative.

The expected visualization files are:

* `visualizations/return_rate_by_payment.png`
* `visualizations/monthly_revenue_trend.png`

## 4. Step 3 — Generate the Business Narrative

Run the narrative generator from the project root directory:

```bash
python narrator/generate_narrative.py
```

### Online mode — Gemini API

Set the `GEMINI_API_KEY` environment variable in Windows PowerShell before running the generator:

```powershell
$env:GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"
python narrator/generate_narrative.py
```

Replace `YOUR_ACTUAL_API_KEY` with your own Gemini API key. Never commit the API key to GitHub.

The online path uses Gemini when the API key is configured and the generator's online implementation successfully makes the request.

### Offline mode — No API key

To run without a Gemini API key in the current PowerShell session:

```powershell
Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
python narrator/generate_narrative.py
```

The offline fallback should generate a narrative without making a Gemini API request or requiring an API key.

The generated narrative is saved to:

`narrator/narrative.json`

## 5. Numeric Accuracy Validation — Part 3, Task 5

Save the narrative text being tested to:

`narrator/sample_output.txt`

Run the numeric accuracy checker from the project root:

```bash
python narrator/check_narrative.py
```

The checker verifies that the saved narrative contains all five required figures:

1. Cleaned total revenue: `97,358.30`
2. COD return rate: `44.4`
3. COD + Tier-2 highest-risk segment return rate: `54.5`
4. Duplicate-driven reconciliation delta: `2,501.90`
5. True peak month: `March`, with revenue of `20,318.90`

For an online test, save the actual Gemini-generated narrative in `narrator/sample_output.txt` before running the checker. The saved sample is used for grading.

## 6. Complete Pipeline Execution Order

To reproduce the project results, follow this order:

1. Load `sql/schema.sql`.
2. Load `sql/seed_data.sql`.
3. Run `sql/reports.sql`.
4. Run `analysis/clean_and_eda.py`.
5. Run `analysis/visualize.py`.
6. Verify the metrics in `narrator/findings.json`.
7. Run `narrator/generate_narrative.py` in online or offline mode.
8. Save the narrative sample and run `narrator/check_narrative.py`.

Use the verified data and saved outputs to reproduce the reported revenue, return rates, reconciliation delta, and peak-month results.
