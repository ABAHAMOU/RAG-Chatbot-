# Chatbot-a-Rag-approach-

Un chatbot RAG (Retrieval-Augmented Generation) capable de répondre à des questions à partir de documents internes, développé dans le cadre d'un stage à SRM Agadir.

## Prérequis

- Python 3.12
- [Ollama](https://ollama.com/download) installé, avec le modèle `llama3.1:8b` téléchargé :
  ```bash
  ollama pull llama3.1:8b
  ```

## Installation

```bash
pip install -r requirements.txt
```
## Indexation des documents

Avant de lancer l'API, placez vos PDF dans le dossier du projet et lancez l'indexation :

```bash
python processor.py
## Lancement

Le projet nécessite **deux processus actifs en parallèle**, dans deux terminaux séparés :

**Terminal 1 — Serveur Ollama (LLM local)**
```bash
ollama serve
```

**Terminal 2 — Serveur FastAPI**
```bash
uvicorn main:app --reload
```

Le serveur est ensuite disponible sur `http://localhost:8000`, avec l'endpoint principal `POST /chat`.

## Structure du projet

- `chunking.py` — extraction et découpage des PDF en chunks
- `processor.py` — indexation des chunks dans ChromaDB (collection `srm_faq`)
- `rag_service.py` — recherche des chunks pertinents et génération de la réponse via Ollama
- `main.py` — API FastAPI, endpoint `POST /chat`
- `srm-chat-widget.html` — widget de chat intégrable sur le site
