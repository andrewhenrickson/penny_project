#!/usr/bin/env python
# coding: utf-8

# <h1> Testing cell for one deck </h1>

# In[2]:


import numpy as np
from itertools import product
import pandas as pd
from pathlib import Path

file_path = "data/decks/decks_100x52_seed_1060.npz"

with np.load(file_path) as data:
    packed_decks = data["decks"]
    n_cards = int(data["n_cards"])  # e.g., 52

# 1. Unpack bits using the same axis and bitorder
unpacked = np.unpackbits(packed_decks, axis=1, bitorder="little")

# 2. Trim padding bits beyond the original n_cards count
original_decks = unpacked[:, :n_cards]

print("Restored shape:", original_decks.shape)  # Output: (100, 52)
print(original_decks[1])



# <h1> Get IDX for first game type with tricks </h1>

# In[4]:


def get_idx(deck_string: str, idx: int, first_choice: str, second_choice: str) -> int: 
    '''
    This function takes the string of the deck, the index to start at, and the two players pattern choices. 
    It finds the indicies for both patterns and compares them. If two valid indicies are returned, 
    take the smaller number, indicate who gets a point and return the index + 3 to main function to update 
    scores and where to start next search. If one of the indicies is -1, it will take the non -1 value as
    the index and allocate points accordingly. If both indicies are -1, the deck is done being searched, and 
    sends final_idx as None to trigger next deck.
    '''
    points = None
    first_idx = deck_string.find(first_choice, idx)
    second_idx = deck_string.find(second_choice, idx)
    # print(f'Found match at {first_idx} and {second_idx}')
    if first_idx == -1 and second_idx == -1:
        final_idx = None
        org_idx = idx
    else:
        if first_idx == -1:
            org_idx = second_idx
            points = 1
        elif second_idx == -1:
            org_idx = first_idx
            points = 0
        else:
            org_idx = first_idx if first_idx < second_idx else second_idx
            points = 0 if first_idx < second_idx else 1

        final_idx = org_idx + 3

        

    return final_idx, points

    


# <h1> Get tricks from the decks for first game type </h1>

# In[5]:


def find_tricks(first_choice: str, second_choice: str, original_decks: list) -> int:
    
    ''' 
    This function iterates through the decks that were created and sends parameters to get_idx
    to look who won the deck. After recieivng the point allocation and idx, points are updated
    and then sends another search with the next idx. If idx is returned as None, the while loop
    is broken and the next deck is searched. Points for each deck are computed inside of the outer
    for loop, and the overall wins are stores globally. The fucntion returns the number of wins for
    player 1, player 2, and how many ties occured. 
    '''

    p1 = 0
    p2 = 0
    tie = 0
    for i, deck in enumerate(original_decks):
        s = str(deck)
        idx = 0
        end_of_str = False
        first_player_points = 0
        second_player_points = 0
        deck_str = s[1:-1].replace(" ", "").replace("\n", "")
        while end_of_str == False:
            idx, points = get_idx(deck_str, idx, first_choice, second_choice)
            if points == 0:
                first_player_points += 1
            elif points == 1:
                second_player_points += 1
            if idx == None:
                end_of_str = True
                if first_player_points > second_player_points:
                    p1 += 1
                if second_player_points > first_player_points:
                    p2 += 1
                if second_player_points == first_player_points:
                    tie += 1

    return p1, p2, tie
            

p1, p2, tie = find_tricks('101', '001', original_decks)
print(p1, p2, tie)
        


# <h1> Iterate through all combos for all decks <h1>

# In[8]:


import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
from itertools import product

