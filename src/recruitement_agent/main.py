from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from recruitement_agent.graph import graph

load_dotenv()


def main():

    candidate_profile = """
            Candidate: Aarav Mehta

            Education:
            B.Tech in Computer Science and Engineering
            National Institute of Technology, Jaipur
            2021 - 2025

            Experience:
            Backend Software Engineer Intern
            TechNova Solutions
            June 2024 - December 2024

            During the internship, developed backend services using Python,
            FastAPI, and PostgreSQL. Built and consumed REST APIs for internal
            applications and integrated third-party APIs.

            Technical Skills:
            Python, Java, SQL, JavaScript
            FastAPI, Django, React
            PostgreSQL, MongoDB
            REST APIs
            Docker, Git, AWS
            Unit Testing, CI/CD

            Projects:

            1. E-Commerce Backend
            - Developed REST APIs using Python and FastAPI.
            - Designed PostgreSQL database schemas and queries.
            - Implemented authentication and authorization.
            - Containerized the application using Docker.
            - Wrote unit tests using pytest.

            2. Customer Analytics Dashboard
            - Built a React frontend with a Python backend.
            - Used PostgreSQL for data storage.
            - Implemented REST APIs for communication between frontend
            and backend.
            - Deployed the application on AWS.

            3. ML Customer Churn Prediction
            - Built a machine learning model using Scikit-learn.
            - Used Python, Pandas and NumPy for data processing.
            - Exposed the trained model through a FastAPI endpoint.

            Certifications:
            AWS Cloud Practitioner
            Python for Everybody
            """
    
    initial_state = {
            "messages": [
                HumanMessage(content=candidate_profile)
            ],
            "experience": None,
            "retrieved_jobs": [],
            "skill_assessments": [],
            "match_scores": {},
            "workflow_results": []
        }
    
    final_state = graph.invoke(initial_state)

    print("\n========== EXPERIENCE ==========")
    print(final_state["experience"])

    print("\n========== RETRIEVED JOBS ==========")
    for job in final_state["retrieved_jobs"]:
        print(f"\nJob ID: {job.metadata['job_id']}")
        print(f"Title: {job.metadata.get('title')}")
        print(f"Location: {job.metadata.get('location')}")

    print("\n========== SKILL ASSESSMENTS ==========")
    for assessment in final_state["skill_assessments"]:
        print(f"\nJob ID: {assessment.job_id}")

        print(f"Required matched: {assessment.required_skills.matched}")
        print(
            f"Required partial: "
            f"{assessment.required_skills.partially_matched}"
        )
        print(f"Required missing: {assessment.required_skills.missing}")

        print(f"Preferred matched: {assessment.preferred_skills.matched}")
        print(
            f"Preferred partial: "
            f"{assessment.preferred_skills.partially_matched}"
        )
        print(f"Preferred missing: {assessment.preferred_skills.missing}")

        print(f"Reasoning: {assessment.reasoning}")
        print(f"LLM Recommendation: {assessment.recommendation}")

    print("\n========== MATCH SCORES ==========")
    for job_id, score in final_state["match_scores"].items():
        print(f"{job_id}: {score}")

    print("\n========== FINAL WORKFLOW RESULTS ==========")
    for result in final_state["workflow_results"]:
        print(f"\nJob ID: {result.job_id}")
        print(f"Match Score: {result.match_score}")
        print(f"Final Recommendation: {result.recommendation}")
        print(f"Status: {result.status}")

    print("\n========== WORKFLOW COMPLETE ==========")


if __name__ == "__main__":
    main()