import React, { useEffect, useState } from "react";
import {
  ComponentProps,
  Streamlit,
  withStreamlitConnection,
} from "streamlit-component-lib";
import './CriteriaTree.css'; // Import a CSS file for styling
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown, faChevronRight } from '@fortawesome/free-solid-svg-icons';


const Tree = ({data} : any) => {

  useEffect(() => {
    Streamlit.setFrameHeight();
  });
  
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    // This will call setFrameHeight every time isExpanded changes
    Streamlit.setFrameHeight();
  }, [isExpanded]);

  const getDecisionClass = (decision : string) => {
    const decisionStr = typeof decision === 'string' ? decision.toLowerCase() : '';

    switch (decisionStr.toLowerCase()) {
      case 'true': return 'decision-true';
      case 'false': return 'decision-false';
      case 'uncertain': return 'decision-uncertain';
      default: return '';
    }
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const checkHasChildren = (criteria : any) => {
    return (criteria.conjunction_sub_criteria && criteria.conjunction_sub_criteria.length > 0) || 
      (criteria.disjunction_sub_criteria && criteria.disjunction_sub_criteria.length > 0);
  };
  
  const renderCriteria = (criteria : any) => {
    if (!criteria) return null;

    const hasChildren = checkHasChildren(criteria);

    return (
      <div className={`criteria ${hasChildren ? 'has-children' : ''}`}>
          <div className="criteria-title" onClick={hasChildren ? toggleExpand : undefined}>
            {criteria.description && (
              <>
                <strong>Criteria description:</strong> {criteria.description}
              </>
            )}
            {hasChildren && (
              <span className="toggle-indicator">
                <FontAwesomeIcon icon={isExpanded ? faChevronDown : faChevronRight} />
                <span className="toggle-text">{isExpanded ? "Collapse" : "Expand"}</span>
              </span>
            )}
          </div>

        {isExpanded && (
          <>
            {criteria.conjunction_sub_criteria.length > 0 && (
              <div>
                <strong>All of these must be true:</strong>
                {criteria.conjunction_sub_criteria.map((subCriteria=[], index=0) => (
                  <div key={index} className="sub-criteria">
                    <Tree data={subCriteria} />
                  </div>
                ))}
              </div>
            )}

            {criteria.disjunction_sub_criteria.length > 0 && criteria.disjunction_condition && (
              <div className="disjunction-condition">
                <strong> {criteria.disjunction_condition.operator} {criteria.disjunction_condition.value} of these must be true:</strong>
              </div>
            )}

            {criteria.disjunction_sub_criteria.map((subCriteria = [], index = 0) => (
              <div key={index} className="sub-criteria">
                <Tree data={subCriteria} />
              </div>
            ))}
          </>
        )}
      </div>
    );
  };


  return (
    <div className={`tree`}>
      <div><strong>Decision:</strong> <span className={`${getDecisionClass(data.decision)}`}> {data.decision} </span> </div>
      <div><strong>Reason:</strong> {data.reason}</div>
      {renderCriteria(data.criteria)}
    </div>
  );
};

const CriteriaTree = (props: ComponentProps) => {
  const {data} = props.args;
  return <Tree data={data}/>;
};

export default withStreamlitConnection(CriteriaTree);