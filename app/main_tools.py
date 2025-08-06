from langchain_core.tools import Tool
from app.tools.comparecompanies_tool import compare_companies
from app.tools.financialqa_tool import answer_financial_question
from app.tools.ratioanalysis_tool import ratio_analysis
from app.tools.summarizer_tool import summarize_text_block
from app.tools.qa_tool import answer_pdf_question
from app.tools.voice_tool import speak_text

# Register all tools with required metadata
all_tools = [
    Tool.from_function(compare_companies, name="compare_companies", description="Compare financials of two companies."),
    Tool.from_function(answer_financial_question, name="answer_financial_question", description="Answer financial questions using company data."),
    Tool.from_function(ratio_analysis, name="ratio_analysis", description="Perform ratio analysis for a company."),
    Tool.from_function(summarize_text_block, name="summarize_text_block", description="Summarize financial documents."),
    Tool.from_function(answer_pdf_question, name="answer_pdf_question", description="Answer questions from uploaded PDFs."),
    Tool.from_function(speak_text, name="speak_text", description="Convert financial text responses into speech.")
]
