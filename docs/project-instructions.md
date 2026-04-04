# Project Instructions (Module 5: Web Documents and HTML Data)

## WEDNESDAY: Complete Workflow Phase 1

Follow the instructions in
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to complete:

1. Phase 1. **Start & Run** - copy the project and confirm it runs

## FRIDAY/SUNDAY: Complete Workflow Phases 2-4

Again, follow the instructions above to complete:

1. Phase 2. **Change Authorship** - update the project to your name and GitHub account
2. Phase 3. **Read & Understand** - review the project structure and code
3. Phase 4. **Make a Technical Modification** - make a change and verify it still runs.

## Phase 4 Suggestions

Make a small technical change that does not break the pipeline.
Choose any one of these (or a different modification as you like):

- Change the target URL to a different arXiv paper
  (find a paper you find interesting at https://arxiv.org)
- Add a new derived column in the Transform stage
  (e.g., sentence count in the abstract, or first author only)
- Add extraction of a new field from the page
  (e.g., the PDF link, or the arXiv category code)
- Adjust logging messages to provide more detail about the pipeline stages

Confirm the script still runs successfully after your change.

## Phase 5 Suggestions

### Phase 5 Suggestion 1. New arXiv Paper (Directed)

Apply the same EVTL pipeline to a different arXiv abstract page.

Steps:

- Find an arXiv paper that interests you at https://arxiv.org
- Copy the abstract page URL (e.g., `https://arxiv.org/abs/XXXX.XXXXX`)
- Update `PAGE_URL` in your copied `config` file with the new URL
- Run the pipeline
- Inspect the extracted fields in the log output
- Confirm the pipeline runs successfully

Then:

- Identify the title, authors, and primary subject of your chosen paper
- Describe one field that required cleaning or special handling
- Explain how the abstract word count compares to the case example

### Phase 5 Suggestion 2. New Web Page (Original Selection)

Apply this pipeline to a different web page of your choice.

Good options include:

- Another arXiv listing page (e.g., `https://arxiv.org/list/cs.AI/recent`)
  to extract multiple papers at once
- A Wikipedia article to extract the introduction and metadata
- A Project Gutenberg page to extract text from a literary work
  (e.g., https://www.gutenberg.org/files/1342/1342-h/1342-h.htm Pride and Prejudice)

Steps:

- Open the target page in your browser
- Right-click and select "View Page Source" to inspect the HTML structure
- Identify the tags and class names that wrap the content you want
- Update your copied `config` file with the new URL
- Update your copied `stage02_validate` file to check for the new structure
- Update your copied `stage03_transform` file to extract the new fields
- Run the pipeline and confirm success

Then:

- Describe the HTML structure of your chosen page
- Identify the tags and attributes you used to extract each field
- Explain one challenge you encountered and how you resolved it

## Key Skill Focus

As you work, focus on:

- how to fetch HTML from a web page
- how to inspect unknown HTML structures using View Page Source
- how to identify tags, classes, and attributes that wrap desired content
- how to extract clean text using BeautifulSoup
- how to handle missing elements gracefully with fallback values
- how data moves through the EVTL pipeline

Your goal is to reuse the same pipeline pattern on new web data sources.

## Optional Enhancements

If time allows, consider:

- extracting additional fields (PDF link, DOI, version history)
- computing additional derived fields (sentence count, average word length)
- scraping a listing page to extract multiple records into a multi-row DataFrame
- comparing two papers side by side in a single DataFrame

## Professional Communication

Remove instructor-provided content you no longer need in your project.

Make sure the title and narrative reflect your presentation.
Verify key files:

- README.md
- docs/ (source and hosted on GitHub Pages)
- src/ (pipeline and stage files)

Ensure your project clearly demonstrates:

- correct EVTL pipeline execution
- understanding of HTML structure and BeautifulSoup
- ability to adapt the pipeline to new web data sources
