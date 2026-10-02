import os 
from recruitement_agent.schema import RecruitmentState
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings


embeddings= OpenAIEmbeddings(
    model="nvidia/nemotron-3-embed-1b:free",
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    check_embedding_ctx_length=False,
    chunk_size=50,
    retry_min_seconds=10
)


vectorstore=PineconeVectorStore(index_name=os.environ.get('INDEX_NAME'), embedding=embeddings)

def retrieve_jobs(state: RecruitmentState) -> RecruitmentState:
    # 1. Get experience classification
    if state["experience"] is None:
        raise ValueError("Experience classification is missing")
    
    experience = state["experience"].category

    # 2. Get candidate context from messages
    messages = state["messages"]

    # 3. Pinecone filtered semantic search

    candidate_query = messages[0].content

    jobs_by_category = vectorstore.similarity_search(
        query=candidate_query,
        k=2,
        filter={
            "expected_experience_level": experience,
            "status":"open"
        }
    )

    print(f"Retrieval completed!")
    
    return {
        **state,
        "retrieved_jobs": jobs_by_category
    }