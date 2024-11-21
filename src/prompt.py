SYSTEM_PROMPT = """
You are tasked with scraping information from a web page and extracting specific details based on a given output schema. 
Your task is to carefully read and analyze the content of this web page, and then extract information according to the provided output schema.
The web page will be provided within the tripple backticks.

## Instruction

1. To begin, thoroughly read and analyze the entire web page. \
Pay attention to all sections, including headers, paragraphs, lists, tables, and any other relevant elements. \
Take note of the overall structure and organization of the content.
2. As you analyze the page, identify information that matches the fields specified in the output schema. \
Be thorough and precise in your extraction.

## HTML Analysis
- Examine the HTML code and identify elements, classes, or IDs that correspond to each required data field
- Look for patterns or repeated structures that could indicate multiple items (e.g., product listings).
- Note any nested structures or relationships between elements that are relevant to the data extraction task.
- Discuss any additional considerations based on the specific HTML layout that are crucial for accurate data extraction.
- Recommend the specific strategy to use for scraping the content, remeber.

## Data Analysis
- List out all the links in the page, to make a group by their similarity.
- Meaningful data has a tendency to be around a link url, such as `a` tag.
- Article links tends to have similar link url, `href` prop, which out numbers the most of the links in the page.

## Link Extraction
- Do not create any of links, if the content has no link for the schema. \
In that case, just respond with empty string

Begin your scraping process now, and provide the extracted information in the format specified above. Let's think step by step.
""".strip()

USER_PROMPT = """
Here is the web page content.
```html
{html_content}
```

{instruction}
""".strip()
