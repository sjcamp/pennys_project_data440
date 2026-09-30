
import numpy as np
import pandas as pd
from pathlib import Path

def game_to_string(packed_game: np.ndarray) ->str:
    '''
    Turns an array from game_history into a string for pattern matching
    '''
    unpacked_game = np.unpackbits(packed_game) #unpack bits 
    game_str = "".join(str(card)for card in unpacked_game[:52])  #turn game into string and ensure there is 52 cards 
    return game_str

def find_pattern(game_str: str, pattern: str, starting_indx: int = 0) -> int:
    ''' 
    Identifies the index of the first time a pattern is found within a game string
    '''
    pattern_indx = game_str.find(pattern, starting_indx)
    return pattern_indx

def compare_patterns(game_str: str, pattern1: str, pattern2: str, starting_indx: int = 0) -> tuple[str,int]:
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

def score_by_tricks(tricks1:int, tricks2:int) -> int:
    if tricks1 > tricks2: #person 1 wins
        return 1
    elif tricks2 > tricks1: #person 2 wins
        return 2
    elif tricks1 == tricks2: #tie
        return 3
    else:
        return 0
    
def score_by_cards(cards1: int, cards2:int) -> int:
    if cards1 > cards2: #person 1 wins
        return 1
    elif cards2 > cards1: #person 2 wins
        return 2
    elif cards1 == cards2: #tie
        return 3
    else:
        return 0

def score_game(game_str:str,pattern1:str,pattern2:str) -> list:
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

opp_patterns = ['000','001','010','011','100','101','110','111']    
my_patterns = ['000','001','010','011','100','101','110','111']

def run_all_patterns (game_str:str) -> list:
    ''' 
    tries all (different) patterns against each other for a single game string, returns a list containing lists of score info for each combination
    '''
    new_rows = [] #initialize list to store new score info as rows are calculated
    for pattern1 in opp_patterns: #run each combination of my patterns and opponent's patterns
        for pattern2 in my_patterns:
            if pattern1 != pattern2: #exclude cases where both patterns are the same
                new_row = score_game(game_str, pattern1, pattern2) #runs score_game for each combination and gets info to store
                new_rows.append(new_row) #appends info to broader list for results from all combinations
    return new_rows


def get_results_for_new_games(game_history: np.ndarray, save:bool=False) -> pd.DataFrame:
    ''' 
    scores all games in game_history using all patterns, returns a dataframe with results info to calcualate probabilities.
   
    '''
    new_scores = [] #list to store info from each game in game_history using each combination
    for game in game_history:
        game_str = game_to_string(game) #unpack game and turn into string
        game_results = run_all_patterns(game_str) #try all patterns for game and store info as game_results
        new_scores.append(game_results) #append game info to list containing info on all games in game_history
    merged_scores = [results for game in new_scores for results in game] #fix shape to turn into dataframe (got help from ChatGPT)
    new_scores_df = pd.DataFrame(merged_scores, columns = ['game_str','pattern1','pattern2','tricks1', 'tricks2', 'cards1', 'cards2', 'winner_tricks','winner_cards'],) #turn into dataframe (may change data storage type later)

    # if save: #only save the full results dataframe if explicitly requested
    #     #similar to datagen.py for saving to /data
    #     output_dir = Path('./data')
    #     output_dir.mkdir(parents=True, exist_ok=True)
    #     arr = new_scores_df.to_records(index=False) #converts df to numpy array 
    #     np.savez_compressed(output_dir / "game_results_array.npz", data=arr)

    return new_scores_df

def calc_probs(df:pd.DataFrame, pattern1:str, pattern2:str) ->tuple[int, int,int,int]:
    subset = df[(df['pattern1']==pattern1) & (df['pattern2']==pattern2)] #subset the dataframe to get only rows with the choice patterns
    prob_wintricks = len(subset[subset['winner_tricks'] == 2]) / len(subset) *100 #calculate probability of winning as the number of rows of the subset where I (pattern2) wins by tricks divided by total rows in the subset, multiplied by 100 to be a percent
    prob_tietricks = len(subset[subset['winner_tricks'] == 3]) / len(subset) *100 #calculate probability of winning as the number of rows of the subset where they tie by tricks divided by total rows in the subset, multiplied by 100 to be a percent
    prob_wincards = len(subset[subset['winner_cards'] == 2]) / len(subset) *100 #calculate probability of winning as the number of rows of the subset where I (pattern2) wins by cards divided by total rows in the subset, multiplied by 100 to be a percent
    prob_tiecards = len(subset[subset['winner_cards'] == 3]) / len(subset) *100 #calculate probability of winning as the number of rows of the subset where they tie by cards divided by total rows in the subset, multiplied by 100 to be a percent
    return int(prob_wintricks), int(prob_tietricks), int(prob_wincards), int(prob_tiecards) #return as integers


