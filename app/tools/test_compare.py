from app.tools.comparecompanies_tool import compare_companies

query = "Compare Apple and NVIDIA's financial performance for 2025"
response = compare_companies.invoke({"query": query})
print(response)
