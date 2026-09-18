#these will go into dataproc.py
#hello
def game_to_string(game):
    '''
    Turns an array from game_history into a string for pattern matching
    '''
    game_str = "".join(str(card)for card in game)
    return game_str

def find_pattern(game_str, pattern):
    ''' 
    Identifies the index of the first time a pattern is found within a game string
    '''
    pattern_indx = game_str.find(pattern)
    return pattern_indx

def compare_patterns(game_str, pattern1, pattern2):
    ''' 
    Compares two patterns to see which one appears first within a game string. Returns the winning pattern and its index
    '''
    pattern1_indx = find_pattern(game_str, pattern1) #find index of first pattern
    pattern2_indx = find_pattern(game_str, pattern2) #find index of second pattern

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

def remove_cards(game_str, winning_indx): #maybe change later to .find to make it run faster 
    ''' 
    Removes all cards from a game string that come before the winning pattern, and the winning pattern itself. Returns the shortened string
    '''
    new_str = game_str[winning_indx+3:]
    return new_str
