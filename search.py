import sys

import chromadb

# open the database saved by index.py
# get_collection (not get_or_create) raises an error if index.py hasn't been run yet
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="code_chunks") # inside here, there is an embedding model 
#that can embed the query and compare it to the embeddings of the functions in the database

# read the question from the command line, e.g. python search.py how does X work
query = " ".join(sys.argv[1:])
# Chroma embeds the query with the same model used in index.py,
# then returns the 3 closest functions
results = collection.query(query_texts=[query], n_results=3)

print(f"question:{query}\n")
for meta, distance in zip(results["metadatas"][0], results["distances"][0]):
    print(f"{distance:.3f}  {meta['name']:<16} {meta['file']}:{meta['start_line']}-{meta['end_line']}")