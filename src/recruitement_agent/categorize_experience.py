from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from recruitement_agent.schema import ExperienceCategoryResponse,RecruitmentState
from recruitement_agent.PROMPT import CATEGORIZATION_PROMPT

load_dotenv()

llm=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0
)



def categorize_experience(state:RecruitmentState)->RecruitmentState:
    """Run the agent experience catgorization node."""

    agent=create_agent(model=llm,
                       response_format=ExperienceCategoryResponse,
                       system_prompt=CATEGORIZATION_PROMPT)
    
    response=agent.invoke({"messages":state["messages"]})

    return {"messages":response["messages"],
            "experience":response["structured_response"]
            }


    



