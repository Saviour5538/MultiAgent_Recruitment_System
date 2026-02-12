class Job:
    def __init__(self, title, required_skills, preferred_skills, min_experience):
        self.title = title
        self.required_skills = [s.lower().strip() for s in required_skills if s.strip()]
        self.preferred_skills = [s.lower().strip() for s in preferred_skills if s.strip()]
        self.min_experience = min_experience
        
    def to_dict(self):
        return {
            "title": self.title,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "min_experience": self.min_experience
        }