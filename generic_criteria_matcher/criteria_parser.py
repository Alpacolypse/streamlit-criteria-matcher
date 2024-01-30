from langchain_openai import ChatOpenAI
from generic_criteria_matcher.prompt_config import (
    CRITERIA_PYDANTIC_PARSER,
    CRITIERA_PARSE_PROMPT_TEMPLATE   
)
from unstructured.partition.pdf import partition_pdf


MODEL_NAME = "gpt-4"

class CriteriaParser:
    """Parses a raw criteria string into a Criteria object using an LLM"""
    def __init__(self):
        self.model = ChatOpenAI(temperature=0, model=MODEL_NAME)

    def parse(self, raw_criteria_path):

        raw_pdf_elements = partition_pdf(
            filename=raw_criteria_path,
            extract_images_in_pdf=False,
            infer_table_structure=False,
        )

        raw_criteria = [str(element) for element in raw_pdf_elements]

        chain = CRITIERA_PARSE_PROMPT_TEMPLATE | self.model | CRITERIA_PYDANTIC_PARSER

        criteria_obj = chain.invoke({"raw_criteria": raw_criteria})
        return criteria_obj
    
    def parse_raw(self, raw_criteria):
        
        chain = CRITIERA_PARSE_PROMPT_TEMPLATE | self.model | CRITERIA_PYDANTIC_PARSER

        criteria_obj = chain.invoke({"raw_criteria": raw_criteria})
        return criteria_obj
