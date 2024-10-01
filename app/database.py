import hashlib
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import torch

# Set up device for embedding model (GPU if available)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load the model once and reuse it
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device=device)

class StorageManager:
    def __init__(self, pg_config, qdrant_host="localhost", qdrant_port=6333):
        self.pg_conn = psycopg2.connect(**pg_config)
        self.pg_cursor = self.pg_conn.cursor()
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        
        # Ensure PostgreSQL and Qdrant setup
        self.ensure_pg_table()
        self.ensure_qdrant_collection()

    def ensure_pg_table(self):
        # Create table if it doesn't exist
        self.pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS text_chunks (
            chunk_number SERIAL PRIMARY KEY,
            chunk_text TEXT NOT NULL,
            source_url TEXT NOT NULL
        );
        """)
        self.pg_conn.commit()

    def ensure_qdrant_collection(self):
        # Check if Qdrant collection exists, if not, create it
        collections = self.qdrant_client.get_collections().collections
        if not any(c.name == "text_embeddings" for c in collections):
            self.qdrant_client.create_collection(
                collection_name="text_embeddings",
                vectors_config=VectorParams(size=384, distance="Cosine")
            )
        else:
            # If collection exists, clear it
            self.qdrant_client.delete_collection(collection_name="text_embeddings")
            self.qdrant_client.create_collection(
                collection_name="text_embeddings",
                vectors_config=VectorParams(size=384, distance="Cosine")
            )

    def clear_pg_table(self):
        # Clear the PostgreSQL table before inserting new chunks
        self.pg_cursor.execute("TRUNCATE TABLE text_chunks;")
        self.pg_conn.commit()

    def store_chunks(self, chunks, url, batch_size=32):
        # Clear existing data
        self.clear_pg_table()

        # Generate embeddings for the chunks
        embeddings = embed_chunks(chunks)

        # Batch insert into PostgreSQL
        try:
            chunk_data = [(i, chunk, url) for i, chunk in enumerate(chunks)]
            self.pg_cursor.executemany(
                "INSERT INTO text_chunks (chunk_number, chunk_text, source_url) VALUES (%s, %s, %s);", 
                chunk_data
            )
            self.pg_conn.commit()
        except Exception as e:
            print(f"Error inserting into PostgreSQL: {e}")
            self.pg_conn.rollback()

        # Batch upsert into Qdrant
        try:
            points = [
                PointStruct(
                    id=i, 
                    vector=embeddings[i].tolist(), 
                    payload={"chunk_number": i, "source_url": url}
                ) for i in range(len(embeddings))
            ]
            for i in range(0, len(points), batch_size):
                batch_points = points[i:i + batch_size]
                self.qdrant_client.upsert(collection_name="text_embeddings", points=batch_points)
        except Exception as e:
            print(f"Error inserting into Qdrant: {e}")

    def retrieve_chunk_from_embedding(self, query_embedding):
        search_result = self.qdrant_client.search(
            collection_name="text_embeddings",
            query_vector=query_embedding.tolist(),
            limit=3
        )

        chunk_number = search_result[0].payload["chunk_number"]
        source_url = search_result[0].payload["source_url"]

        self.pg_cursor.execute("SELECT chunk_text FROM text_chunks WHERE chunk_number = %s AND source_url = %s", (chunk_number, source_url))
        result = self.pg_cursor.fetchone()

        return result[0] if result else None

    def close(self):
        self.pg_cursor.close()
        self.pg_conn.close()

def embed_chunks(chunks, batch_size=32):
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = model.encode(batch_chunks, convert_to_tensor=False)
        embeddings.extend(batch_embeddings)
    return embeddings

# Configuration
pg_config = {
    'dbname': 'yourdbname',
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}

# Initialize StorageManager
storage_manager = StorageManager(pg_config=pg_config)

def process_and_store_chunks(chunks, url):

    storage_manager.store_chunks(chunks, url)
    print(f"Processed and stored {len(chunks)} chunks from {url}")

def retrieve_similar_chunk(query_text):
    query_embedding = model.encode([query_text])[0]
    return storage_manager.retrieve_chunk_from_embedding(query_embedding)
