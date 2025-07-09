from itertools import count
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# def plot_sequences(
#         sequences: dict[str, np.array],
#         path="data/figures/sequences_simple_goal.png"):
#     counting = count(start=0, step=1)
#     plt.figure(figsize=(8, 4))
#     for sequence in sequences:
#         sequences[sequence] = sequences[sequence].mean(axis=0)
#         plt.plot(
#             sequences[sequence],
#             label=sequence,
#             color=f"C{
#                 next(counting)}")

#     plt.xlabel("Time steps")
#     plt.ylabel("Sequence occurence average")
#     plt.title("Sequences across steps")
#     plt.legend()
#     plt.savefig(path)
#     plt.close()

def plot_sequences(
    sequences: dict[str, np.array],
    path="data/figures/sequences_simple_goal.png",
    max_legend_items=15,  # Limit number of legend items
    legend_outside=True,  # Place legend outside plot area
    use_extended_colors=True  # Use extended color palette
):
    plt.figure(figsize=(10, 4) if legend_outside else (8, 4))
    
    # Extended color palette to avoid repetition
    if use_extended_colors:
        # Combine default colors with additional distinct colors
        colors = plt.cm.tab20.colors + plt.cm.Set3.colors  # 32 distinct colors
    else:
        colors = [f"C{i}" for i in range(10)]  # Default matplotlib colors
    
    sequence_names = list(sequences.keys())
    
    # Plot sequences
    for i, sequence in enumerate(sequence_names):
        sequences[sequence] = sequences[sequence].mean(axis=0)
        color = colors[i % len(colors)]
        plt.plot(
            sequences[sequence],
            label=sequence,
            color=color
        )
    
    plt.xlabel("Time steps")
    plt.ylabel("Sequence occurrence average")
    plt.title("Sequences across steps")
    
    # Handle legend based on number of sequences
    num_sequences = len(sequence_names)
    
    if num_sequences <= max_legend_items:
        if legend_outside:
            # Place legend outside the plot area
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
        else:
            # Smart legend positioning to avoid data overlap
            plt.legend(loc='best')
    else:
        # Too many sequences - either skip legend or show limited items
        print(f"Warning: {num_sequences} sequences detected. Legend skipped to avoid crowding.")
        print("Consider filtering sequences or using legend_outside=True with fewer sequences.")
        # Optionally, you could show only the first N sequences in legend:
        # handles, labels = plt.gca().get_legend_handles_labels()
        # plt.legend(handles[:max_legend_items], labels[:max_legend_items], 
        #           title=f"Showing {max_legend_items} of {num_sequences} sequences")
    
    plt.savefig(path, bbox_inches='tight' if legend_outside else None, dpi=300)
    plt.close()


def simple_snsplot(df, x_label, y_label, filename, line=False, color="red", figno=None):
    plt.figure()
    sns.scatterplot(df, x=x_label, y=y_label)
    if line:
        sns.lineplot(df, x=x_label, y=y_label, color=color)
    plt.savefig(filename)
    plt.close()
    if figno:
        plt.figure(figno)


def simple_plotting(data, x_label, y_label, filename, figno=None):
    # plot the current bit:
    plt.figure()
    plt.plot(data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(filename)
    plt.close()
    if figno:
        plt.figure(figno)

def plot_rl_stats(window, vals, filename, figno=None):
    cumul_vals = []
    for i in range(0, len(vals)-window):
        cumul_vals.append(sum(vals[i:i + window])/window)
    plt.figure()
    plt.plot(cumul_vals)
    plt.savefig(filename)
    plt.close()
    if figno:
        plt.figure(figno)