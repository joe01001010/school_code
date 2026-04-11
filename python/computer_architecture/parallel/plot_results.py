import pandas as pd
import matplotlib.pyplot as plt

# load CPU files
cpu_files = [
    "./results/cpu_results_threads_1.csv",
    "./results/cpu_results_threads_2.csv",
    "./results/cpu_results_threads_4.csv",
    "./results/cpu_results_threads_8.csv",
    "./results/cpu_results_threads_16.csv"
]

cpu_data = []

for file in cpu_files:
    df = pd.read_csv(file)
    df = df[df["median"].notna()]
    cpu_data.append(df)

cpu_df = pd.concat(cpu_data)

# load GPU
gpu_df = pd.read_csv("./results/gpu_results.csv")
gpu_df = gpu_df[gpu_df["median"].notna()]

# plot CPU scaling
plt.figure()
for t in cpu_df["threads"].unique():
    subset = cpu_df[cpu_df["threads"] == t]
    plt.plot(subset["elements"], subset["median"], label=f"{t} threads")

plt.xlabel("Elements")
plt.ylabel("Time (s)")
plt.title("CPU Scaling")
plt.legend()
plt.grid()
plt.show()

# plot CPU vs GPU
plt.figure()

cpu_best = cpu_df[cpu_df["threads"] == cpu_df["threads"].max()]
plt.plot(cpu_best["elements"], cpu_best["median"], label="CPU (max threads)")

plt.plot(gpu_df["elements"], gpu_df["median"], label="GPU")

plt.xlabel("Elements")
plt.ylabel("Time (s)")
plt.title("CPU vs GPU")
plt.legend()
plt.grid()
plt.yscale("log")  # recommended
plt.show()
