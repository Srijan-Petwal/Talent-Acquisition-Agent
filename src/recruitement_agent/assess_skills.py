from dotenv import load_dotenv
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from recruitement_agent.schema import SkillAssessmentResponse,SkillAssessmentList,RecruitmentState
from recruitement_agent.PROMPT import SKILL_ASSESSMENT_PROMPT

load_dotenv()

llm=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)


def assess_skills(state:RecruitmentState)->RecruitmentState:
    """Run the agent assess skills node responsible for assessing the candidate profile against retrieved jobs."""
       
    candidate_profile = state["messages"][0].content
    retrieved_jobs = state["retrieved_jobs"]
    #jobs_text = "\n\n--- JOB ---\n\n".join(job.page_content for job in retrieved_jobs)

    jobs_text = "\n\n--- JOB ---\n\n".join(f"job_id: {job.metadata['job_id']}\n"f"{job.page_content}" for job in retrieved_jobs)

    prompt = SKILL_ASSESSMENT_PROMPT

    agent = create_agent(
        model=llm,
        system_prompt=prompt,
        response_format=SkillAssessmentList
         )

    response=agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""
            Candidate profile:
            {candidate_profile}

            Retrieved jobs:
            {jobs_text}
            """
        }]
    })

    return { **state,
            "skill_assessments": response['structured_response'].assessments
            }