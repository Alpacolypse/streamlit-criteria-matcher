import streamlit.components.v1 as components  # Import Streamlit
from streamlit_criteria_portal import st_criteria_tree  # Import the Custom Component class
from generic_criteria_matcher.orchestrator import Orchestrator
import streamlit as st
from streamlit_quill import st_quill
import requests
from util import placeholder_criteria
import tempfile
import os

st.title("Criteria Matcher")

intro = """This tool lets you comprehensively evaluate whether a given document about a person meets certain custom defined criteria or not. 
            Example use cases include screening resumes, evaluating treatment plans for patients based on guidelines, and evaluating insurance claims."""
st.write(intro)

criteria_input = st_quill(toolbar=[{"list": "ordered"}, {"list": "bullet"},], placeholder=placeholder_criteria)

target_document = st.file_uploader("Target Document", type=["pdf"])

orchestrator = Orchestrator()

if st.button('Evaluate'):
    if target_document is not None and criteria_input:
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(target_document.getvalue())
                tmp_file_path = tmp_file.name

            output = orchestrator.evaluate_document(criteria_input, tmp_file_path)

            # Assuming output is in the expected format for st_criteria_tree
            st_criteria_tree(data=output.model_dump())

            # Optionally, delete the temporary file after processing
            os.remove(tmp_file_path)

        except Exception as e:
            st.error(f"Error during evaluation: {e}")
    else:
        st.error("Please input criteria and upload a document.")



#st.markdown(create_criteria_markdown(test_json), unsafe_allow_html=True)