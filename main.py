# Importing essential libraries!

#FastAPI is the library we use to create the backend for this project
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

#The Google library is what we utilize to use the Gemini API 
from google import genai

#Importing the environment variables using the dotenv, os and re libraries
from dotenv import load_dotenv
import os
import re

#Numpy and faiss to manage the text embeddings we create
import numpy as np
import faiss

load_dotenv()
# Create Gemini client (new API style)
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"api_version": "v1alpha"}
)

#Creating a FastAPI application for our backend
app = FastAPI(title="Gemini RAG Workshop")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX = None
CHUNKS = []

#TEXT CHUNKING
#chunk_text is our function to chunk the text, allowing us to only utilize the chunks that are important for our query
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split text into overlapping chunks for embedding.
    """
    words = re.split(r"\s+", text)
    
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


# EMBEDDING + FAISS FUNCTIONS
def create_embeddings(text_list):
    """
    Create embeddings for each text chunk using Gemini's embedding model (new API format).
    """

    response = client.models.embed_content(
        model="text-embedding-004",
        contents= text_list 
    )

    # The new API returns an object with .embeddings
    if hasattr(response, "embeddings"):
        embeddings = np.array(
            [e.values for e in response.embeddings], dtype="float32"
        )
    elif hasattr(response, "embedding"):
        embeddings = np.array([response.embedding.values], dtype="float32")
    else:
        raise ValueError(f"Unexpected embedding structure: {embeddings}") #TODO: Fill in the question mark
    
    if embeddings.ndim > 2:
        embeddings = embeddings.reshape(embeddings.shape[0], -1)

    return embeddings #TODO: Fill in the question mark

    

def create_faiss_index(embeddings: np.ndarray):
    """
    Create FAISS index from embeddings.
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

    
def retrieve_top_k(index, query_embedding, chunks, k=3):
    """
    Retrieve top-k most similar chunks.
    """
    query_embedding = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]

    
# ENDPOINT: UPLOAD
@app.post("/upload")
async def upload_file(file: UploadFile):
    global INDEX, CHUNKS

    text = (await file.read()).decode("utf-8")
    CHUNKS = chunk_text(text)
    embeddings = create_embeddings(CHUNKS)
    INDEX = create_faiss_index(embeddings)

    return {"message": f"Uploaded and embedded {file.filename}", "num_chunks": len(CHUNKS)}

@app.post("/upload_text")
async def upload_file(text: str = Form(...)):
    global INDEX, CHUNKS


    CHUNKS = chunk_text(text)
    embeddings = create_embeddings(CHUNKS)
    INDEX = create_faiss_index(embeddings)

    return {"message": f"Uploaded and embedded text", "num_chunks": len(CHUNKS)}

    
# ENDPOINT: ASK
@app.post("/ask")
async def ask_question(question: str = Form(...)):
    global INDEX, CHUNKS

    if INDEX is None:
        return {"error": "No document uploaded. Upload a .txt file first."}

    # Embed the user's question
    q_embed = create_embeddings([question])[0]
    top_chunks = retrieve_top_k(INDEX, q_embed, CHUNKS, k=3)

    # Build the prompt with retrieved context
    context = "\n\n".join(top_chunks)
    prompt = f"""
You are a helpful AI assistant. Use the following context to answer the user's question clearly and completely.

Context:
{context}

Question: {question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    #Extract the answer text
    answer = None
    try:
        if hasattr(response, "candidates") and response.candidates:
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], "text"):
                answer = parts[0].text
    except Exception as e:
        answer = f"(Error extracting text: {e})"

    # Return both the answer and the retrieved context
    #TODO:Fill in the question marks below
    return {
        "answer": answer,
        "context_used": context
    }


@app.get("/")
async def serve_index():
    return FileResponse("index.html")
