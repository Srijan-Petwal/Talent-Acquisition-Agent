from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from recruitement_agent.assess_skills import assess_skills
from recruitement_agent.categorize_experience import categorize_experience
from recruitement_agent.retrieve_jobs import retrieve_jobs
from recruitement_agent.match_score_calculations import calculate_match_score

from recruitement_agent.schema import RecruitmentState, JobRoutingState, WorkflowResult


load_dotenv()


REJECT = "reject_application"
FORWARD = "forward_to_recruiter"
ASSESSMENT = "schedule_assessment"


def final_verdict(state: RecruitmentState):

    routes = []

    for assessment in state["skill_assessments"]:

        job_id = assessment.job_id
        score = state["match_scores"][job_id]
        llm_recommendation = assessment.recommendation

        if score < 70:
            if llm_recommendation == REJECT:
                final_recommendation = REJECT
            else:
                final_recommendation = FORWARD
        else:
            final_recommendation = llm_recommendation

        routes.append(
            Send(
                final_recommendation,
                {
                    "job_id": job_id,
                    "match_score": score,
                    "assessment": assessment,
                    "recommendation": final_recommendation
                }
            )
        )

    return routes


def reject_application(state: JobRoutingState):
    """
    Handle jobs that should not proceed further in the workflow.
    """
    result = WorkflowResult(
        job_id=state["job_id"],
        match_score=state["match_score"],
        recommendation=state["recommendation"],
        status="rejected"
    )

    return {
        "workflow_results": [result]
    }


def forward_to_recruiter(state: JobRoutingState):
    """
    Send the job assessment to the recruiter for human review.
    """
    result = WorkflowResult(
        job_id=state["job_id"],
        match_score=state["match_score"],
        recommendation=state["recommendation"],
        status="pending_recruiter_review"
    )

    return {
        "workflow_results": [result]
    }


def schedule_assessment(state: JobRoutingState):
    """
    Mark the job for a technical/skills assessment.
    """
    result = WorkflowResult(
        job_id=state["job_id"],
        match_score=state["match_score"],
        recommendation=state["recommendation"],
        status="pending_assessment"
    )

    return {
        "workflow_results": [result]
    }


builder = StateGraph(RecruitmentState)


# Main recruitment workflow
builder.add_node("categorize_experience", categorize_experience)
builder.add_node("retrieve_jobs", retrieve_jobs)
builder.add_node("assess_skills", assess_skills)
builder.add_node("calculate_match_score", calculate_match_score)


# Per-job workflow nodes
builder.add_node(
    "reject_application",
    reject_application,
    input_schema=JobRoutingState
)

builder.add_node(
    "forward_to_recruiter",
    forward_to_recruiter,
    input_schema=JobRoutingState
)

builder.add_node(
    "schedule_assessment",
    schedule_assessment,
    input_schema=JobRoutingState
)


# Main graph
builder.add_edge(START, "categorize_experience")

builder.add_edge(
    "categorize_experience",
    "retrieve_jobs"
)

builder.add_edge(
    "retrieve_jobs",
    "assess_skills"
)

builder.add_edge(
    "assess_skills",
    "calculate_match_score"
)


# Dynamically route every assessed job
builder.add_conditional_edges(
    "calculate_match_score",
    final_verdict,
    [REJECT, FORWARD, ASSESSMENT]
)


# End each per-job branch
builder.add_edge(
    "reject_application",
    END
)

builder.add_edge(
    "forward_to_recruiter",
    END
)

builder.add_edge(
    "schedule_assessment",
    END
)


graph = builder.compile()


def main():
    graph.get_graph().draw_mermaid_png(output_file_path="flow.png")

    print("Graph saved")


if __name__ == "__main__":
    main()