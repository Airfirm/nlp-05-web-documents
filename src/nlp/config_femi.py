"""
src/nlp/config_femi.py - Module 5 Configuration

Stores configuration values for the web document EVTL pipeline.
Source: arXiv abstract page for "Agents of Chaos" (2602.20021)

Purpose

  Store configuration values.

Analytical Questions

- What web page URL should be used as the data source?
- Where should raw and processed data be stored?

"""

from pathlib import Path

# ============================================================
# API CONFIGURATION
# ============================================================

PAGE_URL: str = "https://arxiv.org/abs/2604.01967"
# arXiv abstract page — stable, scraping-friendly, academically relevant

# Let them know who we are (and that we're doing educational web mining).
HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (educational-use; web-mining-course)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

RAW_HTML_PATH: Path = RAW_PATH / "femi_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "femi_processed.csv"
