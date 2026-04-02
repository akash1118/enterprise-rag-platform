from services.retrieval.retrieval import retrieve

def precision_at_k(retrieved_chunks, expected_keywords):
    hits = 0

    for chunk in retrieved_chunks:
        if any(keyword.lower() in chunk.lower() for keyword in expected_keywords):
            hits += 1

    return hits / len(retrieved_chunks)

def recall_at_k(retrieved_chunks, expected_keywords):
    hits = 0

    for keyword in expected_keywords:
        if any(keyword.lower() in chunk.lower() for chunk in retrieved_chunks):
            hits += 1

    return hits / len(expected_keywords)


def evaluate(evaluation_data):
    total_precision = 0
    total_recall = 0

    for sample in evaluation_data:
        chunks = retrieve(sample["question"], top_k=5)

        p = precision_at_k(chunks, sample["expected_keywords"])
        r = recall_at_k(chunks, sample["expected_keywords"])

        print(f"Q: {sample['question']}")
        print(f"Precision@K: {p}")
        print(f"Recall@K: {r}\n")

        total_precision += p
        total_recall += r

    print("Final Precision:", total_precision / len(evaluation_data))
    print("Final Recall:", total_recall / len(evaluation_data))


def evaluate_answer(query, answer):
    prompt = f"""
Evaluate if the answer is correct.

Question: {query}
Answer: {answer}

Score 1-5 and explain.
"""