def iterate_all_combos():
    first_player_combos = list(product([0, 1], repeat=3))
    second_player_combos = list(product([0, 1], repeat=3))

    results = {
        "Player 1 Combo": [],
        "Player 2 Combo": [],
        "Player 1 Wins": [],
        "Player 2 Wins": [],
        "Ties": [],
        "Player 1 Win %": [],
        "Player 2 Win %": [],
        "Tie %": [],
    }

    folder_path = Path("data/decks")

    totals = {}
    for p1 in first_player_combos:
        for p2 in second_player_combos:
            p1_str = str(p1)[1:-1].replace(",", "").replace(" ", "")
            p2_str = str(p2)[1:-1].replace(",", "").replace(" ", "")
            if p1_str != p2_str:
                totals[(p1_str, p2_str)] = [0, 0, 0]

    for file_path in folder_path.glob("*.npz"):
        print(f"Processing: {file_path.name}")

        with np.load(file_path) as data:
            packed_decks = data["decks"]
            n_cards = int(data["n_cards"])

        unpacked = np.unpackbits(packed_decks, axis=1, bitorder="little")
        original_decks = unpacked[:, :n_cards]

        for i in range(len(first_player_combos)):
            p1_combo = (
                str(first_player_combos[i])[1:-1]
                .replace(",", "")
                .replace(" ", "")
            )
            for j in range(len(second_player_combos)):
                p2_combo = (
                    str(second_player_combos[j])[1:-1]
                    .replace(",", "")
                    .replace(" ", "")
                )
                if p1_combo == p2_combo:
                    continue
                else:
                    p1, p2, tie = find_tricks(
                        p1_combo, p2_combo, original_decks
                    )
                    totals[(p1_combo, p2_combo)][0] += p1
                    totals[(p1_combo, p2_combo)][1] += p2
                    totals[(p1_combo, p2_combo)][2] += tie

    for (p1_combo, p2_combo), (p1, p2, tie) in totals.items():
        total = p1 + p2 + tie
        p1_win_perc = p1 / total if total > 0 else 0
        p2_win_perc = p2 / total if total > 0 else 0
        tie_perc = tie / total if total > 0 else 0

        results["Player 1 Combo"].append(p1_combo)
        results["Player 2 Combo"].append(p2_combo)
        results["Player 1 Wins"].append(p1)
        results["Player 2 Wins"].append(p2)
        results["Ties"].append(tie)
        results["Player 1 Win %"].append(p1_win_perc)
        results["Player 2 Win %"].append(p2_win_perc)
        results["Tie %"].append(tie_perc)

    df = pd.DataFrame(results)

    # --- Save to tricks.db ---
    db_path = Path("tricks.db")  # Or Path("data/tricks.db") if in a folder
    with sqlite3.connect(db_path) as conn:
        df.to_sql("trick_stats", conn, if_exists="replace", index=False)
        print(f"Saved {len(df)} rows to '{db_path}' in table 'trick_stats'.")


iterate_all_combos()


# In[10]:


def get_idx_with_cards_earned(deck_string: str, idx: int, first_choice: str, second_choice: str) -> int: 
    '''
    This function takes the string of the deck, the index to start at, and the two players pattern choices. 
    It finds the indicies for both patterns and compares them. If two valid indicies are returned, 
    take the smaller number, indicate who gets a point and return the index + 3 to main function to update 
    scores and where to start next search. If one of the indicies is -1, it will take the non -1 value as
    the index and allocate points accordingly. If both indicies are -1, the deck is done being searched, and 
    sends final_idx as None to trigger next deck.
    '''
    points = None
    points_earned = None
    idx_passed = idx
    first_idx = deck_string.find(first_choice, idx)
    second_idx = deck_string.find(second_choice, idx)
    #check if there are no more to be found
    if first_idx == -1 and second_idx == -1:
        final_idx = None
        org_idx = idx
    else:
        if first_idx == -1:
            org_idx = second_idx
            points = 1
        elif second_idx == -1:
            org_idx = first_idx
            points = 0
        else:
            org_idx = first_idx if first_idx < second_idx else second_idx
            points = 0 if first_idx < second_idx else 1

        final_idx = org_idx + 3
        points_earned = final_idx - idx_passed

        

    return final_idx, points, points_earned


# In[11]:


