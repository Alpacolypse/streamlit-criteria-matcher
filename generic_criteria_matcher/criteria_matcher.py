from generic_criteria_matcher.prompt_config import (
    CRITERIA_VALIDITY_PARSER,
    CRITERIA_VALIDITY_PROMPT_TEMPLATE,
)
from generic_criteria_matcher.document_knowledge_base import DocumentKnowledgeBase
from generic_criteria_matcher.utils import get_op
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from generic_criteria_matcher.models import (
    Criteria,
    CriteriaPredicate,
    SubCriteria,
    DisjunctionCondition,
    CriteriaOut,
    CriteriaPredicateOut,
    SubCriteriaOut
)
from typing import List


class CriteriaMatcher:
    """Class for matching criteria against a knowledge base. Recursively evaluates a criteria tree"""

    def __init__(self):
        self.model = ChatOpenAI(temperature=0, model="gpt-4")

    def match(self, criteria: Criteria, knowledge_base: DocumentKnowledgeBase):
        
        return self._match(criteria, knowledge_base)

    def _match(self, criteria: Criteria, knowledge_base):
        criteria = criteria.criteria
        if isinstance(criteria, CriteriaPredicate):
            return self._evaluate_predicate(criteria, knowledge_base)
        elif isinstance(criteria, SubCriteria):
            return self._evaluate_sub_criteria(criteria, knowledge_base)
        else:
            print(type(criteria))
            raise TypeError("Invalid criteria type")

    def _evaluate_predicate(
        self, predicate: CriteriaPredicate, knowledge_base: DocumentKnowledgeBase
    ):
        relevant_documents = knowledge_base.get_relevant_documents(
            predicate.description
        )

        query = PromptTemplate.from_template(
            "Is the following statement about the person true, false or uncertain? \n{query}\n"
        ).format(query=predicate.description)

        chain = (
            CRITERIA_VALIDITY_PROMPT_TEMPLATE | self.model | CRITERIA_VALIDITY_PARSER
        )

        criteria_validity = chain.invoke(
            {"context": relevant_documents, "query": query}
        )

        criteria_predicate_out = CriteriaPredicateOut(description=predicate.description)

        return CriteriaOut(criteria=criteria_predicate_out, **criteria_validity.dict())

    def _evaluate_sub_criteria(
        self, sub_criteria: SubCriteria, knowledge_base: DocumentKnowledgeBase
    ):
        conjunction_decision, conjunction_evals = self._evaluate_conjunction(
            sub_criteria.conjunction_sub_criteria, knowledge_base
        )
        disjunction_decision, disjunction_evals = self._evaluate_disjunction(
            sub_criteria.disjunction_sub_criteria,
            sub_criteria.disjunction_condition,
            knowledge_base,
        )

        decision = self._combine_decisions(conjunction_decision, disjunction_decision)
        reason = (
            f"Sub-criterias evaluate to {decision}"  # TODO: improve aggregate reasons
        )

        sub_criteria_out = SubCriteriaOut(
            description="SubCriteria Evaluation",
            conjunction_sub_criteria=conjunction_evals,
            disjunction_sub_criteria=disjunction_evals,
            disjunction_condition=sub_criteria.disjunction_condition,
        )

        return CriteriaOut(criteria=sub_criteria_out, decision=decision, reason=reason)

    def _evaluate_criteria_list(
        self, criteria_list: List[Criteria], knowledge_base: DocumentKnowledgeBase
    ):
        evals = [self._match(criteria, knowledge_base) for criteria in criteria_list]
        true_count = sum(sc.decision == "true" for sc in evals)
        uncertain_count = sum(sc.decision == "uncertain" for sc in evals)
        return true_count, uncertain_count, evals

    def _evaluate_conjunction(
        self, criteria_list: List[Criteria], knowledge_base: DocumentKnowledgeBase
    ):
        true_count, uncertain_count, evals = self._evaluate_criteria_list(
            criteria_list, knowledge_base
        )
        if true_count == len(criteria_list):
            return "true", evals
        elif true_count + uncertain_count == len(criteria_list):
            return "uncertain", evals
        else:
            return "false", evals

    def _evaluate_disjunction(
        self,
        criteria_list: List[Criteria],
        condition: DisjunctionCondition,
        knowledge_base: DocumentKnowledgeBase,
    ):
        true_count, uncertain_count, evals = self._evaluate_criteria_list(
            criteria_list, knowledge_base
        )

        if condition:
            op_function = get_op(condition.operator)
            if op_function(true_count, condition.value):
                return "true", evals
            elif op_function(true_count + uncertain_count, condition.value):
                return "uncertain", evals
            else:
                return "false", evals
        else:
            return "true" if true_count > 0 else "false"

    def _combine_decisions(self, conjunction_decision, disjunction_decision):
        if conjunction_decision == "false" or disjunction_decision == "false":
            return "false"
        if conjunction_decision == "uncertain" or disjunction_decision == "uncertain":
            return "uncertain"
        return "true"
