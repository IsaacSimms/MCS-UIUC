import os
import json
from tqdm import tqdm
from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader as IndexReader
import numpy as np
import matplotlib.pyplot as plt
import subprocess


def preprocess_corpus(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r') as f:
        for i, line in enumerate(tqdm(f, desc="Preprocessing corpus")):
            doc = {
                "id": f"{i}",  # Changed to match qrels format
                "contents": line.strip()
            }
            with open(os.path.join(output_dir, f"doc{i}.json"), 'w') as out:
                json.dump(doc, out)


def build_index(input_dir, index_dir):
    if os.path.exists(index_dir) and os.listdir(index_dir):
        print(f"Index already exists at {index_dir}. Skipping index building.")
        return

    cmd = [
        "python", "-m", "pyserini.index.lucene",
        "--collection", "JsonCollection",
        "--input", input_dir,
        "--index", index_dir,
        "--generator", "DefaultLuceneDocumentGenerator",
        "--threads", "1",
        "--storePositions", "--storeDocvectors", "--storeRaw"
    ]
    subprocess.run(cmd, check=True)


def load_queries(query_file):
    with open(query_file, 'r') as f:
        return [line.strip() for line in f]


def load_qrels(qrels_file):
    qrels = {}
    with open(qrels_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                qid, docid, rel = parts
            else:
                raise Exception(f"incorrect line: {line.strip()}")

            if qid not in qrels:
                qrels[qid] = {}
            qrels[qid][docid] = int(rel)
    return qrels


def search(searcher, queries, top_k=10, query_id_start=0):
    results = {}
    for i, query in enumerate(tqdm(queries, desc="Searching")):
        hits = searcher.search(query, k=top_k)
        results[str(i + query_id_start)] = [(hit.docid, hit.score) for hit in hits]
    return results


def compute_ndcg(results, qrels, k=10):
    def dcg(relevances):
        # return sum((2 ** rel - 1) / np.log2(i + 2) for i, rel in enumerate(relevances[:k]))
        dcg_simple = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevances[:k]))
        return dcg_simple

    ndcg_scores = []
    for qid, query_results in results.items():
        if qid not in qrels:
            # print(f"Query {qid} not found in qrels")
            continue
        relevances_current = [qrels[qid].get(docid, 0) for docid, _ in query_results]
        idcg = dcg(sorted(qrels[qid].values(), reverse=True))
        if idcg == 0:
            print(f"IDCG is 0 for query {qid}")
            continue
        ndcg_scores.append(dcg(relevances_current) / idcg)

    if not ndcg_scores:
        print("No valid NDCG scores computed")
        return 0.0
    return np.mean(ndcg_scores)

## == calculates the Precision@10 == ##
def compute_precision_at_k(results, qrels, k=10, threshold=0):
    """Fraction of the top-k hits whose relevance is greater than threshold.

    Documents missing from the qrels are treated as relevance 0. With
    threshold 0, every judged Cranfield grade (1-4) counts as relevant.
    """
    scores = []
    for qid, query_results in results.items():
        if qid not in qrels:
            continue
        hits = query_results[:k]
        relevant = sum(1 for docid, _ in hits if qrels[qid].get(docid, 0) > threshold)
        scores.append(relevant / k)

    if not scores:
        print("No valid Precision scores computed")
        return 0.0
    return float(np.mean(scores))


def sweep_b(searcher, queries, qrels, query_id_start, k1=0.9, top_k=10, precision_threshold=0):
    """Search once per b in [0, 1] and record nDCG@k and Precision@k."""
    rows = []
    for step in range(11):
        b = round(step * 0.1, 1)
        searcher.set_bm25(k1=k1, b=b)
        results = search(searcher, queries, top_k=top_k, query_id_start=query_id_start)
        row = {
            "b": b,
            "ndcg@10": float(compute_ndcg(results, qrels, k=top_k)),
            "precision@10": compute_precision_at_k(
                results, qrels, k=top_k, threshold=precision_threshold
            ),
        }
        print(f"b={b:.1f}  nDCG@10={row['ndcg@10']:.4f}  P@10={row['precision@10']:.4f}")
        rows.append(row)
    return rows


