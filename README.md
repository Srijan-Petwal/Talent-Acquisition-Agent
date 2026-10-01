# Talent Acquisition Agent

AI-assisted recruitment workflow built with **Python, LangChain/LangGraph, Gemini, OpenRouter, and Pinecone**.

## What it does

The project explores how AI can support talent acquisition by converting candidate information into structured experience signals and preparing job data for semantic retrieval.

**Candidate flow:** Candidate Profile → Gemini 3.1 Flash Lite → Structured Experience Category → Recruitment State

**Job flow:** Job JSON → LangChain Documents → OpenRouter/NVIDIA Embeddings → Pinecone → Semantic Retrieval

The current implementation focuses on the **experience-categorization agent** and the **job ingestion/vector-retrieval foundation**, with the architecture designed to be extended into a larger recruitment workflow.

## Architecture

```text
                    TALENT ACQUISITION AGENT

 Candidate Profile                         Job Records
       │                                       │
       ▼                                       ▼
 Gemini 3.1 Flash Lite                  Document Preparation
       │                                       │
       ▼                                       ▼
 Pydantic Structured Output             NVIDIA Nemotron Embed 1B
       │                                 (via OpenRouter)
       ▼                                       │
 RecruitmentState                              ▼
       │                                    Pinecone
       │                                       │
       └──────────────► Matching / Retrieval ◄─┘
                              │
                              ▼
                    Recruitment Workflow
```

### ingestion & indexing pipeline architecture
```
                        SOURCE OF TRUTH
                       MongoDB / PostgreSQL
                              │
                              │
                     ┌────────▼────────┐
                     │ Job JSON/model  │
                     └────────┬────────┘
                              │
                       ingestion pipeline
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          searchable text             metadata
                 │                         │
                 ▼                         ▼
             embedding                structured
                 │                         │
                 └────────────┬────────────┘
                              ▼
                           Pinecone
                              │
                    ┌─────────┴─────────┐
                    │                   │
             metadata filter       semantic search
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       retrieve_jobs
                              │
                              ▼
                      assess_skills
```

### Recruitement Workflow
```
                    Candidate
                        ↓
             categorize_experience
                        ↓
                 experience category
                        ↓
             retrieve matching jobs
                        ↓
              ┌─────────┴─────────┐
              ↓                   ↓
        Fresher jobs        Experienced jobs
              ↓                   ↓
              └─────────┬─────────┘  
                  assess_skills
                        ↓
             ┌──────────┼──────────┐
             ↓          ↓          ↓
           reject     escalate   interview
              └─────────┬─────────┘
                       END        
```

## Repository

https://github.com/Srijan-Petwal/Talent-Acquisition-Agent

## How the agent works

1. A candidate profile is passed into the recruitment workflow.
2. The Gemini-powered agent determines whether the candidate is **fresher, experienced, or senior**.
3. The response is validated using a Pydantic schema containing `category`, `confidence_score`, and `sources`.
4. Job records are converted into searchable LangChain Documents.
5. Job documents are embedded using **NVIDIA Nemotron Embed 1B** through OpenRouter.
6. Embeddings are stored in **Pinecone**, providing a semantic retrieval layer for future matching and recruitment workflows.

The agent is instructed to use evidence from the profile and avoid inventing missing experience.

## Tech Stack

**Python • LangChain • LangGraph • Gemini 3.1 Flash Lite • Pydantic • OpenRouter • NVIDIA Nemotron Embed 1B • Pinecone • uv**

## Project Structure

```text
src/recruitement_agent/
├── main.py
├── categorize_experience.py
├── ingestion.py
├── schema.py
├── PROMPT.py
└── ...
```

- `categorize_experience.py` — AI experience-classification agent
- `schema.py` — structured recruitment state and response schema
- `PROMPT.py` — categorization instructions
- `ingestion.py` — job-document creation and Pinecone ingestion
- `main.py` — runnable example / entry point

## Setup

```bash
git clone https://github.com/Srijan-Petwal/Talent-Acquisition-Agent.git
cd Talent-Acquisition-Agent
uv sync
```

Create a local `.env` with the required **Gemini, OpenRouter, and Pinecone** credentials/configuration used by the project.

Then run the relevant Python module with `uv run`.




