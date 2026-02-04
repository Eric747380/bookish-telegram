# convert_yeast_to_gaston.py

INPUT = "yeast.txt_graph"
OUTPUT = "yeast_gaston.dat"

label_map = {}
next_label = 0

def get_label_id(label):
    global next_label
    if label not in label_map:
        label_map[label] = next_label
        next_label += 1
    return label_map[label]

with open(INPUT) as fin, open(OUTPUT, "w") as fout:
    lines = [l.strip() for l in fin if l.strip()]
    i = 0

    fout.write("# Yeast dataset converted for Gaston\n")

    while i < len(lines):
        if lines[i].startswith("#"):
            graph_id = lines[i][1:]
            fout.write(f"t # {graph_id}\n")
            i += 1

            n = int(lines[i])
            i += 1

            # vertices
            for v in range(n):
                label = lines[i]
                lid = get_label_id(label)
                fout.write(f"v {v} {lid}\n")
                i += 1

            m = int(lines[i])
            i += 1

            # edges
            for _ in range(m):
                u, v, elabel = lines[i].split()
                fout.write(f"e {u} {v} {elabel}\n")
                i += 1

