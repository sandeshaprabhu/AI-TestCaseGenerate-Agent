from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime

search = DuckDuckGoSearchRun()


@tool
def search_tool(query: str) -> str:
    """Search the web for recent information, current events, or general facts."""
    return search.run(query)


# Wikipedia
wiki_api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki = WikipediaQueryRun(api_wrapper=wiki_api)


@tool
def wiki_tool(query: str) -> str:
    """Search Wikipedia for factual and background information."""
    return wiki.run(query)

# Save result to file


@tool
def save_text_to_file(data: str) -> str:
    """
    Saves structured research data to a text file.
    Input should be a string containing the research output.
    """
    filename = "research_output.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"
