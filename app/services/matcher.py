class Matcher:

    @staticmethod
    def match(resume_skills, jobs):
        """
        Match resume skills against available jobs.
        """

        results = []

        # Convert resume skills to lowercase for comparison
        resume_set = {skill.lower() for skill in resume_skills}

        for job in jobs:

            # Convert job skills into a list
            job_skills = [
                skill.strip()
                for skill in job["skills"].split(",")
            ]

            # Lowercase version for comparison
            job_set = {skill.lower() for skill in job_skills}

            # Skills found in both resume and job
            matched = resume_set.intersection(job_set)

            # Skills required by the job but missing from the resume
            missing = job_set.difference(resume_set)

            # Match score
            score = round(
                (len(matched) / len(job_set)) * 100
            )

            results.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "required_skills": job_skills,
                "matched_skills": sorted(list(matched)),
                "missing_skills": sorted(list(missing)),
                "match_score": score
            })

        # Highest score first
        results.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        return results