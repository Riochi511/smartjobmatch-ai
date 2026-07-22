from app.services.skill_loader import SkillLoader

loader = SkillLoader("data/skills.csv")

skills = loader.load_skills()

print(skills)