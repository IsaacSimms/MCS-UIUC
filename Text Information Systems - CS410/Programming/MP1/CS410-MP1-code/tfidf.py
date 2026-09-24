import os

from pyserini.pyclass import autoclass
from pyserini.search.lucene import LuceneSearcher

from main import (
    build_index,
    compute_ndcg,
    compute_precision_at_k,
    load_qrels,
    load_queries,
    preprocess_corpus,
    search,
)


def main():
    """Score the chosen dataset with Lucene ClassicSimilarity (TF-IDF)."""

    # Edit cname to "cranfield", "apnews", or "new_faculty".
    cname = "apnews"
    top_k = 10
    precision_threshold = 0

    query_id_start = {
        "apnews": 0,
        "cranfield": 1,
        "new_faculty": 1,
    }[cname]

    base_dir = f"data/{cname}"
    corpus_file = os.path.join(base_dir, f"{cname}.dat")
    query_file = os.path.join(base_dir, f"{cname}-queries.txt")
    qrels_file = os.path.join(base_dir, f"{cname}-qrels.txt")
    processed_corpus_dir = f"processed_corpus/{cname}"
    index_dir = f"indexes/{cname}"

    os.makedirs(processed_corpus_dir, exist_ok=True)
    if not os.listdir(processed_corpus_dir):
        preprocess_corpus(corpus_file, processed_corpus_dir)
    else:
        print(f"Preprocessed corpus already exists at {processed_corpus_dir}. Skipping preprocessing.")

    build_index(processed_corpus_dir, index_dir)

    queries = load_queries(query_file)
    qrels = load_qrels(qrels_file)
    print(f"Number of queries: {len(queries)}")
    print(f"Number of qrels: {len(qrels)}")

    searcher = LuceneSearcher(index_dir)
    ClassicSimilarity = autoclass("org.apache.lucene.search.similarities.ClassicSimilarity")
    searcher.object.searcher.setSimilarity(ClassicSimilarity())

    results = search(searcher, queries, top_k=top_k, query_id_start=query_id_start)
    ndcg = float(compute_ndcg(results, qrels, k=top_k))
    precision = compute_precision_at_k(
        results, qrels, k=top_k, threshold=precision_threshold
    )
    print(f"dataset={cname}  similarity=tfidf  nDCG@10={ndcg:.4f}  P@10={precision:.4f}")


if __name__ == "__main__":
    main()
