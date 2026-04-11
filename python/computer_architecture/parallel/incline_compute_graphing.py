import numpy as np
import time
import csv
import statistics
import os

def compute_elements(num_elements: int = 1000, ex=np):
    rd = ex.random.RandomState(88)
    a = rd.randint(1, num_elements, (num_elements, num_elements))
    y = rd.randint(1, num_elements, (num_elements))
    res = ex.linalg.solve(a, y)
    return res


if __name__ == '__main__':
    sizes = [10, 50, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]

    threads = os.environ.get("OMP_NUM_THREADS", "unknown")

    with open(f"cpu_results_threads_{threads}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["elements", "threads", "run", "median"])

        for n_elems in sizes:
            runtimes = []

            for run in range(3):
                start_time = time.time()
                res = compute_elements(n_elems)
                end_time = time.time()

                runtime = end_time - start_time
                runtimes.append(runtime)

                writer.writerow([n_elems, threads, runtime, ""])

            median_val = statistics.median(runtimes)

            writer.writerow([n_elems, threads, "", median_val])

            print(f"{n_elems} elements | threads={threads} | median={median_val}")
