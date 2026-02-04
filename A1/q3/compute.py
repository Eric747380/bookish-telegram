import sys

def read_candidates(path):
    """
    Reads mutagenicity_candidates.dat
    Returns: dict {query_id (1-based): set(graph_ids)}
    """
    C = {}
    current_q = None

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("q #"):
                current_q = int(line.split("#")[1])
                C[current_q] = set()

            elif line.startswith("c #"):
                parts = line.split()
                for x in parts[2:]:
                    C[current_q].add(int(x))

    return C


def read_truth(path):
    """
    Reads muta_truth.dat
    Format:
      0: 4,8,15,...
      1: 10,20,...
    Returns: dict {query_id (1-based): set(graph_ids)}
    """
    R = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            idx, rest = line.split(":")
            qid = int(idx) + 1  # convert 0-based to 1-based

            if rest.strip() == "":
                R[qid] = set()
            else:
                R[qid] = set(map(int, rest.split(",")))

    return R


def main():
    cand_path = sys.argv[1]
    truth_path = sys.argv[2]

    C = read_candidates(cand_path)
    R = read_truth(truth_path)

    common_queries = sorted(set(C.keys()) & set(R.keys()))

    print(f"Found {len(common_queries)} queries")

    scores = []

    print("\nPer-query scores:")
    for q in common_queries:
        Cq = C[q]
        Rq = R[q]

        if len(Cq) == 0:
            sq = 0.0
        else:
            sq = len(Rq) / len(Cq)

        scores.append(sq)

        # Safety check
        if not Rq.issubset(Cq):
            print(f"⚠️  WARNING: Query {q} lost true matches!")

        print(
            f"Query {q:02d}: |Rq|={len(Rq):4d}, "
            f"|Cq|={len(Cq):4d}, s_q={sq:.6f}"
        )

    avg_score = sum(scores) / len(scores)

    print("\n==============================")
    print(f"Average s_q over queries: {avg_score:.6f}")
    print("==============================")


if __name__ == "__main__":
    main()