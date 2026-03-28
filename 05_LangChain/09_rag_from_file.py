from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("AIMLAPI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("AIMLAPI_API_KEY"),
    base_url="https://api.aimlapi.com/v1",
    check_embedding_ctx_length=False,
)


# ── 1. Load the text file ────────────────────────────────────────────────────
loader = TextLoader("knowledge_base.txt", encoding="utf-8")
docs = loader.load()
print(f"Loaded {len(docs)} document(s) from knowledge_base.txt")


# ── 2. Split into chunks & store in FAISS ─────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split into {len(chunks)} chunks")

vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("Vector store created!\n")


# ── 3. RAG chain ──────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't know based on the given context."

Context:
{context}

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
questions = [
    "What is the deepest point on Earth?",
    "How many neurons does the human brain have?",
    "Who painted the Sistine Chapel ceiling?",
    "What is the fastest growing plant on Earth?",
    "How fast does the ISS travel?",
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {rag_chain.invoke(q)}\n")
