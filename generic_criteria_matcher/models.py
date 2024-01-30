# from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from typing import List, Union, Optional
from enum import Enum


class DisjunctionCondition(BaseModel):
    operator: str = Field(
        description="The operator to use to compare the number of true sub_criteria with the value. One of '>=', '<=', '>', '<', '==', '!='"
    )
    value: int = Field(
        description="The value to compare the number of true sub_criteria with"
    )


class CriteriaPredicate(BaseModel):
    description: str = Field(
        description="The statement of the criteria to be checked for"
    )


class SubCriteria(BaseModel):
    conjunction_sub_criteria: List["Criteria"] = Field(
        description="The criteria that must all be true for this criteria to be true. Can be an empty list."
    )
    disjunction_sub_criteria: List["Criteria"] = Field(
        description="The criteria of which at least some must be true for this criteria to be true. Can be an empty list."
    )
    disjunction_condition: DisjunctionCondition | None = Field(
        description="The condition that the number of true disjunction_sub_criteria must meet."
    )


class Criteria(BaseModel):
    criteria: Union[CriteriaPredicate, SubCriteria] = Field(
        description="Either a CriteriaPredicate or a SubCriteria"
    )


SubCriteria.update_forward_refs()

###########
# OUTPUTS #
###########

class DecisionEnum(str, Enum):
    true = "true"
    false = "false"
    uncertain = "uncertain"

class CriteriaValidity(BaseModel):
    ## The order here is important as the LLM is more accurate with its decision 
    ## when it first asked to come up with a reason
    reason: str = Field(description="The reason and context for the decision")
    decision: DecisionEnum = Field(
        description="Whether the criteria is 'true', 'false' or 'uncertain'"
    )  

class CriteriaPredicateOut(BaseModel):
    description: str = Field(
        description="The statement of the criteria to be checked for"
    )

class SubCriteriaOut(BaseModel):
    conjunction_sub_criteria: List["CriteriaOut"] = Field(
        description="The list of criteria that must all be true for this criteria to be true. Can be an empty list."
    )
    disjunction_sub_criteria: List["CriteriaOut"] = Field(
        description="The list criteria of which at least some must be true for this criteria to be true. Can be an empty list."
    )
    disjunction_condition: DisjunctionCondition = Field(
        description="The condition that the number of true disjunction_sub_criteria must meet."
    )


class CriteriaOut(CriteriaValidity):
    criteria: Union[CriteriaPredicateOut, SubCriteriaOut] = Field(
        description="Either a CriteriaPredicateOut or a SubCriteriaOut"
    )


SubCriteriaOut.update_forward_refs()
