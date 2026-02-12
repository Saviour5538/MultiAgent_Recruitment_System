class CurriculumAgent:
    def __init__(self):
        self.course_database = {
            "python": {
                "title": "Python for Everybody",
                "platform": "Coursera",
                "hours": 40,
                "level": "Beginner"
            },
            "sql": {
                "title": "SQL Complete Bootcamp",
                "platform": "Udemy",
                "hours": 25,
                "level": "Beginner"
            },
            "aws": {
                "title": "AWS Certified Solutions Architect",
                "platform": "AWS Training",
                "hours": 40,
                "level": "Intermediate"
            },
            "docker": {
                "title": "Docker Mastery with Kubernetes",
                "platform": "Udemy",
                "hours": 20,
                "level": "Beginner"
            },
            "kubernetes": {
                "title": "Kubernetes for Beginners",
                "platform": "KodeKloud",
                "hours": 25,
                "level": "Intermediate"
            },
            "react": {
                "title": "React - The Complete Guide",
                "platform": "Udemy",
                "hours": 50,
                "level": "Intermediate"
            },
            "javascript": {
                "title": "JavaScript: The Complete Guide",
                "platform": "Coursera",
                "hours": 45,
                "level": "Beginner"
            },
            "tensorflow": {
                "title": "TensorFlow Developer Certificate",
                "platform": "DeepLearning.AI",
                "hours": 80,
                "level": "Advanced"
            },
            "pytorch": {
                "title": "PyTorch Zero to GANs",
                "platform": "FreeCodeCamp",
                "hours": 35,
                "level": "Intermediate"
            },
            "mongodb": {
                "title": "MongoDB University",
                "platform": "MongoDB",
                "hours": 15,
                "level": "Beginner"
            }
        }
    
    def generate_recommendations(self, missing_skills):
        recommendations = []
        
        for skill in missing_skills[:3]:
            skill_lower = skill.lower()
            if skill_lower in self.course_database:
                course = self.course_database[skill_lower].copy()
                course["skill"] = skill
                recommendations.append(course)
            else:
                recommendations.append({
                    "skill": skill,
                    "title": f"Introduction to {skill}",
                    "platform": "Various Platforms",
                    "hours": 25,
                    "level": "Beginner"
                })
        
        return recommendations