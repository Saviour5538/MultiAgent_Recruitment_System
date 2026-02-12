import re
from models.candidate import Candidate

class ResumeParserAgent:
    def __init__(self):
        self.skill_keywords = [
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust",
            "sql", "mysql", "postgresql", "mongodb", "oracle", "redis",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
            "react", "angular", "vue", "node", "django", "flask", "spring",
            "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
            "git", "linux", "agile", "scrum", "jira", "confluence"
        ]
    
    def parse(self, text):
        candidate = Candidate()
        candidate.raw_text = text
        
        lines = text.split('\n')
        for line in lines[:15]:
            line = line.strip()
            if line and not candidate.name:
                words = line.split()
                if 2 <= len(words) <= 4:
                    candidate.name = line
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            candidate.email = emails[0]
        
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            candidate.phone = phones[0]
        
        text_lower = text.lower()
        for skill in self.skill_keywords:
            if skill in text_lower:
                candidate.skills.append(skill)
        
        exp_pattern = r'(\d+)\+?\s*(?:years|yrs)'
        exp_matches = re.findall(exp_pattern, text_lower)
        if exp_matches:
            candidate.experience_years = int(exp_matches[0])
        
        return candidate