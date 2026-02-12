from agents.extractor import PDFExtractorAgent
from agents.parser import ResumeParserAgent
from agents.matcher import MatchingAgent
from agents.curriculum import CurriculumAgent
from agents.decision import DecisionAgent

class RecruitmentOrchestrator:
    def __init__(self):
        self.extractor = PDFExtractorAgent()
        self.parser = ResumeParserAgent()
        self.matcher = MatchingAgent()
        self.curriculum = CurriculumAgent()
        self.decision = DecisionAgent()
    
    def run(self, pdf_path, job):
        try:
            # Step 1: Extract text from PDF
            raw_text = self.extractor.extract_text(pdf_path)
            
            # Step 2: Parse resume into structured data
            candidate = self.parser.parse(raw_text)
            
            # Step 3: Match candidate against job
            match_result = self.matcher.calculate_score(candidate, job)
            
            # Step 4: Generate learning recommendations if score is low
            recommendations = []
            if match_result["final_score"] < 0.6:
                recommendations = self.curriculum.generate_recommendations(
                    match_result["missing_skills"]
                )
            
            # Step 5: Make final decision
            decision = self.decision.decide(match_result, candidate)
            
            return {
                "candidate": candidate,
                "match_result": match_result,
                "recommendations": recommendations,
                "decision": decision,
                "error": None
            }
            
        except Exception as e:
            return {
                "candidate": None,
                "match_result": None,
                "recommendations": [],
                "decision": {"decision": "ERROR", "reason": str(e)},
                "error": str(e)
            }