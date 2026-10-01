from typing import List,Dict
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
import os
import json
from pathlib import Path

load_dotenv()

BATCH_SIZE=10

embeddings=OpenAIEmbeddings(
    model="nvidia/nemotron-3-embed-1b:free",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1/",
    check_embedding_ctx_length=False,
    chunk_size=50,
    retry_min_seconds=10
)

vectorstore=PineconeVectorStore(index_name=os.environ.get("INDEX_NAME"), embedding=embeddings)


def prepare_jobs_for_ingestion(job:Dict)->Document:
    features=[
        f"Job Title:{job['title']}",
        f"Experience Level: {job['expected_experience_level']}",
        f"Required Skills: {', '.join(job['required_skills'])}",
        f"Preferred Skills: {', '.join(job['preferred_skills'])}",
        f"Responsibilities: {', '.join(job['responsibilities'])}",
        f"Description: {job['description']}"
    ]

    text="\n\n".join(features)
    metadata={
       "job_id": job["job_id"],
        "title": job["title"],
        "department": job["department"],
        "location": job["location"],
        "urgency": job["urgency"],
        "expected_experience_level": job["expected_experience_level"],
        "status": job["status"],
    }

    return Document(
        id=job['job_id'],
        page_content=text,
        metadata=metadata,
        )
    

def main():
    print("Ingestion begins!")

    all_docs=[]

    jobs_dir=Path('jobs')

    for job_file in jobs_dir.glob("*.json"):
        with open(job_file, "r",encoding="utf-8") as fs:
            job=json.load(fs)

        doc=prepare_jobs_for_ingestion(job)
        all_docs.append(doc)

    print(f"Total jobs for ingestion:{len(all_docs)}")

    batch_size=BATCH_SIZE
    batches=[all_docs[i:i+batch_size] for i in range(0,len(all_docs),batch_size)]


    for i,batch in enumerate(batches):
        try:
            vectorstore.add_documents(batch)
        except Exception as e:
            print(f"error at storing batch{i+1}:{e}")

    print(f"Total Batches:{len(batches)}")
    print("Ingestion complete")
    #print(all_docs[0])
    
if __name__=="__main__":
    main()



