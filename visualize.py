import csv
import matplotlib.pyplot as plt

STYLES = {
    "sorted": ("C0", "-"),
    "reversed": ("C1", "--"),
    "random": ("C2", "-"),
}


def load(path="benchmark_results.csv"):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("count", "repeats", "seconds", "comparisons", "items_per_second"):
            row[key] = float(row[key])
    return rows


def draw(axis, rows, ykey):
    for method, (color, style) in STYLES.items():
        chosen = sorted((row for row in rows if row["method"] == method), key=lambda row: row["count"])
        axis.plot(
            [row["count"] for row in chosen],
            [row[ykey] for row in chosen],
            marker="o",
            color=color,
            linestyle=style,
            label=method,
        )
    axis.set_yscale("log")
    axis.set_xlabel("items")
    axis.legend()


def save(figure, path):
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)
    print("saved", path)


def main():
    rows = load()
    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "seconds")
    axis.set_ylabel("seconds (log scale)")
    axis.set_title("Sort time by starting order")
    save(figure, "sort_time.png")

    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "comparisons")
    axis.set_ylabel("comparisons (log scale)")
    axis.set_title("Comparisons by starting order")
    save(figure, "comparison_count.png")

    figure, axis = plt.subplots(figsize=(8, 4.5))
    draw(axis, rows, "items_per_second")
    axis.set_ylabel("items per second (log scale)")
    axis.set_title("Sort throughput as the list grows")
    save(figure, "throughput.png")


if __name__ == "__main__":
    main()
