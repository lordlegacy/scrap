# Web Scraping and RAG System

This project implements a web scraping and Retrieval-Augmented Generation (RAG) system. It can scrape publicly available text from a given URL, store and embed the data, and perform similarity searches on the stored content.

## Features

- Web scraping using Selenium
- Text cleaning and chunking
- Embedding generation using SentenceTransformers
- Vector storage with Qdrant
- Similarity search capabilities

## Setup

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/lordlegacy/scrap.git
   cd scrap
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up and run Qdrant (vector database) using Docker:
   ```
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. Configure the PostgreSQL connection in `database.py`:
   Update the `pg_config` dictionary with your database details:
   ```python
   pg_config = {
       'dbname': 'yourdbname',
       'user': 'user',
       'password': 'password',
       'host': 'localhost',
       'port': 5432
   }
   ```

5. Start the application:
   ```
   python main.py
   ```

## Usage

The application exposes two main routes:

### 1. Scrape and Store Content

To scrape a webpage, send a POST request to the `/scrape` endpoint:

```
POST /scrape
Content-Type: application/json

{
    "url": "https://example.com"
}
```

This will:
- Scrape the content from the provided URL
- Clean and chunk the text
- Generate embeddings for each chunk
- Store the chunks in PostgreSQL
- Store the embeddings in Qdrant

### 2. Find Similar Text

To find text chunks similar to a query, send a POST request to the `/similar` endpoint:

```
POST /similar
Content-Type: application/json

{
    "query": "Your search text here"
}
```

This will:
- Generate an embedding for the query text
- Search for similar embeddings in Qdrant
- Retrieve the corresponding text chunk from PostgreSQL
- Return the most similar text chunk

## Note

This system implements the data storage and retrieval parts of a RAG system. To complete a full RAG implementation, you would need to integrate an LLM to use the retrieved similar chunks as context for generating responses.
