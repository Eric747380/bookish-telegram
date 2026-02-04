import matplotlib.pyplot as plt
import sys
import os

# Output directory (default: current directory)
out_dir = sys.argv[1] if len(sys.argv) > 1 else "."

# Support thresholds
supports = [5, 10, 25, 50, 95]

# Runtime containers
gspan_times = []
fsg_times = []
gaston_times = []

# Read runtime files
for s in supports:
    for algo, times_list in [
        ("gspan", gspan_times),
        ("fsg", fsg_times),
        ("gaston", gaston_times),
    ]:
        time_file = os.path.join(out_dir, f"{algo}{s}.time")

        try:
            with open(time_file, "r") as f:
                lines = f.readlines()
                content = lines[-1].strip()
                if content:
                    times_list.append(float(content))
                else:
                    raise ValueError
        except (FileNotFoundError, ValueError):
            # Use 1 hour as timeout / failure marker
            times_list.append(3600.0)

# Plot runtimes
plt.plot(supports, gspan_times, "o-", label="gSpan")
plt.plot(supports, fsg_times, "s-", label="FSG")
plt.plot(supports, gaston_times, "^-", label="Gaston")

plt.xlabel("Min Support (%)")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime vs Minimum Support on Yeast Dataset")
plt.legend()
plt.grid(True)

# Save plot
output_path = os.path.join(out_dir, "plot.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()
