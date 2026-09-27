import sys
import argparse
import secrets
import time
from pathlib import Path
import numpy as np



#help from claude to create this 
sys.path.append(str(Path(__file__).parent / "src")) #include since main.py exists outside of src folder 

from datagen import generate_data
from dataproc import make_count_arrays
from datavis import update_visualizations

#add Argument Parser to allow for user to pick the games and seeds 
def parse_args():
    parser = argparse.ArgumentParser(description="Generate, score, and visualize new decks for the card game.")
    parser.add_argument(
        "--games", type=int, default=100,
        help="Number of new decks to generate and score (default: 100)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for deck generation. Default: a fresh random seed each run, so you get genuinely new decks each time you run this."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    seed = args.seed if args.seed is not None else secrets.randbits(32) #random seed by default so each run generates new decks, not the same ones every time

    game_history = generate_data(seed=seed, trials=args.games) #generate the new decks (raw decks are not saved -- see datagen.py)
    win_tricks, tie_tricks, win_cards, tie_cards, n_games = make_count_arrays(game_history) #score them and get win/tie counts

    #save only the scored counts (not the raw decks, not the full per-game dataframe) with a unique filename
    output_dir = Path('./data')
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    np.savez_compressed(
        output_dir / f"{seed}_{n_games}_{timestamp}_scored.npz",
        win_tricks=win_tricks,
        tie_tricks=tie_tricks,
        win_cards=win_cards,
        tie_cards=tie_cards,
        n_games=n_games,
    )
    print(f"Scored {n_games} new decks (seed={seed}) and saved results to {output_dir}/")

    #rebuild the heatmaps using every scored file on disk (this run plus all past runs)
    update_visualizations()


if __name__ == "__main__":
    main()
