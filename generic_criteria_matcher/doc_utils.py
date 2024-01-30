from langchain_core.prompts import PromptTemplate, format_document

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

MAX_DOCUMENT_LIMIT = 4  ## Needs to be fine tuned


def combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="###\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings[:MAX_DOCUMENT_LIMIT])

