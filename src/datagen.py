import numpy as np
import pandas as pd
from pathlib import Path
import time 



# this will go into datagen.py
def generate_data(seed:int, trials:int, save:bool=False) -> np.ndarray:
    ''' 
    Generates decks of shuffled cards according to specified number of trials and seed.
    '''
    game_history = [] #initialize a list to store the shuffled decks
    base_cards = [0] * 26 + [1] * 26  #base cards to shuffle 
    rng = np.random.default_rng(seed) #initialize random number generator
    for num in range(trials): #for loop to generate specified number of shuffled decks
        game = rng.permutation(base_cards) #shuffle the base cards
        packed_game = np.packbits(game) #bitpacking 
        game_history.append(packed_game) #return packed game history 
    if save: #only save raw decks if explicitly requested
        timestamp = time.strftime("%Y%m%d_%H%M%S")  #get timestamp 
        output_dir = Path('./data')
        output_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(output_dir /f"{seed}_{trials}_{timestamp}_datagen.npz", decks = np.array(game_history), seed = seed, trials = trials) #got help from https://www.skytowner.com/explore/numpy_savez_compressed_method and claude 
    return game_history 


# if __name__ == "__main__":
#     generate_data(seed=42, trials=10)
