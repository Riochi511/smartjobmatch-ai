import re


class Matcher:

    @staticmethod
    def match(resume_skills, candidate_jobs):

        results = []

        # Normalize resume skills to lowercase set
        if resume_skills and isinstance(resume_skills[0], dict):
            resume_set = {
                item["skill"].lower()
                for item in resume_skills
            }
        else:
            resume_set = {
                skill.strip().lower()
                for skill in resume_skills
            }

        for job in candidate_jobs:

            # Prefer pre-extracted job skills if available
            job_skills = job.get("required_skills") or []

            if not job_skills:
                # Fallback: extract from description
                description = str(job.get("description", "")).lower()
                job_skills = []
                for skill in resume_set:
                    pattern = r"\b" + re.escape(skill) + r"\b"
                    if re.search(pattern, description):
                        job_skills.append(skill)

            job_set = {s.lower() for s in job_skills}

            # Correct comparison
            matched_set = resume_set & job_set
            missing_set = job_set - resume_set

            if job_set:
                keyword_score = round(
                    (len(matched_set) / len(job_set)) * 100, 2
                )
            else:
                keyword_score = 0.0

            results.append({
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "company": job.get("company_name") or job.get("company"),
                "location": job.get("location"),
                "industry": job.get("industry_name") or job.get("industry"),
                "employment_type": job.get("formatted_work_type") or job.get("employment_type"),
                "experience_level": job.get("formatted_experience_level") or job.get("experience_level"),

                "required_skills": sorted(list(job_set)),
                "matched_skills": sorted(list(matched_set)),
                "missing_skills": sorted(list(missing_set)),

                "keyword_score": keyword_score,
                "semantic_score": job.get("semantic_score", 0.0)
            })

        return results