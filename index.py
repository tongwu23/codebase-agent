# put all the functions in the repo into a chroma_db database
from pathlib import Path

import chromadb
# add extract_top_level to the imports
from chunk import extract_functions, extract_top_level

REPO = Path("../tractian_dashboard")

# open the chroma_db database, if it doesn't exist, create it
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="code_chunks")

# extract all the functions into chunks using chunk.py
chunks = []
for py_file in REPO.rglob("*.py"):
    chunks.extend(extract_functions(py_file))
    chunks.extend(extract_top_level(py_file))

# save the chunks into the chroma_db database, with their name, file, start_line, end_line as metadata
collection.upsert(
    ids=[f"{c['file']}:{c['start_line']}" for c in chunks],
    documents=[c["code"] for c in chunks],
    metadatas=[
        {
            "name": c["name"],
            "file": c["file"],
            "start_line": c["start_line"],
            "end_line": c["end_line"],
        }
        for c in chunks
    ],
)

print(f"save {collection.count()} functions to chroma_db")