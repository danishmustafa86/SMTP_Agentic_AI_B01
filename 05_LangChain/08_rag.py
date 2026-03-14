from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)


# ── 1. Documents ── our "knowledge base" ─────────────────────────────────────
docs = [
    Document(page_content="LangChain is a framework for building LLM-powered apps."),
    Document(page_content="LCEL stands for LangChain Expression Language. It uses | to chain steps."),
    Document(page_content="Vector stores save embeddings and let you do similarity search."),
    Document(page_content="RAG means Retrieval-Augmented Generation: retrieve relevant docs, then generate."),
    Document(page_content="Agents use tools and an LLM to reason and take actions step by step."),
]


# ── 2. Split & embed → store in FAISS ────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_documents(docs)

vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


# ── 3. RAG chain ──────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_template("""
Answer using ONLY the context below. If unsure, say "I don't know."

Context: {context}

Question: {question}
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# ── 4. Ask questions ──────────────────────────────────────────────────────────
print(rag_chain.invoke("What is LCEL?"))
print(rag_chain.invoke("What does RAG stand for?"))
