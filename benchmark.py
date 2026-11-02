import csv
import random
import time

COUNTS = [20_000, 80_000, 320_000]
METHODS = ["sorted", "reversed", "random"]


class Item:
    def __init__(self, value, counter):
        self.value = value
        self.counter = counter

    def __lt__(self, other):
        self.counter[0] += 1
        return self.value < other.value


def values_for(method, count):
    numbers = list(range(count))
    if method == "reversed":
        numbers.reverse()
    elif method == "random":
        random.shuffle(numbers)
    return numbers


def sort_items(values):
    counter = [0]
    items = [Item(value, counter) for value in values]
    items.sort()
    return counter[0]


def repeats_for(count):
    if count <= 20_000:
        return 5
    if count <= 80_000:
        return 2
    return 1


def main():
    rows = []
    for count in COUNTS:
        repeats = repeats_for(count)
        prepared = {method: values_for(method, count) for method in METHODS}
        for method in METHODS:
            values = prepared[method]
            started = time.perf_counter()
            comparisons = 0
            for _ in range(repeats):
                comparisons = sort_items(values)
            seconds = (time.perf_counter() - started) / repeats
            rows.append([
                method,
                count,
                repeats,
                round(seconds, 6),
                comparisons,
                round(count / seconds, 1),
            ])

    with open("benchmark_results.csv", "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["method", "count", "repeats", "seconds", "comparisons", "items_per_second"])
        writer.writerows(rows)

    print(len(rows), "measurements written")


if __name__ == "__main__":
    main()
