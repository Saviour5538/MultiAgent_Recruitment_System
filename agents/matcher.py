import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MatchingAgent:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model ready")
    
    def calculate_semantic_score(self, text1, text2):
        embeddings = self.model.encode([text1[:1000], text2[:1000]])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    
    def calculate_score(self, candidate, job):
        # Skills match
        candidate_skills = set([s.lower() for s in candidate.skills])
        required_set = set(job.required_skills)
        preferred_set = set(job.preferred_skills)
        
        matched_required = candidate_skills.intersection(required_set)
        matched_preferred = candidate_skills.intersection(preferred_set)
        
        required_score = len(matched_required) / max(len(required_set), 1)
        preferred_score = len(matched_preferred) / max(len(preferred_set), 1)
        
        skill_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        # Experience match
        if job.min_experience > 0:
            experience_score = min(1.0, candidate.experience_years / job.min_experience)
        else:
            experience_score = 1.0
        
        # Semantic match using Sentence Transformers
        job_text = job.title + " " + " ".join(job.required_skills) + " " + " ".join(job.preferred_skills)
        semantic_score = self.calculate_semantic_score(candidate.raw_text, job_text)
        
        # Final score
        final_score = (skill_score * 0.5) + (experience_score * 0.3) + (semantic_score * 0.2)
        final_score = max(0.0, min(1.0, final_score))
        
        missing_skills = list(required_set - candidate_skills)
        matched_skills = list(matched_required) + list(matched_preferred)
        
        return {
            "final_score": final_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "semantic_score": semantic_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }