from app.ai.vector_search import VectorSearch

resume = """
Python
Machine Learning
Docker
FastAPI
SQL
"""

results = VectorSearch.search(
    resume,
    top_k=3
)

for job in results:
    print(job)