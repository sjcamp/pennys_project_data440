import numpy as np
import pandas as pd

#this will go into datagen.py
#still need to figue out how to store the data in data folder
def generate_data(seed,trials):
    ''' 
    Generates decks of shuffled cards according to specified number of trials and seed
    '''
    game_history = [] #initialize a list to store the shuffled decks
    base_cards = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #base cards to shuffle
    rng = np.random.default_rng(seed) #initialize random number generator
    for num in range(trials): #for loop to generate specified number of shuffled decks
        game = rng.permutation(base_cards) #shuffle the base cards
        game_history.append(game) #add deck to game_history
    return game_history