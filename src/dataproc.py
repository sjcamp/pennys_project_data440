
import numpy as np
import pandas as pd

#these will go into dataproc.py
def game_to_string(packed_game):
    '''
    Turns an array from game_history into a string for pattern matching
    '''
    unpacked_game = np.unpackbits(packed_game)
    game_str = "".join(str(card)for card in unpacked_game[:52]) 
    return game_str

def find_pattern(game_str, pattern, starting_indx = 0):
    ''' 
    Identifies the index of the first time a pattern is found within a game string
    '''
    pattern_indx = game_str.find(pattern, starting_indx)
    return pattern_indx

def compare_patterns(game_str, pattern1, pattern2, starting_indx = 0):
    ''' 
    Compares two patterns to see which one appears first within a game string. Returns the winning pattern and its index
    '''
    pattern1_indx = find_pattern(game_str, pattern1, starting_indx) #find index of first pattern
    pattern2_indx = find_pattern(game_str, pattern2, starting_indx) #find index of second pattern

    if 0 <= pattern1_indx: #if pattern 1 is found (not index -1):
        if pattern1_indx < pattern2_indx or pattern2_indx == -1: #if pattern 2 is larger than pattern 1 or pattern 2 is not found then pattern 1 wins
            winning_pattern = pattern1 #pattern 1 wins
            winning_indx =  pattern1_indx #store winning index
        elif 0 <= pattern2_indx < pattern1_indx: #if pattern 2 is found and smaller than pattern 1, pattern 2 wins
            winning_pattern = pattern2 #pattern 2 wins
            winning_indx =  pattern2_indx #store winning index
    elif pattern1_indx == -1: #if pattern 1 is not found:
        if 0 <= pattern2_indx: #if pattern 2 is found, pattern 2 wins
            winning_pattern = pattern2 #pattern 2 wins
            winning_indx = pattern2_indx #store winning index
        elif pattern2_indx == -1: #if pattern 2 is not found, neither wins
            winning_pattern = None
            winning_indx = None
    return winning_pattern, winning_indx

def score_game(game_str,pattern1,pattern2):
    ''' 
    Scores a single game string, returning tricks1, tricks2, cards1, cards2
    '''
    tricks1 = 0 #initialize variables to store tricks and cards
    tricks2 = 0
    cards1 = 0
    cards2 = 0
    cards_left = len(game_str) ##initialize to store cards left
    starting_indx=0 #begin at index 0, will get updated in loop
    while cards_left > 0: #while there are cards left in the deck
        winning_pattern, winning_indx = compare_patterns(game_str,pattern1,pattern2,starting_indx) #compare to find which pattern appears first
        if winning_pattern != None: #if at least one pattern is found
            if winning_pattern == pattern1: #update tricks and cards according to winner
                tricks1 += 1 #add one trick
                cards1 += ((winning_indx + 3) - starting_indx) #add the number of cards since the starting index (+3 to account for 2 more cards in pattern and since index is zero based)
            elif winning_pattern == pattern2: #same if pattern 2 wins
                tricks2 += 1
                cards2 += ((winning_indx + 3) - starting_indx)
            cards_left = (len(game_str)) - (winning_indx + 3) #if a pattern was found, update cards left by subracting the total cards taken from original deck length
            starting_indx = (winning_indx+3) #if a pattern was found, update the starting index so next time the loop runs it starts after the cards already won
        else:
            cards_left = 0 #if neither pattern was found, update cards_left to zero, ending the loop
    return tricks1, tricks2, cards1, cards2