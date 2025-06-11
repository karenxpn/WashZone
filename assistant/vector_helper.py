import os

import chromadb
from openai import OpenAI
import json

open_ai_client = OpenAI(api_key=os.environ.get('OPENAI_SECRET_KEY'))
client = chromadb.PersistentClient(path="./chroma")

def get_serialized_representation(instance, serializer_class) -> str:
    serialized = serializer_class(instance).data
    return json.dumps(serialized, ensure_ascii=False)


def get_embedding(text: str) -> list[float]:
    response = open_ai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding

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


def add_service_to_provider_embedding(provider_id: int, service_instance, service_serializer_class):
    serialized_text = get_serialized_representation(service_instance, service_serializer_class)
    embedding = get_embedding(serialized_text)

    collection = get_collection("providers")

    # We upsert using the provider ID (document ID remains the same)
    collection.upsert(
        documents=[serialized_text],
        embeddings=[embedding],
        ids=[f"provider-{provider_id}-service-{service_instance.id}"],
        metadatas=[{
            "provider_id": str(provider_id),   # store as string for consistency in filtering
            "service_id": str(service_instance.id),
            "type": "service"
        }],
    )

def update_service_in_provider_embedding(provider_id: int, service_instance, service_serializer_class):
    # Delete the old embedding
    delete_service_from_provider_embedding(provider_id, service_instance.id)

    # Re-add with updated data
    add_service_to_provider_embedding(provider_id, service_instance, service_serializer_class)


def delete_service_from_provider_embedding(provider_id: int, service_id: int):
    collection = get_collection("providers")
    collection.delete(ids=[f"provider-{provider_id}-service-{service_id}"])

