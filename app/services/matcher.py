import re


class Matcher:

    @staticmethod
    def match(resume_skills, candidate_jobs):

        results = []

        # Support both old and new skill formats
        if resume_skills and isinstance(resume_skills[0], dict):

            resume_skill_map = {
                item["skill"].lower(): item["category"]
                for item in resume_skills
            }

        else:

            resume_skill_map = {
                skill.strip().lower(): "General"
                for skill in resume_skills
            }

        resume_set = set(resume_skill_map.keys())

        for job in candidate_jobs:

            description = str(
                job.get("description", "")
            ).lower()

            matched_set = set()

            matched_categories = {}

            for skill in resume_set:

                pattern = (
                    r"\b"
                    + re.escape(skill)
                    + r"\b"
                )

                if re.search(pattern, description):

                    matched_set.add(skill)

                    matched_categories[skill] = (
                        resume_skill_map[skill]
                    )

            missing = sorted(
                list(
                    resume_set - matched_set
                )
            )

            if resume_set:

                keyword_score = round(
                    (
                        len(matched_set)
                        / len(resume_set)
                    ) * 100,
                    2
                )

            else:

                keyword_score = 0.0

            results.append({

                "job_id": job.get("job_id"),

                "title": job.get("title"),

                "company": job.get("company_name"),

                "location": job.get("location"),

                "industry": job.get("industry_name"),

                "employment_type": job.get(
                    "formatted_work_type"
                ),

                "experience_level": job.get(
                    "formatted_experience_level"
                ),

                # These will be improved in Phase 3
                "required_skills": sorted(
                    list(matched_set)
                ),

                "matched_skills": sorted(
                    list(matched_set)
                ),

                "matched_skill_categories": matched_categories,

                "missing_skills": missing,

                "keyword_score": keyword_score,

                "semantic_score": job.get(
                    "semantic_score",
                    0.0
                )

            })

        return results