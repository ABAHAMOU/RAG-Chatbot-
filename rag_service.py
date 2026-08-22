## "fastapi dev main.py" to launch the server

import ollama

from processor import collection


def generer_reponse(question, history=None):
    history = history or []

    # Recherche des chunks pertinents dans ChromaDB
    
    resultats = collection.query(query_texts=[question], n_results=10)
    chunks = resultats['documents'][0]
    metadonnees = resultats['metadatas'][0]

    texte = "\n\n".join(chunks)
    sources = {(m["source"], m["page"]) for m in metadonnees}
    print(f"[debug] chunks utilisés : {sources}")

    system_prompt = (
        "Tu es l'assistant virtuel de SRM Agadir. Réponds à la question "
        "en te basant uniquement sur les informations ci-dessous, mais "
        "réponds directement et naturellement, comme si tu connaissais "
        "l'information toi-même.\n\n"
        "INTERDIT : ne fais JAMAIS référence à la source de l'information. "
        "N'utilise jamais des expressions comme \"d'après le texte\", "
        "\"selon le document\", \"le contexte indique que\", \"dans le "
        "texte fourni\", \"les informations fournies\", \"d'après les "
        "documents disponibles\", \"selon les données disponibles\" ou "
        "toute variante similaire — que ce soit pour donner une réponse "
        "ou pour dire que tu ne sais pas.\n\n"
        "Si l'information demandée n'est pas disponible ci-dessous, "
        "réponds exactement sur ce modèle, sans mentionner de texte ni "
        "de document : \"Je ne dispose pas de cette information. Je vous "
        "invite à contacter le service client SRM Agadir.\"\n\n"
        f"Informations disponibles :\n{texte}"
    )

    messages = [{"role": "system", "content": system_prompt}]
  
    messages += history[-6:]
    messages.append({"role": "user", "content": question})

    response = ollama.chat(
        model="llama3.1:8b",
        messages=messages
    )

    return response['message']['content']