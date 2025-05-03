from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_sequences(sequences: dict[str, np.array]):
    counting = Counter(start=0, step=1)
    plt.figure(figsize=(8, 4))
    for sequence in sequences:
        sequences[sequence] = sequences[sequence].mean(axis=0)
        plt.plot(
            sequences[sequence],
            label=sequence,
            color=f"C{
                next(counting)}")

    plt.xlabel("Time steps")
    plt.ylabel("Sequence occurence average")
    plt.title("Sequences across steps")
    plt.legend()
    plt.savefig("figures/sequences_simple_goal.png")
    plt.close()


def simple_snsplot(df, x_label, y_label, filename, line=False, color="red"):
    sns.scatterplot(df, x=x_label, y=y_label)
    if line:
        sns.lineplot(df, x=x_label, y=y_label, color=color)
    plt.savefig(filename)
    plt.close()


def simple_plotting(data, x_label, y_label, filename, figno):
    # plot the current bit:
    plt.figure()
    plt.plot(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(filename)
    plt.close()
    plt.figure(figno)
