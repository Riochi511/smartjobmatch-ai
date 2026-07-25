# 🤖 SmartJob AI

**AI-Powered Resume Analysis, Hybrid Job Matching & Career Coaching Platform**

A production-ready AI application that analyzes resumes, semantically matches candidates to relevant job opportunities using Sentence Transformers + FAISS, explains every match, and delivers personalized career coaching through Large Language Models.

**Live Demo:** https://smartjob-ai-528680050748.us-central1.run.app
**API Docs:** https://smartjob-ai-528680050748.us-central1.run.app/docs

## 📖 Overview

SmartJob AI is a full-stack AI product that helps job seekers understand how well their resume matches real job openings and what they should improve.

It goes beyond simple keyword matching by combining:
- Semantic understanding (Sentence Transformers)
- High-speed vector search (FAISS)
- Keyword re-ranking
- Explainable match reasons
- LLM-powered career coaching

## ✨ Key Features

### 1. Intelligent Resume Analysis
- PDF resume parsing
- Skill extraction across multiple categories
- Resume strength & weakness detection

### 2. Hybrid AI Job Matching
- Semantic retrieval with Sentence Transformers
- FAISS vector search over thousands of jobs
- Keyword re-ranking
- Returns the Top 10 best matches

### 3. Match Explainability (New)
Every job match now includes:
- Why this matched
- Gap Severity (None / Low / Medium / High)
- Actionable Suggestion

### 4. AI Career Coach
Powered by OpenRouter LLMs. Provides:
- Resume strengths & gaps
- Personalized learning roadmap
- Portfolio project ideas
- Interview preparation tips

### 5. Production Architecture
- FastAPI backend
- React + Vite frontend
- Google Cloud Storage for large embedding files
- Deployed on Google Cloud Run
- Dockerized & production-ready

## 🏗 System Architecture

```
Resume Upload
     │
     ▼
Document Parser + Text Cleaning
     │
     ▼
Skill Extraction + Resume Analysis
     │
     ▼
Sentence Transformer Embeddings
     │
     ▼
FAISS Semantic Retrieval (Top 200)
     │
     ▼
Keyword Re-ranking + Hybrid Scoring
     │
     ▼
Match Explainer (Why matched + Gap + Suggestion)
     │
     ▼
Top 10 Jobs + AI Career Coach
```

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.12 |
| AI / NLP | Sentence Transformers, FAISS, PyTorch |
| LLM | OpenRouter (DeepSeek) |
| Frontend | React + Vite + Tailwind |
| Storage | Google Cloud Storage |
| Deployment | Google Cloud Run + Docker |
| Document Parsing | PyMuPDF, python-docx |

## 📂 Project Structure

```
app/
├── ai/                  # HybridMatcher, SemanticMatcher, FAISS
├── api/                 # FastAPI routers
├── llm/                 # Career Coach + prompts
├── services/            # Business logic, MatchExplainer, DataDownloader
├── exceptions/
├── utils/
└── main.py

frontend/                # React + Vite application
data/
├── raw/                 # jobs.csv (loaded from GCS in production)
├── embeddings/          # FAISS index + embeddings (loaded from GCS)
└── skills/

Dockerfile
Procfile
```

## 🚀 Live Deployment

The backend is live on Google Cloud Run:
- **Service URL:** https://smartjob-ai-528680050748.us-central1.run.app
- **Swagger UI:** https://smartjob-ai-528680050748.us-central1.run.app/docs

Large embedding files are stored in Google Cloud Storage and downloaded on first request (lazy loading).

## 📡 API Endpoints

**Match Resume**
`POST /jobs/match`
Upload a PDF resume → returns analysis + top 10 jobs with explanations.

**Career Coach**
`POST /career-coach/?job_index=0`
Generate personalized career advice for a specific matched job.

## 🖥 Local Development

```bash
# Clone
git clone https://github.com/Riochi511/smartjobmatch-ai.git
cd smartjobmatch-ai

# Backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Environment
cp .env.example .env
# Add your OPENROUTER_API_KEY and GCS_BUCKET

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
echo "VITE_API_URL=http://127.0.0.1:8000" > .env
npm run dev
```

## 🧠 How Matching Works

1. Resume is parsed and cleaned
2. Skills are extracted
3. Resume is embedded with `all-MiniLM-L6-v2`
4. FAISS retrieves the top 200 semantically similar jobs
5. Keyword matching re-ranks the candidates
6. Hybrid score is calculated
7. MatchExplainer generates human-readable reasons + gap analysis
8. Top 10 results are returned

## 🗺 Roadmap

**Completed (v1.1)**
- [x] Resume parsing (PDF)
- [x] Hybrid semantic + keyword matching
- [x] Top-10 ranked results
- [x] Match explainability
- [x] AI Career Coach
- [x] Google Cloud Run deployment
- [x] GCS integration for large files
- [x] Full frontend integration

**Future**
- [ ] User accounts & history
- [ ] Live job board APIs
- [ ] Resume improvement suggestions with rewrite
- [ ] Employer-facing dashboard

## 👨‍💻 Author

**Alfred Bright Riochi**
AI/ML Engineer focused on building practical, production-ready intelligent systems.

- GitHub: https://github.com/Riochi511
- LinkedIn: https://www.linkedin.com/in/riochi-ai453b9

## 📄 License

This project is licensed under the MIT License.