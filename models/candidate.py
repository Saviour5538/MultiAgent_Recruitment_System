class Candidate:
    def __init__(self):
        self.name = None
        self.email = None
        self.phone = None
        self.skills = []
        self.experience_years = 0
        self.experience_details = []
        self.education = []
        self.certifications = []
        self.raw_text = ""
        
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills,
            "experience_years": self.experience_years,
            "raw_text": self.raw_text[:500]
        }