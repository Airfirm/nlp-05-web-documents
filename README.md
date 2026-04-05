# nlp-05-web-documents

[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Structured EVTL pipeline for reliable extraction and transformation of data from HTML web pages.


# arXiv HTML EVTL Pipeline Project

## Overview

This project builds an **EVTL pipeline** to extract, validate, transform, and load data from an arXiv paper webpage.

EVTL stands for:

- **Extract** – fetch the raw HTML from the source URL
- **Validate** – inspect and validate the HTML structure
- **Transform** – extract and clean fields from the page and create derived analytical features
- **Load** – save the processed output to a final file such as CSV

The goal of this project is to turn a semi-structured HTML page into a structured, analysis-ready dataset.

---

## Source URL

The source data for this project comes from the following arXiv page:

`https://arxiv.org/abs/2604.01967`

This page contains metadata for the paper:

**Optimizing Relational Queries over Array-Valued Data in Columnar Systems**

The raw HTML includes fields such as:

- title
- authors
- abstract
- subject/category
- submission date
- canonical arXiv ID
- PDF link

---

## Project Goal

The purpose of this project is to practice working with HTML as a data source in an NLP-style pipeline. Unlike JSON APIs, HTML must be parsed and inspected carefully because the content is embedded inside tags, classes, and attributes.

This project demonstrates how to:

- fetch raw HTML from a webpage
- validate expected HTML elements
- extract bibliographic and descriptive metadata
- clean fields that contain descriptor prefixes
- create derived analytical columns
- produce a structured DataFrame for downstream analysis

---

## Pipeline Structure

This project is organized into pipeline stages:

- `config_femi.py` – stores paths, source URL, and request headers
- `stage01_extract_femi.py` – fetches the raw HTML from the webpage
- `stage02_validate_femi.py` – validates that the required HTML structure exists
- `stage03_transform_femi.py` – extracts, cleans, and transforms fields into a DataFrame
- `stage04_load_femi.py` – saves the final output
- `pipeline_femi_html.py` – orchestrates the full EVTL pipeline

---

## How to Run

Run the full pipeline from the project root:

```bash
uv run python -m nlp.pipeline_femi_html



This executes the stages in order:

Extract
Validate
Transform
Load
Data Source Type

This project uses HTML as the source data type.

That means the workflow differs from an API JSON pipeline because:

HTML must be parsed using BeautifulSoup
fields must be located using HTML tags, classes, and attributes
data often requires additional cleaning after extraction
webpage structure can change, making validation especially important
Tools Used
Python
requests
BeautifulSoup
pandas
logging
EVTL pipeline design
Fields Extracted

The Transform stage extracts the following core fields from the arXiv page:

arxiv_id
title
authors
subjects
submitted
abstract

Additional extracted metadata includes:

pdf_url
primary_subject
primary_category_code
Derived Analytical Fields

The Transform stage also creates derived fields to make the output more useful for analysis:

author_count – number of authors listed on the paper
first_author – first author extracted from the author list
abstract_word_count – total number of words in the abstract
abstract_sentence_count – estimated number of sentences in the abstract
title_char_count – number of characters in the title

These fields help support exploratory analysis and make the dataset more informative than a basic scrape.

Cleaning and Special Handling

Several fields required extra cleaning after extraction:

Title

The title is stored in an <h1> tag that includes the visible prefix Title: inside the same tag as the actual paper title.
This prefix had to be removed.

Abstract

The abstract is stored in a <blockquote> tag that includes the prefix Abstract:.
This descriptor had to be removed to produce clean text.

Submitted Date

The submission date appears in a format like:

[Submitted on 2 Apr 2026]

This required cleaning to remove brackets and the phrase Submitted on.

Authors

The authors container includes author links and punctuation.
To avoid formatting issues, the author names were extracted from the individual <a> tags and then joined into a clean comma-separated string.

What Was Modified

The Transform stage was customized beyond the base example to:

add a new derived column for sentence count in the abstract
add extraction of the PDF URL
add extraction of the primary arXiv category code
add extraction of the first author
improve logging detail for each pipeline step
clean descriptor-prefixed fields more carefully

These updates made the pipeline more analytical, more readable, and easier to debug.

Why These Modifications Were Made

These modifications were made to create a richer structured output from the HTML page and to make the transformed data more useful for analysis.

Instead of only capturing the basic bibliographic fields, the updated pipeline now produces a more complete paper record that can support:

metadata analysis
text-based feature generation
category grouping
paper summary comparisons
future NLP workflows
Example Analytical Questions Supported

This transformed dataset can help answer questions such as:

What is the primary arXiv category for this paper?
How many authors contributed to the paper?
Who is the first author?
How long is the abstract in words or sentences?
What PDF link is associated with the paper?
How much cleaning is needed when scraping HTML metadata fields?
Results Summary

The final output is a clean one-row pandas DataFrame containing:

bibliographic metadata
cleaned abstract and title text
subject/category information
a direct PDF link
derived analytical features

This makes the webpage content analysis-ready and suitable for saving as a CSV or using in later NLP workflows.

Challenges Encountered

A few challenges came up during development:

some extracted fields included descriptor text like Title: and Abstract:
the submission date included extra formatting that needed cleaning
author extraction required handling multiple <a> tags instead of using the full container text
extraction logic had to be based on the actual HTML structure, not assumptions

These challenges reinforced the importance of inspecting the page source before writing extraction code.

How the Challenges Were Addressed

The challenges were addressed by:

carefully reviewing the HTML source
locating the correct tags and classes
using targeted cleaning with string replacement and strip()
extracting author names from <a> tags directly
adding more detailed logging messages to verify each step
Why Pandas Was Used

This project uses pandas instead of Polars because the transformed output is a small, structured record from a single webpage. Pandas was a good fit because it is simple, readable, and convenient for building a one-row DataFrame from extracted fields.

What Is Interesting About This Project

What is interesting about this project is that it turns a single HTML paper page into a structured analytical record. It shows that even though HTML is designed for display in a browser, it can still be transformed into a clean dataset with the right parsing and cleaning logic.

It also demonstrates that transformation is not just about copying values — it is also about improving the usefulness of the data by creating analytical features.

Lessons Learned

This project reinforced several important ideas:

HTML must be inspected before extraction logic is written
validation is important because webpage structure can change
scraped fields often need cleaning before they are usable
small derived columns can add major analytical value
EVTL is a strong design pattern for reproducible data workflows
Suggestions for Future Improvements

Possible next steps for this project include:

scraping multiple arXiv paper pages instead of one
extracting DOI and submission history details
adding text preprocessing for the abstract
performing word frequency analysis on multiple abstracts
grouping papers by category code
exporting multiple paper records into one larger dataset



Web Mining and Applied NLP require reliable acquisition and
processing of structured and semi-structured text data.
This project implements a reproducible pipeline for
working with HTML data from web pages.

The pipeline follows an EVTL architecture:

- Extract HTML from a web page
- Validate structure and content before use
- Transform HTML into a structured representation
- Load results into a persistent, analyzable format

The emphasis is on correctness, inspectability, and repeatability:
every stage has explicit inputs, outputs, and logging,
and intermediate artifacts are preserved for verification.

## This Project

This project demonstrates how to work with
HTML data retrieved from web pages using a structured EVTL pipeline.

The workflow:

- Acquire HTML from an external web page
- Inspect and validate its structure
- Transform it into a tabular representation
- Persist results for downstream analysis

Each stage is implemented as a modular component with explicit inputs and outputs.

## Key Files

These files define the EVTL pipeline and the components you will update for your project.

- **src/nlp/pipeline_web_html.py** - Main pipeline orchestrator (no changes required)
- **src/nlp/config_case.py** - Configuration for page URL and paths (<mark>**copy and edit**</mark> for your project)
- **src/nlp/stage01_extract.py** - Extract stage: fetches HTML from a web page (no changes required)
- **src/nlp/stage02_validate_case.py** - Validate stage: inspects and verifies HTML structure (<mark>**copy and edit**</mark>)
- **src/nlp/stage03_transform_case.py** - Transform stage: converts HTML into structured data (<mark>**copy and edit**</mark>)
- **src/nlp/stage04_load.py** - Load stage: writes output to persistent storage (no changes required)
- **pyproject.toml** - Project metadata and dependencies (<mark>**update**</mark> authorship, links, and dependencies)
- **zensical.toml** - Documentation configuration (<mark>**update**</mark> authorship and links)

## First: Follow These Instructions

Follow the [step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/) to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**

## Challenges

Challenges are expected.
Sometimes instructions may not quite match your operating system.
When issues occur, share screenshots, error messages, and details about what you tried.
Working through issues is an important part of implementing professional projects.

## Success

After completing Phase 1. **Start & Run**, you'll have your own GitHub project,
running on your machine, and running the example will print out:

```shell
========================
Pipeline executed successfully!
========================
```

The following artifacts will be created:

- project.log - confirming successful run
- data/raw/case_raw.json - dump of the fetched JSON
- data/processed/case_processed.csv - final loaded result

## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/Airfirm/nlp-05-web-documents
cd nlp-05-web-documents
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files

# Later, we install spacy data model and
# en_core_web_sm = english, core, web, small
# It's big: spacy+data ~200+ MB w/ model installed
#           ~350–450 MB for .venv is normal for NLP
# uv run python -m spacy download en_core_web_sm

# First, run the module
# IMPORTANT: Close each figure after viewing so execution continues
uv run python -m nlp.pipeline_web_html

uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Example Artifact (Output)

```text
START PIPELINE
ROOT_PATH = .
DATA_PATH = data
RAW_PATH = data\raw
PROCESSED_PATH = data\processed
========================
STAGE 01: EXTRACT starting...
========================
SOURCE URL = https://arxiv.org/abs/2602.20021
SINK PATH = data\raw\case_raw.html
========================
STAGE 02: VALIDATE starting...
========================
HTML STRUCTURE INSPECTION:
Top-level type: BeautifulSoup
Top-level elements: ['html']
VALIDATE: Title found: True
VALIDATE: Authors found: True
VALIDATE: Abstract found: True
VALIDATE: Subjects found: True
VALIDATE: Dateline found: True
VALIDATE: HTML structure is valid.
Sink: validated BeautifulSoup object
========================
STAGE 03: TRANSFORM starting...
========================
Transformation complete.
DataFrame preview:
   arxiv_id            title  ... abstract_word_count  author_count
0  2602.20021  Agents of Chaos  ...                177            38
Sink: Pandas DataFrame created
========================
STAGE 04: LOAD starting...
========================
SINK PATH = data\processed\case_processed.csv
========================
Pipeline executed successfully!
========================
```

## Enhancements

In production systems, validation is often automated using tools
such as **Great Expectations** or **Soda**.

Within the EVTL architecture, **VALIDATE** is a key stage
with a clear source, process, and sink:

- **Source**: HTML fetched from the web page
- **Process**: parsing with BeautifulSoup, checking structure, confirming expected elements are present
- **Sink**: BeautifulSoup object passed to the TRANSFORM stage

This stage ensures the data is in a **consistent and reliable form**
before transformation begins,
so later steps can run without errors or unexpected results.

In this project, validation is implemented directly,
so all checks are visible, repeatable, and easy to review as part
of the pipeline.
