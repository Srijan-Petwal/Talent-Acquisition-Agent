from typing import Dict

from recruitement_agent.schema import RecruitmentState


PARTIAL_WEIGHT = 0.5
REQUIRED_WEIGHT = 0.70
PREFERRED_WEIGHT = 0.30


def calculate_match_score(state: RecruitmentState) -> RecruitmentState:
    """
    Calculate a deterministic match score for every assessed job.
    """

    match_scores: Dict[str, int] = {}

    for entry in state['skill_assessments']:

        job_id = entry.job_id

        
        # Required skills
       

        required = entry.required_skills

        total_required_skills = (
            len(required.matched)
            + len(required.partially_matched)
            + len(required.missing)
        )

        if total_required_skills > 0:
            required_coverage = (
                len(required.matched)
                + PARTIAL_WEIGHT * len(required.partially_matched)
            ) / total_required_skills
        else:
            required_coverage = 0.0

      
        # Preferred skills
        

        preferred = entry.preferred_skills

        total_preferred_skills = (
            len(preferred.matched)
            + len(preferred.partially_matched)
            + len(preferred.missing)
        )

        if total_preferred_skills > 0:
            preferred_coverage = (
                len(preferred.matched)
                + PARTIAL_WEIGHT * len(preferred.partially_matched)
            ) / total_preferred_skills
        else:
            preferred_coverage = 0.0

       
        # Final score
      

        if total_preferred_skills > 0:
            score = 100 * (
                REQUIRED_WEIGHT * required_coverage
                + PREFERRED_WEIGHT * preferred_coverage
            )
        else:
            # No preferred skills:
            # redistribute their weight to required skills.
            score = 100 * required_coverage

        match_scores[job_id] = round(score)

    return {
        **state,
        "match_scores": match_scores
    }