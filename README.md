# Men's T20I Cricket Analytics

Team and match performance analysis built from **ball-by-ball** records of Men's T20 Internationals, spanning **2005–2026**.

## At a glance

| Metric | Value |
| --- | --- |
| Matches analysed | 658 |
| Teams | 106 |
| Runs scored | 181,347 |
| Wickets taken | 8,561 |
| Sixes | 6,460 |
| Fours | 14,062 |
| Average first-innings score | 148.1 |
| Win rate batting first | 51.2% |

## What the dashboard shows

- **How scoring has changed** — average first-innings score and runs per over, by year
- **Team profile** — pick any team with 25+ matches and see win %, average score, average conceded, and phase-by-phase batting vs bowling economy
- **Phase analysis** — powerplay (overs 1–6), middle (7–15), and death (16–20)
- **Sortable team table** — matches, wins, win %, average score, average conceded, win % batting first, and win % chasing
- **Leading wicket-takers and venue breakdowns**

## Repository contents

| Path | Contents |
| --- | --- |
| `index.html` | The dashboard, fully self-contained (all data embedded) — this is what is deployed |
| `Project_Files/` | The original dashboard HTML plus the Python dataset scripts |
| `Dataset_Files/mens_t20_processed.csv` | Cleaned ball-by-ball dataset behind the analysis (25.5 MB) |
| `Report_Presentation_and_Dashboard_Screenshots/` | Written report, presentation, and dashboard screenshots (PDF/PPTX) |

### Note on the raw dataset

The original raw export `ball_by_ball_t20_men.csv` is **130.8 MB**, which exceeds GitHub's 100 MB per-file limit, so it is **excluded from this repository** (see `.gitignore`). The processed dataset in `Dataset_Files/` is the subset used to build the dashboard.

## Dataset scripts

| Script | Purpose |
| --- | --- |
| `inspect_dataset.py` | Prints column names, sample rows, and the total row count of a CSV |
| `audit_dataset.py` | Data-quality audit: exact duplicates, missing values by column, distinct teams and venues, season/gender/match-type coverage |
| `prepare_dataset.py` | Builds the processed dataset by selecting complete matches spread chronologically from the raw export |
| `validate_dataset.py` | Validates the processed CSV: row counts, unique matches, required columns, date coverage |

`inspect_dataset.py`, `audit_dataset.py`, and `prepare_dataset.py` prompt for file paths when run. `validate_dataset.py` has a hard-coded Windows path near the top of the file — update it to your own location before running.

## View it locally

No installation, no build step, no server:

> Open `index.html` in any modern browser.

The charts, filters, and tables all run client-side from the embedded dataset.

To rebuild the processed dataset from your own raw export:

```bash
python Project_Files/prepare_dataset.py
```

## Interpreting the results

Winners in this dataset are decided by **innings totals**, so rain-affected results may differ from the official record. All figures describe the supplied dataset only.