# def make_prob_arrays(game_history): # commented out to keep for looking back on but no longer used
#     ''' 
#     Produces 4 probability arrays (winning by tricks, tying by tricks, winning by cards, tying by cards) 
#     for a single batch of games. Note: these are percentages, and percentages from
#     different-sized batches can't simply be added together to combine runs -- see
#     make_count_arrays below, which is what main.py now uses for that purpose.
#     '''
#     df = get_results_for_new_games(game_history) #process the data toget the dataframe containing results
#     #initialize 4 arrays of 0s to store probabilities
#     p_wintricks_array = np.zeros((8,8),dtype=int)
#     p_tietricks_array = np.zeros((8,8),dtype=int)
#     p_wincards_array = np.zeros((8,8),dtype=int)
#     p_tiecards_array = np.zeros((8,8),dtype=int)
    
#     #for loops to update values in the arrays
#     for i in range(8):
#         for j in range(8):
#             if j != i:
#                 prob_wintricks, prob_tietricks, prob_wincards, prob_tiecards = calc_probs(df,opp_patterns[i],my_patterns[j]) #calculate each probability at given combination of patterns
#                 p_wintricks_array[i][j] = prob_wintricks #update arrays
#                 p_tietricks_array[i][j] = prob_tietricks
#                 p_wincards_array[i][j] = prob_wincards
#                 p_tiecards_array[i][j] = prob_tiecards
#             else:
#                 p_wintricks_array[i][j] = 0 #keep the diagonals as 0
#                 p_tietricks_array[i][j] = 0
#                 p_wincards_array[i][j] = 0
#                 p_tiecards_array[i][j] = 0

#     return p_wintricks_array, p_tietricks_array, p_wincards_array, p_tiecards_array 

#below added calc_counts and make_count_arrays with help from claude and previous code to help count every game won (not just latest batch) and run it for every combination 


def calc_counts(df:pd.DataFrame, pattern1:str, pattern2:str)->tuple[int, int,int,int]:
    '''
    Same idea as calc_probs, but returns raw counts instead of percentages so that
    results from different-sized runs can be correctly combined later. 
    '''
    subset = df[(df['pattern1']==pattern1) & (df['pattern2']==pattern2)]
    win_tricks = int((subset['winner_tricks'] == 2).sum())
    tie_tricks = int((subset['winner_tricks'] == 3).sum())
    win_cards = int((subset['winner_cards'] == 2).sum())
    tie_cards = int((subset['winner_cards'] == 3).sum())
    return win_tricks, tie_tricks, win_cards, tie_cards


def make_count_arrays(game_history:np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
    '''
    Scores game_history and returns 4 raw-count arrays (win by tricks, tie by
    tricks, win by cards, tie by cards) plus n_games, the number of decks scored.
    This is what gets saved to disk per-run: counts + n_games can be summed across
    many runs of different sizes and then converted to a percentage once, at
    visualization time (see datavis.load_all_scored_data / counts_to_pct).
    '''
    df = get_results_for_new_games(game_history) 
    win_tricks_array = np.zeros((8,8), dtype=int)
    tie_tricks_array = np.zeros((8,8), dtype=int)
    win_cards_array = np.zeros((8,8), dtype=int)
    tie_cards_array = np.zeros((8,8), dtype=int)

    n_games = len(game_history)

    for i in range(8):
        for j in range(8):
            if j != i:
                win_tricks, tie_tricks, win_cards, tie_cards = calc_counts(df, opp_patterns[i], my_patterns[j])
                win_tricks_array[i][j] = win_tricks
                tie_tricks_array[i][j] = tie_tricks
                win_cards_array[i][j] = win_cards
                tie_cards_array[i][j] = tie_cards
            #diagonal (j == i) left as 0, same as make_prob_arrays

    return win_tricks_array, tie_tricks_array, win_cards_array, tie_cards_array, n_games
