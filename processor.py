from pathlib import Path
import chromadb
from chunking import extraire_et_chunker

from chromadb.utils import embedding_functions

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)


# Connexion à la base de données :

client = chromadb.PersistentClient(path="./srm_db")

try:
    client.delete_collection(name="srm_faq")
except Exception:
    pass 
collection = client.get_or_create_collection(name="srm_faq",embedding_function=embedding_fn)

# Traitement de tous les PDFs
dossier = "library"

for pdf in Path(dossier).glob("*.pdf"):
    if chunks := extraire_et_chunker(str(pdf)):
        collection.add(
            ids=[f"{pdf.stem}_{i}" for i in range(len(chunks))],
            documents=[c["text"] for c in chunks],
            metadatas=[{"page": c["page"], "source": c["source"]} for c in chunks]
        )
        print(f"{pdf.name} : {len(chunks)} chunks ajoutés")