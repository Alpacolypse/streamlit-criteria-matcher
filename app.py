import streamlit.components.v1 as components  # Import Streamlit
from streamlit_criteria_portal import st_criteria_tree  # Import the Custom Component class
import streamlit as st
from streamlit_quill import st_quill
import requests
from util import placeholder_criteria

st.title("Criteria Matcher")

intro = """This tool lets you comprehensively evaluate whether a given document about a person meets certain custom defined criteria or not. 
            Example use cases include screening resumes, evaluating treatment plans for patients based on guidelines, and evaluating insurance claims."""
st.write(intro)

criteria_input = st_quill(toolbar=[{"list": "ordered"}, {"list": "bullet"},], placeholder=placeholder_criteria)

target_document = st.file_uploader("Target Document", type=["pdf"])

# Button to evaluate
if st.button('Evaluate'):
    if target_document is not None and criteria_input:
        # Assuming 'evaluate-document' API accepts POST requests with criteria and file
        files = {'document_file': target_document.getvalue()}
        data = {'criteria_text': criteria_input}
        #TODO: use a proper dns
        response = requests.post("http://18.203.235.214:8000/evaluate-document/", files=files, data=data)

        if response.status_code == 200:
            output = response.json()
            st_criteria_tree(data=output)
        else:
            st.error("Error in API call")
    else:
        st.error("Please input criteria and upload a document.")



#st.markdown(create_criteria_markdown(test_json), unsafe_allow_html=True)