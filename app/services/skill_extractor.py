import re

from app.services.skill_loader import SkillLoader


class SkillExtractor:

    loader = SkillLoader("data/skills")

    @classmethod
    def extract(cls, text: str):

        skills = cls.loader.load_skills()

        text = text.lower()

        found = []

        for skill, category in skills.items():

            escaped = re.escape(skill.lower())

            pattern = rf"(?<!\w){escaped}(?!\w)"

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                found.append(
                    {
                        "skill": skill,
                        "category": category
                    }
                )

        return sorted(
            found,
            key=lambda x: x["skill"]
        )