"""
src/nlp/stage03_transform_femi.py

Source: validated BeautifulSoup object
Sink: Pandas DataFrame

NOTE: We use Pandas here to contrast with Polars (from Module 4).
You may use Polars or another library if you prefer:
the pipeline pattern is identical; only the DataFrame API differs.

Pandas vs. Polars:
- Pandas is widely used and has a larger ecosystem.
- Polars is faster, more memory efficient, handles larger datasets,
  and is better suited for production pipelines and complex
  transformations.

Purpose

  Transform validated BeautifulSoup object into a structured format.

Analytical Questions

- Which fields are needed from the HTML data?
- How can records be normalized into tabular form?
- What derived fields would support analysis?

How to find the fields you want to extract from the web page:

  1. Open the web page in your browser.
  2. Right-click anywhere on the page and select "View Page Source".
  3. Use Ctrl+F to search for text you can see on the page,
     e.g. the paper title or "Abstract:".
  4. Find the HTML tag and class that wraps it, e.g.:
       <h1 class="title mathjax"><span class="descriptor">Title:</span>
  5. Use soup.find("h1", class_="title") to locate the associated tag.
  6. Use .get_text(strip=True) to extract the visible text from inside the tag.
  7. If the tag contains a descriptor prefix like "Title:" or "Authors:",
     use .replace("Title:", "").strip() to remove it.
  8. If the tag is not found, soup.find() returns None which is not a string.
     To avoid errors, use a conditional expression to return "unknown" as a safe fallback:
       value = tag.get_text(strip=True) if tag else "unknown"

Apply this process for each field you want to extract for analysis.
The same approach works for any web page.

Example: For the arXiv page at https://arxiv.org/abs/2604.01967,
we can extract the following fields using BeautifulSoup:

- title from <h1 class="title"> (string)
- authors from <div class="authors"> (string)
- abstract from <blockquote class="abstract"> (string)
- primary subject from <div class="subheader"> (string)
- submission date from <div class="dateline"> (string)
- arXiv ID from canonical link in the <head> section (string)

we can calculate derived fields like:
- abstract word count (integer)
- author count (integer)

IMPORTANT: Getting information from a web page is not as simple as it looks.
Web pages are designed for human consumption, not for data extraction.
The HTML structure can be complex and inconsistent, and may require careful inspection and handling to extract the desired information.
The title and abstract are wrapped in tags with descriptor text ("Title:", "Abstract:") that must be removed to get clean values.
The authors are listed as multiple <a> tags inside a <div>, so we must extract each author separately and join them with commas to avoid double-comma issues.
The arXiv ID is not directly visible on the page but can be extracted from the canonical link in the HTML head.
This stage requires careful inspection of the HTML structure and thoughtful handling of edge cases to ensure we extract clean, structured data for analysis.

Use all your resources, creativity, and problem-solving skills to navigate the complexities of web data extraction and transformation.


"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
import re

from bs4 import BeautifulSoup, Tag
import pandas as pd

# ============================================================
# Section 2. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform HTML into a structured DataFrame.

    Args:
        soup (BeautifulSoup): Validated BeautifulSoup object.
        LOG (logging.Logger): The logger instance.

    Returns:
        pd.DataFrame: The transformed dataset.
    """
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    LOG.info(
        "Source sink: validated BeautifulSoup object -> analysis-ready Pandas DataFrame"
    )
    LOG.info("Beginning field extraction from inspected arXiv HTML structure")

    # ========================================================
    # STAGE 03a: Locate key HTML elements
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03a: Locate HTML elements")
    LOG.info("========================")

    title_tag: Tag | None = soup.find("h1", class_="title")

    authors_tag: Tag | None = soup.find("div", class_="authors")

    abstract_tag: Tag | None = soup.find("blockquote", class_="abstract")
    subheader_tag: Tag | None = soup.find("div", class_="subheader")
    dateline_tag: Tag | None = soup.find("div", class_="dateline")
    canonical_tag: Tag | None = soup.find("link", rel="canonical")
    pdf_tag: Tag | None = soup.find("a", class_="abs-button download-pdf")
    primary_subject_tag: Tag | None = soup.find("span", class_="primary-subject")

    LOG.info(f"title_tag found: {title_tag is not None}")
    LOG.info(f"authors_tag found: {authors_tag is not None}")
    LOG.info(f"abstract_tag found: {abstract_tag is not None}")
    LOG.info(f"subheader_tag found: {subheader_tag is not None}")
    LOG.info(f"dateline_tag found: {dateline_tag is not None}")
    LOG.info(f"canonical_tag found: {canonical_tag is not None}")
    LOG.info(f"pdf_tag found: {pdf_tag is not None}")
    LOG.info(f"primary_subject_tag found: {primary_subject_tag is not None}")

    # ========================================================
    # STAGE 03b: Extract and clean bibliographic fields
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03b: Extract and clean bibliographic fields")
    LOG.info("========================")

    # Title cleaning:
    # arXiv stores the visible descriptor "Title:" inside the same <h1> tag
    # as the actual title, so we must remove that prefix after extraction.
    raw_title: str = title_tag.get_text(" ", strip=True) if title_tag else "unknown"
    title: str = (
        raw_title.replace("Title:", "", 1).strip()
        if raw_title != "unknown"
        else "unknown"
    )

    # Authors extraction:
    # Use only <a> tags to avoid punctuation/text node issues in the container.
    author_tags_list: list[Tag] = authors_tag.find_all("a") if authors_tag else []
    author_names_list: list[str] = [
        tag.get_text(strip=True) for tag in author_tags_list
    ]
    authors: str = ", ".join(author_names_list) if author_names_list else "unknown"

    # New derived field: first author only
    first_author: str = author_names_list[0] if author_names_list else "unknown"

    # Abstract cleaning:
    # arXiv includes "Abstract:" inside the blockquote, so remove it.
    raw_abstract: str = (
        abstract_tag.get_text(" ", strip=True) if abstract_tag else "unknown"
    )
    abstract: str = (
        raw_abstract.replace("Abstract:", "", 1).strip()
        if raw_abstract != "unknown"
        else "unknown"
    )

    LOG.info(f"Extracted cleaned title: {title}")
    LOG.info(f"Extracted authors count from tags: {len(author_names_list)}")
    LOG.info(f"Extracted first author: {first_author}")
    LOG.info(f"Extracted abstract preview: {abstract[:120]}...")

    # ========================================================
    # STAGE 03c: Extract subject and category metadata
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03c: Extract subject and category metadata")
    LOG.info("========================")

    subjects: str = (
        subheader_tag.get_text(" ", strip=True) if subheader_tag else "unknown"
    )
    primary_subject: str = (
        primary_subject_tag.get_text(" ", strip=True)
        if primary_subject_tag
        else "unknown"
    )

    # Example primary subject text:
    # "Databases (cs.DB)"
    # Extract the category code inside parentheses if available.
    category_match = re.search(r"\(([^)]+)\)", primary_subject)
    primary_category_code: str = (
        category_match.group(1) if category_match else "unknown"
    )

    LOG.info(f"Extracted subjects heading: {subjects}")
    LOG.info(f"Extracted primary subject: {primary_subject}")
    LOG.info(f"Extracted primary category code: {primary_category_code}")

    # ========================================================
    # STAGE 03d: Extract date, canonical arXiv id, and PDF link
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03d: Extract date, arXiv ID, and PDF link")
    LOG.info("========================")

    raw_submitted: str = (
        dateline_tag.get_text(" ", strip=True) if dateline_tag else "unknown"
    )

    # Dateline cleaning:
    # The visible text includes square brackets, e.g. "[Submitted on 2 Apr 2026]".
    # Remove brackets and the fixed phrase for a cleaner field.
    submitted: str = raw_submitted
    if submitted != "unknown":
        submitted = submitted.replace("[", "").replace("]", "")
        submitted = submitted.replace("Submitted on", "", 1).strip()

    if canonical_tag is None:
        LOG.warning("Canonical link not found; setting arxiv_id to 'unknown'")
        arxiv_id = "unknown"
    else:
        href = str(canonical_tag.get("href", ""))
        arxiv_id = href.split("/abs/")[-1] if "/abs/" in href else "unknown"

    # New extracted field: PDF link
    if pdf_tag is None:
        LOG.warning("PDF link not found; setting pdf_url to 'unknown'")
        pdf_url = "unknown"
    else:
        pdf_href = str(pdf_tag.get("href", "")).strip()
        pdf_url = (
            f"https://arxiv.org{pdf_href}"
            if pdf_href.startswith("/")
            else pdf_href
            if pdf_href
            else "unknown"
        )

    LOG.info(f"Extracted submitted date: {submitted}")
    LOG.info(f"Extracted arXiv ID: {arxiv_id}")
    LOG.info(f"Extracted PDF URL: {pdf_url}")

    # ========================================================
    # STAGE 03e: Calculate derived analytical fields
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03e: Calculate derived analytical fields")
    LOG.info("========================")

    abstract_word_count: int = len(abstract.split()) if abstract != "unknown" else 0
    abstract_sentence_count: int = (
        len([s for s in re.split(r"[.!?]+", abstract) if s.strip()])
        if abstract != "unknown"
        else 0
    )
    author_count: int = len(author_names_list)
    title_char_count: int = len(title) if title != "unknown" else 0

    LOG.info(f"Calculated author_count: {author_count}")
    LOG.info(f"Calculated abstract_word_count: {abstract_word_count}")
    LOG.info(f"Calculated abstract_sentence_count: {abstract_sentence_count}")
    LOG.info(f"Calculated title_char_count: {title_char_count}")

    # ========================================================
    # STAGE 03f: Build final record and DataFrame
    # ========================================================
    LOG.info("========================")
    LOG.info("STAGE 03f: Build record and DataFrame")
    LOG.info("========================")

    record = {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "first_author": first_author,
        "author_count": author_count,
        "subjects": subjects,
        "primary_subject": primary_subject,
        "primary_category_code": primary_category_code,
        "submitted": submitted,
        "abstract": abstract,
        "abstract_word_count": abstract_word_count,
        "abstract_sentence_count": abstract_sentence_count,
        "title_char_count": title_char_count,
        "pdf_url": pdf_url,
    }

    df = pd.DataFrame([record])

    LOG.info(f"Created DataFrame with {len(df)} row and {len(df.columns)} columns")
    LOG.info(f"Output columns: {list(df.columns)}")
    LOG.info("Preview of transformed record:")
    LOG.info(f"\n{df.head().to_string(index=False)}")

    LOG.info("Sink: Pandas DataFrame created")
    LOG.info("Transformation complete.")

    return df