def plot_b_sweep(rows, output_path, k1):
    plt.figure()
    plt.plot([row["b"] for row in rows], [row["ndcg@10"] for row in rows], marker="o", label="nDCG@10")
    plt.plot(
        [row["b"] for row in rows],
        [row["precision@10"] for row in rows],
        marker="o",
        label="Precision@10",
    )
    plt.xlabel(f"b (k1 fixed at {k1})")
    plt.ylabel("score")
    plt.title("Cranfield BM25: nDCG@10 and Precision@10 vs b")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def sweep_k(searcher, queries, qrels, query_id_start, b=0.4, top_k=10, precision_threshold=0):
    """Search once per k1 and record nDCG@k and Precision@k. b stays fixed."""
    k1_values = [0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0, 2.5, 3.0]
    rows = []
    for k1 in k1_values:
        searcher.set_bm25(k1=k1, b=b)
        results = search(searcher, queries, top_k=top_k, query_id_start=query_id_start)
        row = {
            "k1": k1,
            "ndcg@10": float(compute_ndcg(results, qrels, k=top_k)),
            "precision@10": compute_precision_at_k(
                results, qrels, k=top_k, threshold=precision_threshold
            ),
        }
        print(f"k1={k1:.1f}  nDCG@10={row['ndcg@10']:.4f}  P@10={row['precision@10']:.4f}")
        rows.append(row)
    return rows


def plot_k_sweep(rows, output_path, b):
    plt.figure()
    plt.plot([row["k1"] for row in rows], [row["ndcg@10"] for row in rows], marker="o", label="nDCG@10")
    plt.plot(
        [row["k1"] for row in rows],
        [row["precision@10"] for row in rows],
        marker="o",
        label="Precision@10",
    )
    plt.xlabel(f"k1 (b fixed at {b})")
    plt.ylabel("score")
    plt.title("Cranfield BM25: nDCG@10 and Precision@10 vs k1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


## == Driver code == ##
def main():
    """main function for searching"""

    """=======TODO: Choose Dataset======="""
    # You can choose from "cranfield", "apnews", and "new_faculty" for dataset
    cname = "apnews"
    """============================"""

    base_dir = f"data/{cname}"
    query_id_start = {
        "apnews": 0,
        "cranfield": 1,
        "new_faculty": 1,
    }[cname]

    # Paths to the raw corpus, queries, and relevance label files
    corpus_file = os.path.join(base_dir, f"{cname}.dat")
    query_file = os.path.join(base_dir, f"{cname}-queries.txt")
    qrels_file = os.path.join(base_dir, f"{cname}-qrels.txt")
    # processed_corpus_dir = os.path.join(base_dir, "corpus")

    # Directories where the processed corpus and index will be stored for toolkit
    processed_corpus_dir = f"processed_corpus/{cname}"
    os.makedirs(processed_corpus_dir, exist_ok=True)
    index_dir = f"indexes/{cname}"

    # Preprocess corpus
    if not os.path.exists(processed_corpus_dir) or not os.listdir(processed_corpus_dir):
        preprocess_corpus(corpus_file, processed_corpus_dir)
    else:
        print(f"Preprocessed corpus already exists at {processed_corpus_dir}. Skipping preprocessing.")

    # Build index
    build_index(processed_corpus_dir, index_dir)

    # Load queries and qrels
    queries = load_queries(query_file)
    qrels = load_qrels(qrels_file)

    # Debug info
    print(f"Number of queries: {len(queries)}")
    print(f"Number of qrels: {len(qrels)}")
    print(f"Sample qrel: {list(qrels.items())[0] if qrels else 'No qrels'}")

    # Search once per b. b changes, k1 is a constant
    searcher = LuceneSearcher(index_dir)
    k1 = 0.9
    precision_threshold = 0
    rows = sweep_b(
        searcher,
        queries,
        qrels,
        query_id_start,
        k1=k1,
        precision_threshold=precision_threshold,
    )

    # define selection
    sweep = {
        "dataset": cname,
        "k1": k1,
        "precision_threshold": precision_threshold,
        "rows": rows,
    }
    scores_path = f"bm25_b_sweep_{cname}.json"
    plot_path = f"bm25_b_sweep_{cname}.png"
    with open(scores_path, "w") as f:
        json.dump(sweep, f, indent=2)
    plot_b_sweep(rows, plot_path, k1)
    print(f"Wrote {scores_path} and {plot_path}")

    # Search once per k1. k1 changes, b stays at the Pyserini default.
    b = 0.4
    k_rows = sweep_k(
        searcher,
        queries,
        qrels,
        query_id_start,
        b=b,
        precision_threshold=precision_threshold,
    )
    k_sweep = {
        "dataset": cname,
        "b": b,
        "precision_threshold": precision_threshold,
        "rows": k_rows,
    }
    k_scores_path = f"bm25_k_sweep_{cname}.json"
    k_plot_path = f"bm25_k_sweep_{cname}.png"
    with open(k_scores_path, "w") as f:
        json.dump(k_sweep, f, indent=2)
    plot_k_sweep(k_rows, k_plot_path, b)
    print(f"Wrote {k_scores_path} and {k_plot_path}")


if __name__ == "__main__":
    main()
