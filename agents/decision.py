class DecisionAgent:
    def __init__(self, interview_threshold=0.8, review_threshold=0.6):
        self.interview_threshold = interview_threshold
        self.review_threshold = review_threshold
    
    def decide(self, match_result, candidate):
        score = match_result["final_score"]
        
        if score >= self.interview_threshold:
            decision = "INTERVIEW"
            reason = f"Candidate scores {score:.1%}. Strong match across skills and experience."
        elif score >= self.review_threshold:
            decision = "REVIEW"
            reason = f"Candidate scores {score:.1%}. Moderate match, requires human review."
        else:
            decision = "DEVELOP"
            missing_count = len(match_result["missing_skills"])
            reason = f"Candidate scores {score:.1%}. {missing_count} skill gaps identified. Learning resources provided."
        
        return {
            "decision": decision,
            "reason": reason,
            "score": score
        }