from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── 1. TextLoader ── load a local .txt file ───────────────────────────────────
loader = TextLoader("sample.txt", encoding="utf-8")
docs = loader.load()
print(docs[0].page_content)     # raw text
print(docs[0].metadata)         # {"source": "sample.txt"}


# ── 2. WebBaseLoader ── scrape text from any URL ──────────────────────────────
# loader = WebBaseLoader("https://en.wikipedia.org/wiki/Python_(programming_language)")
# docs = loader.load()

# print(f"Pages loaded   : {len(docs)}")
# print(f"Characters     : {len(docs[0].page_content)}")
# print(f"Preview        : {docs[0].page_content[:300]}")


# # ── 3. RecursiveCharacterTextSplitter ── chop large docs into smaller chunks ──
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,     # max chars per chunk
#     chunk_overlap=50,   # overlap keeps context at boundaries
# )
# chunks = splitter.split_documents(docs)

# print(f"\nTotal chunks   : {len(chunks)}")
# print(f"First chunk    :\n{chunks[0].page_content}")

# # Every chunk keeps its source metadata
# print(f"\nMetadata       : {chunks[0].metadata}")
