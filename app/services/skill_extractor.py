from app.services.skill_loader import SkillLoader


class SkillExtractor:

    loader = SkillLoader("data/skills.csv")

    @classmethod
    def extract(cls, text: str):

        skills = cls.loader.load_skills()

        text = text.lower()

        found = []

        for skill in skills:
            if skill.lower() in text:
                found.append(skill)

        return sorted(set(found))