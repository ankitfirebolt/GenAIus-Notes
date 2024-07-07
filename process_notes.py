from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader
from langchain_community.llms import Ollama

RAG_DATA_LOCATION = "./RAG_data"
ALLOWED_EXTENSIONS = ["*.pdf", "*.docx", "*.txt"]


class ProcessNotes:

    def __init__(self, model_name):
        self.llm = Ollama(model=model_name, temperature=0)
        self.rag_data_location = RAG_DATA_LOCATION
        self.allowed_extensions = ALLOWED_EXTENSIONS
        self.retriever = self.rag_retriever()

    def rag_retriever(self):
        documents = []
        for extension in self.allowed_extensions:
            loader = DirectoryLoader(
                self.rag_data_location, glob=extension, show_progress=True
            )
            documents += loader.load()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=300, chunk_overlap=50
        )

        # Make splits
        splits = text_splitter.split_documents(documents)
        # Index
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=HuggingFaceEmbeddings(model_name="thenlper/gte-large"),
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
        return retriever

    def generate(self, input_notes):
        # chain = (prompt_template | self.llm | StrOutputParser())
        prompt = f"""
        {input_notes}
            """
        return self.llm.invoke(prompt)

    def rag_generate(self, input_notes):

        # Prompt
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        # LLM
        llm = self.llm

        retriever = self.retriever

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return rag_chain.invoke(input_notes)
