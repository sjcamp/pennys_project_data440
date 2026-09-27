import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

#same tick labels as Prof Smith 
x_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
y_tick_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']


def load_all_scored_data(data_dir=Path('./data')):
    '''
    Reads every previously-saved scored-results file (*_scored.npz) in data_dir and
    sums their count arrays together, so all games ever scored -- past runs plus the
    current one -- count toward the totals.
    '''
    win_tricks_total = np.zeros((8, 8), dtype=int)
    tie_tricks_total = np.zeros((8, 8), dtype=int)
    win_cards_total = np.zeros((8, 8), dtype=int)
    tie_cards_total = np.zeros((8, 8), dtype=int)
    n_games_total = 0

    data_dir = Path(data_dir)
    scored_files = sorted(data_dir.glob("*_scored.npz"))
    for file in scored_files:
        with np.load(file) as npz:
            win_tricks_total += npz['win_tricks']
            tie_tricks_total += npz['tie_tricks']
            win_cards_total += npz['win_cards']
            tie_cards_total += npz['tie_cards']
            n_games_total += int(npz['n_games'])

    return win_tricks_total, tie_tricks_total, win_cards_total, tie_cards_total, n_games_total


def counts_to_pct(count_array, n_games_total):
    '''
    Converts a combined count array into a percentage array using the total number
    of decks scored across all runs.
    '''
    if n_games_total == 0:
        return np.zeros((8, 8))
    return (count_array / n_games_total) * 100


def plot_heatmap(win_data, tie_data, title, output_path):
    '''
    Draws heatmap
    '''
    fig, ax = plt.subplots()
    cmap = plt.get_cmap("Blues")
    ax.imshow(win_data, cmap=cmap, vmin=0, vmax=100)
    n_rows, n_cols = win_data.shape

    #sets grid lines and ticks
    ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
    ax.set_xticks(range(len(x_tick_labels)), labels=x_tick_labels)
    ax.set_yticks(range(len(y_tick_labels)), labels=y_tick_labels)

    ax.grid(which='minor', color='steelblue', linestyle='-', linewidth=1.5)
    ax.tick_params(which='minor', bottom=False, left=False)
    ax.set_xticks(np.arange(n_cols))
    ax.set_yticks(np.arange(n_rows))

    #label each cell with "win (tie)", picking text color by that cell's actual
    #rendered luminance so it reads clearly whether the cell is light or dark
    for i in range(n_rows):
        for j in range(n_cols):
            win_val = win_data[i][j]
            tie_val = tie_data[i][j]
            r, g, b, _ = cmap(win_val / 100)
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            text_color = "white" if luminance < 0.5 else "black"
            ax.text(
                j, i, f"{round(win_val)} ({round(tie_val)})",
                ha="center", va="center", color=text_color, fontsize=9
            )

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("My Choice", fontsize=12)
    ax.set_ylabel("Opponent Choice", fontsize=12)

    fig.savefig(output_path)
    plt.close(fig)


def update_visualizations(data_dir=Path('./data'), figures_dir=Path('./figures')):
    '''
    Reads all scored data currently in data_dir, combines it into one running total,
    and creates/overwrites the two heatmaps (cards_viz.png, tricks_viz.png) in
    figures_dir using the win-probability percentages. The sample size (total number
    of decks behind the percentages) is shown in each title.
    '''
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    win_tricks_total, tie_tricks_total, win_cards_total, tie_cards_total, n_games_total = load_all_scored_data(data_dir)

    if n_games_total == 0:
        print("No scored data found in the data folder yet -- run main.py first to generate some.")
        return

    win_cards_pct = counts_to_pct(win_cards_total, n_games_total)
    tie_cards_pct = counts_to_pct(tie_cards_total, n_games_total)
    win_tricks_pct = counts_to_pct(win_tricks_total, n_games_total)
    tie_tricks_pct = counts_to_pct(tie_tricks_total, n_games_total)

    plot_heatmap(win_cards_pct, tie_cards_pct, f"Score by Cards (n = {n_games_total} decks)", figures_dir / "cards_viz.png")
    plot_heatmap(win_tricks_pct, tie_tricks_pct, f"Score by Tricks (n = {n_games_total} decks)", figures_dir / "tricks_viz.png")

    print(f"Updated heatmaps using {n_games_total} total scored decks.")


if __name__ == "__main__":
    update_visualizations()
