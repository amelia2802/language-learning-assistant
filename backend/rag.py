import chromadb
import os
# setup Chroma in-memory, for easy prototyping. Can add persistence easily!
client = chromadb.Client()

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
collection = client.create_collection("bangla-listing-comprehension")

# Function to read documents from a directory
def read_documents_from_directory(directory_path):
    documents = []
    metadatas = []
    ids = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                metadatas.append({"source": filename})
                ids.append(filename)
    return documents, metadatas, ids

# Directory containing text files
directory_path = "/bengali-transcripts"

# Read documents, metadatas, and ids from the directory
documents, metadatas, ids = read_documents_from_directory(directory_path)

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.add(
    documents=documents, # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
    metadatas=metadatas, # filter on these!
    ids=ids, # unique for each doc
)

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)

print(results)