label_map = {}
next_label = 0


input_file = "yeast.txt_graph"
output_file = "yeast.dat"

with open(input_file) as f, open(output_file, "w") as out:
    graph_id = -1
    lines = iter(f.readlines())

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # New graph
        if line.startswith("#"):
            graph_id += 1
            out.write(f"t # {graph_id}\n")

            # Number of vertices
            n = int(next(lines).strip())

            # Read vertices
            for vid in range(n):
                label = next(lines).strip()
                if label not in label_map:
                    label_map[label] = next_label
                    next_label += 1
                out.write(f"v {vid} {label_map[label]}\n")

            # Number of edges
            m = int(next(lines).strip())

            # Read edges
            for _ in range(m):
                u, v, bond = next(lines).split()
                out.write(f"e {u} {v} {bond}\n")

