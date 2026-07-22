class ContextBuilder:

    @staticmethod
    def build(analysis, skills, match, recommendations):

        matched_skills = match.get("matched_skills", [])
        missing_skills = match.get("missing_skills", [])

        # Normalize skills to a list of strings
        skill_names = [
            skill["skill"] if isinstance(skill, dict) else str(skill)
            for skill in skills
        ]

        context = f"""
==============================
SMARTJOB AI CAREER ANALYSIS
==============================

RESUME SUMMARY
--------------
{analysis}

EXTRACTED SKILLS
----------------
{", ".join(skill_names)}

SELECTED JOB
------------
Job Title: {match.get("title", "Unknown")}

Company: {match.get("company", "Unknown")}

Location: {match.get("location", "Unknown")}

Overall Match Score:
{match.get("overall_score", 0)}%

Matched Skills
--------------
{", ".join(matched_skills)}

Missing Skills
--------------
{", ".join(missing_skills)}

SYSTEM RECOMMENDATIONS
----------------------
{chr(10).join("- " + r for r in recommendations)}

YOUR TASK

1. Evaluate the resume.
2. Explain why it matches this job.
3. Explain why the missing skills matter.
4. Produce a four-week learning roadmap.
5. Recommend portfolio projects.
6. Recommend certifications if appropriate.
7. Suggest interview preparation.
8. Give a hiring readiness score out of 100.

Do not invent qualifications.
"""

        return context