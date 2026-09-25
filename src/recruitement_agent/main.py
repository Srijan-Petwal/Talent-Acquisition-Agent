from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

from langchain_core.messages import HumanMessage

from recruitement_agent.categorize_experience import categorize_experience


test_state = {
    "messages": [
        HumanMessage(
            content="""
                        Candidate Profile

                Name: Ananya Sharma

                Education:
                B.Tech in Computer Science and Engineering
                Graphic Era Hill University
                2022 - 2026

                Experience:
                Software Engineering Intern — Microsoft
                May 2025 - July 2025
                - Developed REST APIs using Python and FastAPI.
                - Wrote unit tests and improved API test coverage.
                - Collaborated with the backend engineering team.

                Projects:
                - Built a food nutrition analysis application using Python,
                scikit-learn, React, and MongoDB.
                - Developed a recommendation system using Python and cosine similarity.

                Skills:
                Python, Java, JavaScript, React, SQL, MongoDB, Git, Docker

                Current Status:
                Final-year undergraduate student seeking a full-time software
                engineering position after graduation.
            """
        )
    ],
    "experience": None,
}


result = categorize_experience(test_state)

print("\n=== RESULT ===")
print(result)

print("\n=== EXPERIENCE ===")
print(result["experience"])

print("\n=== CATEGORY ===")
print(result["experience"].category)

print("\n=== CONFIDENCE ===")
print(result["experience"].confidence_score)

print("\n=== SOURCES ===")
for source in result["experience"].sources:
    print("-", source)