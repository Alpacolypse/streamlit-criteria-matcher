import streamlit as st


placeholder_criteria = """• Candidate eligible for Senior MLE interview loop as indicated by any 2 of the following:
    • PHD in Computer Science related field
    • 3+ years of industry experience
    • Expertise in ML frameworks as indicated by all of the following:
        • 4+ Open source contributions
        • Experience with pytorch
"""

sample_output = {
  "reason": "Sub-criterias evaluate to false",
  "decision": "false",
  "criteria": {
    "conjunction_sub_criteria": [
      {
        "reason": "The context mentions that the person has a Bachelor of Science degree in Computer Science from Northwestern University Evanston, USA.",
        "decision": "true",
        "criteria": {
          "description": "Candidate must have a Bachelor's"
        }
      }
    ],
    "disjunction_sub_criteria": [
      {
        "reason": "There is no information provided in the context about a dog named Rufus.",
        "decision": "uncertain",
        "criteria": {
          "description": "A dog named Rufus"
        }
      },
      {
        "reason": "The person has a minor in Film Production from Northwestern University, which indicates an interest in cinema.",
        "decision": "true",
        "criteria": {
          "description": "An interest in Cinema"
        }
      },
      {
        "reason": "The person won the Microsoft 1871 Hackathon in 2016, as stated in the 'Awards' section of the context.",
        "decision": "true",
        "criteria": {
          "description": "Hackathon award"
        }
      },
      {
        "reason": "Sub-criterias evaluate to true",
        "decision": "true",
        "criteria": {
          "conjunction_sub_criteria": [],
          "disjunction_sub_criteria": [
            {
              "reason": "The person has worked at Amazon, which is a big tech company. This is mentioned in the 'Experience' section where it states 'Software Engineer | Amazon, Seattle, USA August 2017 – September 2022'.",
              "decision": "true",
              "criteria": {
                "description": "Working at a big tech company"
              }
            },
            {
              "reason": "The context does not provide any information about the person founding their own startup.",
              "decision": "uncertain",
              "criteria": {
                "description": "founded own startup"
              }
            },
            {
              "reason": "There is no information in the provided context about the person giving a TedX talk.",
              "decision": "uncertain",
              "criteria": {
                "description": "given a TedX talk"
              }
            }
          ],
          "disjunction_condition": {
            "operator": ">=",
            "value": 1
          }
        }
      }
    ],
    "disjunction_condition": {
      "operator": "==",
      "value": 2
    }
  }
}