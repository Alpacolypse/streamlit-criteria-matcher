from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from generic_criteria_matcher.models import (
    CriteriaValidity,
    Criteria
)

CRITERIA_PARSE_INSTRUCTIONS = """
Formulate the criteria from the given text. 
Each criteria must either be a CriteriaPredicate or a SubCriteria. 
The CriteriaPredicate must contain a field 'description' which describes the condition for the given criteria. 
The SubCriteria contains a list of conjunction_sub_criteria , a list of disjunction sub_criteria (OR) and a disjunction_condition.
The conjunction_sub_criteria are the criteria that must all be true for this criteria to be true. It could be an empty list, but it should always be present in the response.
The disjunction_sub_criteria are the criteria of which at least some must be true for this criteria to be true. It could be an empty list, but it should always be present in the response.
The disjunction_condition has an operator and a value. The operator is one of '>=', '<=', '>', '<', '==', '!='. The value is a number. It denotes the condition that the number of true disjunction_sub_criteria must meet for this criteria to be true.
For e.g "5 or more of the following are true" would be represented as operator='>=' and value=5.
The SubCriteria is considered to be satisfied only when all of the conjunction_sub_criteria are true, and the number of true disjunction_sub_criteria meet the disjunction_condition.
"""
#CRITERIA_PARSE_INSTRUCTIONS=""


CRITERIA_PARSE_FEW_SHOT_EXAMPLES = """
---
Input:
Type 2 Diabetes management, as indicated by 1 or more of the following:
\t Patient diagnosed with Type 2 Diabetes, as indicated by ALL of the following:
\t\t HbA1c level of 6.5% or higher
\t\t Fasting blood sugar level of 126 mg/dL or higher
\t Diabetes diagnosed in one or more first-degree relatives of any age and 2 of the thefollowing:
\t\t History of cardiovascular disease
\t\t Presence of kidney disease or microalbuminuria
\t\t Diabetic retinopathy or neuropathy
\t Patients not meeting targets on current management plan, indicated by:
\t\t HbA1c level above the target range set by the physician
\t\t Uncontrolled blood sugar levels despite current medication regimen
###
{
        "criteria": {
            "conjunction_sub_criteria": [],
            "disjunction_sub_criteria": [
                {
                    "criteria": {
                        "conjunction_sub_criteria": [
                            {
                                "criteria": {
                                    "description": "HbA1c level of 6.5% or higher"
                                }
                            },
                            {
                                "criteria": {
                                    "description": "Fasting blood sugar level of 126 mg/dL or higher"
                                }
                            }
                        ],
                        "disjunction_sub_criteria": [],
                        "disjunction_condition": {
                            "operator": "==",
                            "value": 0
                        }
                    }
                },
                
                {
                    "criteria": {
                        "conjunction_sub_criteria": [
                            {
                                "criteria": {
                                    "description": "Diabetes diagnosed in one or more first-degree relatives of any age"
                                }
                            }
                        ],
                        "disjunction_sub_criteria": [
                            {
                                "criteria": {
                                    "description": "History of cardiovascular disease"
                                }
                            },
                            {
                                "criteria": {
                                    "description": "Presence of kidney disease or microalbuminuria"
                                }
                            },
                            {
                                "criteria": {
                                    "description": "Diabetic retinopathy or neuropathy"
                                }
                            }
                        ],
                        "disjunction_condition": {
                            "operator": ">=",
                            "value": 2
                        }
                    }
                },
                {
                    "criteria": {
                        "conjunction_sub_criteria": [
                            {
                                "criteria": {
                                    "description": "HbA1c level above the target range set by the physician"
                                }
                            },
                            {
                                "criteria": {
                                    "description": "Uncontrolled blood sugar levels despite current medication regimen"
                                }
                            }
                        ],
                        "disjunction_sub_criteria": [],
                        "disjunction_condition": {
                            "operator": "==",
                            "value": 0
                        }
                    }
                }
            ],
            "disjunction_condition": {
                "operator": ">=",
                "value": 1
            }
        }
    }
---
Input:"""


CRITERIA_PYDANTIC_PARSER = PydanticOutputParser(pydantic_object=Criteria)

CRITIERA_PARSE_PROMPT_TEMPLATE = PromptTemplate(
    template="\n{format_instructions}\n{instructions}\n{few_shot_examples}\n{raw_criteria}\n###\n",
    input_variables=["raw_criteria"],
    partial_variables={
        "format_instructions": CRITERIA_PYDANTIC_PARSER.get_format_instructions(),
        "instructions": CRITERIA_PARSE_INSTRUCTIONS,
        "few_shot_examples": CRITERIA_PARSE_FEW_SHOT_EXAMPLES,
    },
)

def get_structured_output_with_context_template(structured_output_parser, instructions):
    return PromptTemplate(
        template="""Given the following 'Context' about the medical patient, answer the query. 
                          Context: {context}
                          ##### END OF CONTEXT ##### 
                          Query: {query}
                          ##### END OF QUERY #####
                          Follow the instructions below to format your response.
                          Formatting instructions: {format_instructions}
                          {input_instructions}""",
        input_variables=["context", "query"],
        partial_variables={
            "format_instructions": structured_output_parser.get_format_instructions(),
            "input_instructions": instructions,
        },
    )

CRITERIA_VALIDY_INPUT_INSTRUCTIONS = """Assume that any medical/treatment history of the patient provided is complete and authoritative. 
In your response,'decision' should contain whether the given query about the patient is true, false or uncertain. 
Respond with 'true' only when there is concrete evidence to support the statement. Respond with 'false' only when there is concrete evidence against it. 
Respond with 'uncertain' if there is no information about the statement.
'reason' should contain the reason why you think the query is true/false/uncertain and the relevant section of the document that supports your answer."""

CRITERIA_VALIDITY_PARSER = PydanticOutputParser(pydantic_object=CriteriaValidity)
CRITERIA_VALIDITY_PROMPT_TEMPLATE = get_structured_output_with_context_template(
    CRITERIA_VALIDITY_PARSER, CRITERIA_VALIDY_INPUT_INSTRUCTIONS
)