def find_points(first_choice: str, second_choice: str, original_decks: list) -> int:
    
    ''' 
    This function iterates through the decks that were created and sends parameters to get_idx
    to look who won the deck. After recieivng the point allocation and idx, points are updated
    and then sends another search with the next idx. If idx is returned as None, the while loop
    is broken and the next deck is searched. Points for each deck are computed inside of the outer
    for loop, and the overall wins are stores globally. The fucntion returns the number of wins for
    player 1, player 2, and how many ties occured. 
    '''

    p1 = 0
    p2 = 0
    tie = 0
    for i, deck in enumerate(original_decks):
        s = str(deck)
        idx = 0
        end_of_str = False
        first_player_points = 0
        second_player_points = 0
        deck_str = s[1:-1].replace(" ", "").replace("\n", "")
        while end_of_str == False:
            idx, points, points_earned = get_idx_with_cards_earned(deck_str, idx, first_choice, second_choice)
            if points == 0:
                first_player_points += points_earned
            elif points == 1:
                second_player_points += points_earned
            if idx == None:
                end_of_str = True
                if first_player_points > second_player_points:
                    p1 += 1
                if second_player_points > first_player_points:
                    p2 += 1
                if second_player_points == first_player_points:
                    tie += 1


    return p1, p2, tie
            

p1, p2, tie = find_points('101', '001', original_decks)
print(p1, p2, tie)
        


# In[13]:


import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
from itertools import product

def iterate_all_combos_for_points():
    first_player_combos = list(product([0, 1], repeat=3))
    second_player_combos = list(product([0, 1], repeat=3))

    results = {
        "Player 1 Combo": [],
        "Player 2 Combo": [],
        "Player 1 Wins": [],
        "Player 2 Wins": [],
        "Ties": [],
        "Player 1 Win %": [],
        "Player 2 Win %": [],
        "Tie %": [],
    }

    folder_path = Path("data/decks")

    totals = {}
    for p1 in first_player_combos:
        for p2 in second_player_combos:
            p1_str = str(p1)[1:-1].replace(",", "").replace(" ", "")
            p2_str = str(p2)[1:-1].replace(",", "").replace(" ", "")
            if p1_str != p2_str:
                totals[(p1_str, p2_str)] = [0, 0, 0]

    for file_path in folder_path.glob("*.npz"):
        print(f"Processing: {file_path.name}")
        with np.load(file_path) as data:
            packed_decks = data["decks"]
            n_cards = int(data["n_cards"])

        unpacked = np.unpackbits(packed_decks, axis=1, bitorder="little")
        original_decks = unpacked[:, :n_cards]

        for i in range(len(first_player_combos)):
            p1_combo = str(first_player_combos[i])[1:-1].replace(",", "").replace(" ", "")
            for j in range(len(second_player_combos)):
                p2_combo = str(second_player_combos[j])[1:-1].replace(",", "").replace(" ", "")
                if p1_combo == p2_combo:
                    continue
                else:
                    p1, p2, tie = find_points(p1_combo, p2_combo, original_decks)
                    totals[(p1_combo, p2_combo)][0] += p1
                    totals[(p1_combo, p2_combo)][1] += p2
                    totals[(p1_combo, p2_combo)][2] += tie

    for (p1_combo, p2_combo), (p1, p2, tie) in totals.items():
        total = p1 + p2 + tie
        p1_win_perc = p1 / total if total > 0 else 0
        p2_win_perc = p2 / total if total > 0 else 0
        tie_perc = tie / total if total > 0 else 0

        results["Player 1 Combo"].append(p1_combo)
        results["Player 2 Combo"].append(p2_combo)
        results["Player 1 Wins"].append(p1)
        results["Player 2 Wins"].append(p2)
        results["Ties"].append(tie)
        results["Player 1 Win %"].append(p1_win_perc)
        results["Player 2 Win %"].append(p2_win_perc)
        results["Tie %"].append(tie_perc)

    df = pd.DataFrame(results)

    # --- Save to SQLite Database ---
    db_path = Path("points.db")
    with sqlite3.connect(db_path) as conn:
        df.to_sql("combo_stats", conn, if_exists="replace", index=False)
        print(f"Successfully saved {len(df)} rows to '{db_path}' in table 'combo_stats'.")

iterate_all_combos_for_points()

