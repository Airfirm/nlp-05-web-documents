# Glossary (Module 5: Web Documents and HTML Data)

## Web Page

A document written in HTML that is served by a web server
and rendered by a browser.
In this project, a web page is used as the data source
instead of a structured API.

## HTML (HyperText Markup Language)

The standard language used to structure content on the web.
HTML uses tags to define elements such as headings, paragraphs, links, and divs.
To learn more about HTML, see [HTML: HyperText Markup Language](https://developer.mozilla.org/en-US/docs/Web/HTML).

### HTML Tag

A label that defines the type and structure of an HTML element.
Tags are written with angle brackets, e.g. `<h1>`, `<div>`, `<a>`.
Most tags have an opening tag and a closing tag:
`<h1>Title text</h1>`.

### HTML Attribute

Additional information attached to an HTML tag.
Attributes appear inside the opening tag as key-value pairs,
for example `<div class="authors">`.
Here `class` is the attribute and `"authors"` is its value.

## CSS Class

A label applied to an HTML element using the `class` attribute
to group similar tags into a shared class so they can be styled together.
CSS classes are used to style elements, but also serve as
reliable identifiers when scraping, e.g. `soup.find("div", class_="authors")`.
To learn more about CSS, see [CSS: Cascading Style Sheets](https://developer.mozilla.org/en-US/docs/Web/CSS).

## DOM (Document Object Model)

The tree-like structure representing an HTML document.
The DOM organizes elements as nested nodes:
the `<html>` element contains `<head>` and `<body>`,
which contain further nested elements.
BeautifulSoup parses HTML into a traversable DOM structure.
When working with web pages for content, DOM is a common way to refer to the page.
To learn more about the DOM, see [Document Object Model (DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model).

## Web Scraping

The process of extracting data from web pages by parsing their HTML structure.
Web scraping requires inspecting the page source to identify
the tags and attributes that wrap the desired data.

## Page Source

The raw HTML content of a web page.
In a browser, right-click and select "View Page Source" (Ctrl+U / Cmd+U)
to inspect the HTML structure and find the tags you want to extract.

## requests

A Python library used to make HTTP requests and retrieve web page content.
`requests.get(url)` fetches the HTML of a page and returns a response object.

## HTTP Response

The reply from a web server to an HTTP request.
A response includes a status code and a body.
Status code `200` means success; `404` means not found; `403` means forbidden.

## BeautifulSoup

A Python library for parsing HTML and XML documents.
BeautifulSoup creates a traversable object from raw HTML
that supports searching for tags, attributes, and text content.

## soup.find()

A BeautifulSoup method that searches the parsed HTML for the first
element matching a given tag name and optional attributes.
Returns a `Tag` object if found, or `None` if not found.

Example: `soup.find("h1", class_="title")`

## soup.find_all()

A BeautifulSoup method that returns a list of all elements
matching a given tag name and optional attributes.
Returns an empty list if no matches are found.

Example: `soup.find_all("a")` returns all link tags on the page.

## Tag

A BeautifulSoup object representing a single HTML element.
`Tag` objects support methods like `.get_text()` and `.find_all()`.
`soup.find()` returns a `Tag` or `None`.

## .get_text()

A BeautifulSoup method called on a `Tag` object
that extracts all visible text from inside the element,
including text from any nested child elements.
`strip=True` removes leading and trailing whitespace.
`separator=", "` inserts a separator string between text from child elements.

## Descriptor Prefix

Text included inside an HTML tag that labels the content for human readers,
such as `"Title:"` or `"Abstract:"`.
These prefixes must be removed using `.replace()` to extract clean data values.

## Canonical Link

An HTML `<link>` tag in the `<head>` section of a page that specifies
the preferred URL for the page.
Example: `<link rel="canonical" href="https://arxiv.org/abs/2602.20021"/>`
The `href` attribute contains the URL, from which structured identifiers
like the arXiv ID can be extracted.

## AttributeValueList

A BeautifulSoup type returned when accessing an HTML attribute value
using bracket notation, e.g. `tag["href"]`.
It is not a plain Python string and does not support string methods directly.
Cast it to `str()` first: `str(tag["href"])`.

## .split()

A Python string method that splits a string into a list of substrings
using a specified separator.
Example: `"https://arxiv.org/abs/2602.20021".split("/abs/")`
returns `["https://arxiv.org", "2602.20021"]`.

## List Indexing

A way to access individual elements of a Python list by position.
Lists are zero-indexed: `[0]` is the first element, `[1]` is the second.
Negative indices count from the end: `[-1]` is the last element.

## List Comprehension

A concise Python syntax for creating a new list by applying an expression
to each item in an existing list.
Example: `[tag.get_text(strip=True) for tag in author_tags_list]`
produces a list of author name strings from a list of Tag objects.

## str.join()

A Python string method that concatenates a list of strings
into a single string, inserting the calling string between each element.
Example: `", ".join(["Alice", "Bob", "Carol"])` returns `"Alice, Bob, Carol"`.

## Pipeline

A sequence of processing stages where data flows from a source to a sink.

## EVTL (Extract, Validate, Transform, Load)

A pipeline model used in this project:

- **Extract**: fetch HTML from a web page and save it to a file
- **Validate**: parse the HTML and confirm expected structure is present
- **Transform**: extract fields and reshape into a structured format
- **Load**: write the data to a destination

## Source

The origin of data in a pipeline stage.
In this module, the source is an HTML page fetched from the web.

## Sink

The destination where data is written after processing.
In this module, the sink is a CSV file.

## Extract

The stage of the pipeline that fetches the HTML page
and saves it as a raw file for inspection and downstream use.

## Validate

The stage of the pipeline that parses the raw HTML
and confirms that expected structural elements are present
before extraction begins.

## Transform

The stage of the pipeline that extracts fields from the parsed HTML,
cleans and normalizes the values, and assembles them into a structured record.

## Load

The stage of the pipeline that writes the processed DataFrame to a CSV file.

## DataFrame

A tabular data structure with rows and columns.
In this module, a Pandas DataFrame is used to store the extracted record.

## Pandas

A Python library for working with tabular data.
`pd.DataFrame([record])` creates a single-row DataFrame from a dictionary.

## Record

A single dictionary mapping field names to values.
In this module, one record represents one arXiv paper.

## Derived Field

A field calculated from other extracted fields rather than
read directly from the source.
Examples: `abstract_word_count` computed from the abstract string,
`author_count` computed from the authors string.

## Normalization

The process of converting data into a consistent, structured format
where each record follows the same schema.

## Fallback Value

A default value used when expected data is missing or cannot be extracted.
In this module, `"unknown"` is used as the fallback string
and `0` is used as the fallback integer.

## Reproducibility

The ability to run the same pipeline and obtain consistent results,
given the same inputs and configuration.
