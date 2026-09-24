
import numpy as np
import pandas as pd

def game_to_string(packed_game):
    '''
    Turns an array from game_history into a string for pattern matching
    '''
    unpacked_game = np.unpackbits(packed_game) #unpack bits 
    game_str = "".join(str(card)for card in unpacked_game[:52])  #turn game into string and ensure there is 52 cards 
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

def score_by_tricks(tricks1, tricks2):
    if tricks1 > tricks2: #person 1 wins
        return 1
    elif tricks2 > tricks1: #person 2 wins
        return 2
    elif tricks1 == tricks2: #tie
        return 3
    else:
        return 0
    
def score_by_cards(cards1, cards2):
    if cards1 > cards2: #person 1 wins
        return 1
    elif cards2 > cards1: #person 2 wins
        return 2
    elif cards1 == cards2: #tie
        return 3
    else:
        return 0

def score_game(game_str,pattern1,pattern2):
    ''' 
    Scores a single game string, returning a list of game_str, pattern1, pattern2, tricks1, tricks2, cards1, cards2, winner_tricks, winner_cards to save
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
    winner_tricks = score_by_tricks(tricks1, tricks2)
    winner_cards = score_by_cards(cards1, cards2)
    new_row = [game_str,pattern1,pattern2,tricks1,tricks2,cards1,cards2,winner_tricks,winner_cards]
    return new_row

my_patterns = ['000','001','010','011','100','101','110','111']
opp_patterns = ['000','001','010','011','100','101','110','111']

def run_all_patterns (game_str):
    ''' 
    tries all (different) patterns against each other for a single game string, returns a list containing lists of score info for each combination
    '''
    new_rows = [] #initialize list to store new score info as rows are calculated
    for pattern1 in my_patterns: #run each combination of my patterns and opponent's patterns
        for pattern2 in opp_patterns:
            if pattern1 != pattern2: #exclude cases where both patterns are the same
                new_row = score_game(game_str, pattern1, pattern2) #runs score_game for each combination and gets info to store
                new_rows.append(new_row) #appends info to broader list for results from all combinations
    return new_rows


def get_results_for_new_games(game_history):
    ''' 
    scores all games in game_history using all patterns, returns a dataframe with results info to calcualate probabilities
    '''
    new_scores = [] #list to store info from each game in game_history using each combination
    for game in game_history:
        game_str = game_to_string(game) #unpack game and turn into string
        game_results = run_all_patterns(game_str) #try all patterns for game and store info as game_results
        # add code to store game results in data folder
        #for now storing as a dataframe but could change to .npz
    new_scores.append(game_results) #append game info to list containing info on all games in game_history
    new_scores_df = pd.DataFrame(game_results, columns = ['game_str','pattern1','pattern2','tricks1', 'tricks2', 'cards1', 'cards2', 'winner_tricks','winner_cards'],) #turn into dataframe (may change data storage type later)
    
    #add some code here to make sure the data goes to the data folder

    return new_scores_df