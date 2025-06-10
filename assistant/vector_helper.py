import openai
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma"))

def get_embedding(text: str) -> list[float]:
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002",
    )
    return response["data"][0]["embedding"]

def get_collection(collection_name: str):
    return client.get_or_create_collection(collection_name)

def add_to_vector_db(collection_name: str, object_id: int, text: str, metadata: dict = None):
    embedding = get_embedding(text)
    collection = get_collection(collection_name)
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(object_id)],
        metadatas=[metadata or {}],
    )

def update_in_vector_db(collection_name: str, object_id: int, text: str, metadata: dict = None):
    delete_from_vector_db(collection_name, object_id)
    add_to_vector_db(collection_name, object_id, text, metadata)

def delete_from_vector_db(collection_name: str, object_id: int):
    collection = get_collection(collection_name)
    collection.delete(ids=[str(object_id)])

def semantic_search(collection_name: str, query: str, top_k: int = 5):
    collection = get_collection(collection_name)
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
    return results

