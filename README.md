# Talent Acquisition Agent

AI-assisted recruitment workflow built with **Python, LangChain, LangGraph, Gemini, OpenRouter, and Pinecone**.

## What it does

The project explores how AI can support talent acquisition by analyzing candidate profiles, retrieving suitable job openings, evaluating skill alignment, calculating match scores, and routing candidates through recruitment workflows.

**Candidate flow:**

Candidate Profile → Experience Classification → Job Retrieval → Skill Assessment → Match Score → Recruitment Decision

**Job flow:**

Job JSON → LangChain Documents → NVIDIA Nemotron Embed 1B via OpenRouter → Pinecone → Semantic Retrieval

The current implementation covers the **core LangGraph recruitment workflow**, with a React frontend and FastAPI API layer planned next.

## Architecture

```text
                    TALENT ACQUISITION AGENT

                     Candidate Profile
                            │
                            ▼
                categorize_experience
                            │
                     Gemini 3.1 Flash Lite
                            │
                            ▼
                  Experience Category
                            │
                            ▼
                     retrieve_jobs
                            │
                     Pinecone Search
                            │
                            ▼
                     Retrieved Jobs
                            │
                            ▼
                     assess_skills
                            │
                     Gemini 3.1 Flash Lite
                            │
                            ▼
                   Skill Assessments
                            │
                            ▼
                calculate_match_score
                            │
                     Python Scoring
                            │
                            ▼
                     final_verdict
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           Reject       Recruiter     Assessment
                        Review
              └─────────────┼─────────────┘
                            ▼
                     WorkflowResult
```

## Job Ingestion & Retrieval

```text
                     Job JSON
                        │
                        ▼
                LangChain Document
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Searchable Text         Metadata
              │                   │
              ▼                   │
     NVIDIA Nemotron Embed 1B     │
        via OpenRouter            │
              │                   │
              └────────┬──────────┘
                       ▼
                    Pinecone
                       │
              Semantic Search
              + Metadata Filter
                       │
                       ▼
                 retrieve_jobs
```

Jobs are currently stored as JSON records and indexed in Pinecone. Retrieval filters jobs by **experience level** and **open status**, followed by semantic similarity search.

## Recruitment Workflow

```text
Candidate
    ↓
categorize_experience
    ↓
retrieve_jobs
    ↓
assess_skills
    ↓
calculate_match_score
    ↓
final_verdict
    │
    ├──────────────┬───────────────────┐
    ▼              ▼                   ▼
 Reject     Recruiter Review      Assessment
```

Each retrieved job is evaluated independently using LangGraph's dynamic routing.

## How the Agent Works

1. The candidate profile is classified as **fresher, experienced, or senior** using Gemini 3.1 Flash Lite.
2. The response is validated using a Pydantic schema with `category`, `confidence_score`, and `sources`.
3. Relevant open jobs are retrieved from Pinecone using semantic search and experience-level filtering.
4. Each retrieved job is assessed independently for **required** and **preferred** skills.
5. Skills are classified as `matched`, `partially_matched`, or `missing` using explicit evidence from the candidate profile.
6. A deterministic Python function calculates the match score.
7. The workflow combines the score with the LLM recommendation and routes the job to rejection, recruiter review, or assessment.
8. Each branch produces a structured `WorkflowResult` for future frontend use.

## Match Scoring

Partial matches receive **50% credit**.

```text
Required Coverage
= (Matched + 0.5 × Partial) / Total Required Skills

Preferred Coverage
= (Matched + 0.5 × Partial) / Total Preferred Skills

Final Score
= 100 × (0.70 × Required Coverage + 0.30 × Preferred Coverage)
```

When a job has no preferred skills, the required-skill coverage contributes the full score.

## Tech Stack

**Python • LangChain • LangGraph • Gemini 3.1 Flash Lite • Pydantic • OpenRouter • NVIDIA Nemotron Embed 1B • Pinecone • uv**

**Frontend (in progress):** React • Vite • Tailwind CSS

**API layer (planned):** FastAPI • REST/JSON

## Project Structure

```text
recruitement_agent/
├── src/
│   └── recruitement_agent/
│       ├── main.py
│       ├── graph.py
│       ├── schema.py
│       ├── PROMPT.py
│       ├── categorize_experience.py
│       ├── retrieve_jobs.py
│       ├── assess_skills.py
│       ├── match_score_calculations.py
│       ├── ingestion.py
│       └── jobs/
│           ├── ENG-001.json
│           ├── ENG-002.json
│           └── ...
│
├── frontend/
│   └── React + Vite application
│
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

- `graph.py` — LangGraph workflow and routing
- `schema.py` — recruitment state and structured response schemas
- `categorize_experience.py` — experience classification
- `retrieve_jobs.py` — Pinecone job retrieval
- `assess_skills.py` — per-job skill assessment
- `match_score_calculations.py` — deterministic match scoring
- `ingestion.py` — job-document creation and Pinecone ingestion
- `PROMPT.py` — LLM prompts
- `main.py` — local workflow execution/testing

## Current Progress

- [x] Experience classification
- [x] Job ingestion and Pinecone indexing
- [x] Semantic job retrieval
- [x] Skill assessment
- [x] Deterministic match scoring
- [x] Recommendation and dynamic routing
- [x] Structured workflow results
- [x] End-to-end workflow testing
- [ ] FastAPI backend
- [ ] React + Vite frontend
- [ ] Candidate View
- [ ] Recruiter View
- [ ] Deployment

## Repository

[GitHub Repository](https://github.com/Srijan-Petwal/Talent-Acquisition-Agent)

## Setup

```bash
git clone https://github.com/Srijan-Petwal/Talent-Acquisition-Agent.git
cd Talent-Acquisition-Agent
uv sync
```

Create a local `.env` file with the required **Gemini, OpenRouter, and Pinecone** credentials.

Then run the Python workflow using `uv run`.