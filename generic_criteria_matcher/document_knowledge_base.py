import uuid

from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from unstructured.partition.pdf import partition_pdf
from langchain.globals import set_debug, set_verbose
from generic_criteria_matcher.doc_utils import combine_documents
import os

# turn on wandb logging for langchain
# os.environ["LANGCHAIN_WANDB_TRACING"] = "true"
# os.environ["WANDB_PROJECT"] = "criteria-matcher-tracing"

# set_verbose(True)
#set_debug(True)

MODEL_NAME = "gpt-4"

class DocumentKnowledgeBase:
    def __init__(self, file_path):
        self.path = "data/records"
        self.model = ChatOpenAI(temperature=0, model=MODEL_NAME)
        self.retriever = self._ingest(file_path)

    def get_relevant_documents(self, query):
        return self._get_document_query_chain().invoke(query)

    def _ingest(self, file_path):
        raw_pdf_elements = partition_pdf(
            filename=file_path,
            # Unstructured first finds embedded image blocks
            extract_images_in_pdf=False,
            # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
            # Titles are any sub-section of the document
            infer_table_structure=True,
            # Post processing to aggregate text once we have the title
            chunking_strategy="by_title",
            # Chunking params to aggregate text blocks
            max_characters=2000,
            new_after_n_chars=1000,
            # combine_text_under_n_chars=2000,
            image_output_dir_path=self.path,
        )

        # Categorize by type
        tables = []
        sections = []
        id_key = "doc_id"

        for element in raw_pdf_elements:
            if "unstructured.documents.elements.CompositeElement" in str(type(element)):
                sections.append(str(element))
            if "unstructured.documents.elements.Table" in str(type(element)):
                tables.append(str(element))

        summary_tables = []
        if tables:
            prompt_text = """You are an assistant tasked with summarizing tables and text. \ 
            Give a concise summary of the table or text. Table or text chunk: {element} """
            prompt = ChatPromptTemplate.from_template(prompt_text)
            summarize_chain = (
                {"element": lambda x: x} | prompt | self.model | StrOutputParser()
            )
            table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})
            table_ids = [str(uuid.uuid4()) for _ in tables]
            summary_tables = [
                Document(page_content=s, metadata={id_key: table_ids[i]})
                for i, s in enumerate(table_summaries)
            ]

        # Add texts
        doc_ids = [str(uuid.uuid4()) for _ in sections]
        section_docs = [
            Document(page_content=s, metadata={id_key: doc_ids[i]})
            for i, s in enumerate(sections)
        ]

        documents = section_docs + summary_tables
        print(len(documents))
        # The vectorstore to use to index the child chunks
        vectordb = Chroma.from_documents(
            documents=documents,
            embedding=OpenAIEmbeddings(),
            collection_name=str(uuid.uuid4()),
        )

        # Generates multiple versions of given query and retrieves the most relevant documents for each query
        # thereby increasing the chances of retrieving the most relevant documents
        retriever = MultiQueryRetriever.from_llm(
            retriever=vectordb.as_retriever(), llm=self.model
        )

        return retriever

    def _get_document_query_chain(self):
        chain = self.retriever | combine_documents

        return chain
