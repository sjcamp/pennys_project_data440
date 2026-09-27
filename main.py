import sys
from pathlib import Path
import pandas as pd



#help from claude to create this 
sys.path.append(str(Path(__file__).parent / "src")) #include since main.py exists outside of src folder 

from datagen import generate_data
from dataproc import get_results_for_new_games

def main():
    game_history = generate_data(seed=42, trials=10) #generate data
    results_df = get_results_for_new_games(game_history) #get results
    pd.set_option('display.max_columns', None) # force it to display all the columns
    print(results_df.head(10)) # adjust number in head() to get number of games to display

if __name__ == "__main__":
    main()