from generic_criteria_matcher.document_knowledge_base import DocumentKnowledgeBase
from generic_criteria_matcher.criteria_matcher import CriteriaMatcher
from generic_criteria_matcher.criteria_parser import CriteriaParser

class Orchestrator:
    def __init__(self):
        self.criteria_matcher = CriteriaMatcher()
        self.criteria_parser = CriteriaParser()

    def evaluate_document(self, raw_criteria, file_path):
        # Create knowledge base from medical record
        record_knowledge_base = DocumentKnowledgeBase(file_path)

        criteria = self.criteria_parser.parse_raw(raw_criteria)
        
        criteria_out = self.criteria_matcher.match(
            criteria, record_knowledge_base
        )

        return criteria_out
    
    
