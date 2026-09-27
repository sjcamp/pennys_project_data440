import sys
from pathlib import Path


#help from claude to create this 
sys.path.append(str(Path(__file__).parent / "src")) #include since main.py exists outside of src folder 

from datagen import generate_data
from dataproc import get_results_for_new_games

def main():
    game_history = generate_data(seed=42, trials=10) #generate data
    results_df = get_results_for_new_games(game_history) #get results
    print(results_df.head())

if __name__ == "__main__":
    main()