from generic_criteria_matcher.orchestrator import Orchestrator
from generic_criteria_matcher.criteria_matcher import CriteriaMatcher
from generic_criteria_matcher.criteria_parser import CriteriaParser
from langchain_openai import ChatOpenAI
from fastapi import Depends

def get_llm_model():
    return ChatOpenAI(temperature=0, model="gpt-4")


def get_criteria_matcher(model=Depends(get_llm_model)):
    return CriteriaMatcher(model=model)

def get_criteria_parser():
    return CriteriaParser()

def get_orchestrator(
    criteria_matcher=Depends(get_criteria_matcher),
    criteria_parser=Depends(get_criteria_parser),
):
    return Orchestrator(
        criteria_matcher=criteria_matcher, criteria_parser=criteria_parser
    )
