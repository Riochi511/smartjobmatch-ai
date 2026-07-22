import re

from app.services.skill_loader import SkillLoader


class JobSkillExtractor:

    loader = SkillLoader("data/skills")

    # Load once when the application starts
    skills = loader.load_skills()

    # Fast lookup
    skill_lookup = {
        skill.lower(): category
        for skill, category in skills.items()
    }

    @classmethod
    def extract(cls, description: str):

        description = description.lower()

        # Tokenize once
        tokens = set(
            re.findall(
                r"[a-zA-Z0-9+#.\-]+",
                description
            )
        )

        matched_skills = []
        matched_categories = set()

        # Single-word skills
        for token in tokens:

            if token in cls.skill_lookup:

                matched_skills.append(token)

                matched_categories.add(
                    cls.skill_lookup[token]
                )

        # Multi-word skills
        for skill, category in cls.skill_lookup.items():

            if " " not in skill:
                continue

            if skill in description:

                matched_skills.append(skill)

                matched_categories.add(category)

        return {
            "required_skills": sorted(
                set(matched_skills)
            ),
            "required_skill_categories": sorted(
                matched_categories
            )
        }