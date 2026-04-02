import re
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def sentence_split(text):
    return re.split(r'(?<=[.!?]) +', text)


def semantic_chunk(text, max_sentences=4, similarity_threshold=0.7):
    sentences = sentence_split(text)

    if len(sentences) <= max_sentences:
        return [" ".join(sentences)]

    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(embeddings[i-1], embeddings[i])

        if sim > similarity_threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def cosine_similarity(vec1, vec2):
    return (vec1 @ vec2) / ((vec1 @ vec1) ** 0.5 * (vec2 @ vec2) ** 0.5)


def recursive_chunk(text, max_length=200):
    paragraphs = text.split("\n\n")
    chunks = []

    for p in paragraphs:
        if len(p) <= max_length:
            chunks.append(p)
        else:
            chunks.extend(semantic_chunk(p))

    return chunks


def add_overlap(chunks, overlap=10):
    new_chunks = []

    for i in range(len(chunks)):
        chunk = chunks[i]

        if i > 0:
            chunk = chunks[i-1].split()[-20:] + chunk.split()

        new_chunks.append(" ".join(chunk))

    return new_chunks


def smart_chunk(text):
    chunks = recursive_chunk(text)
    chunks = add_overlap(chunks)
    return chunks