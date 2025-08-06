from langchain.tools import tool

@tool
def summarize_text_block(text: str) -> str:
    """
    Clean and return the full input text for summarization by the main LLM.
    """
    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    # Re-join all cleaned lines to retain full context
    full_text = " ".join(lines)
    
    return full_text
