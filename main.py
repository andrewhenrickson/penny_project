# %%
import numpy as np
from itertools import product
import pandas as pd
from pathlib import Path
import sqlite3
import json
from datetime import datetime as dt
import matplotlib.pyplot as plt
import time

from datagen import make_decks, get_next_seed, save_decks, generate_decks, get_total_decks
from processing import iterate_all_combos, iterate_all_combos_for_points
from make_fig import (load_data, process_data, create_heatmap_data, plot_heatmap
)

def main(n_decks):

    # 1. Generate new decks

    new_deck_files = generate_decks(n_decks=n_decks, batch_size=1000)

    print(f"Created {n_decks} new decks.")

    # 2. Count ALL saved decks

    total_decks = get_total_decks()

    print(f"Total decks available: {total_decks}")

    # 3. Run Tricks strategy

    print("\nProcessing Tricks strategy...")

    iterate_all_combos(deck_files=new_deck_files)

    tricks_data = load_data(
        "tricks.db",
        "trick_stats"
    )

    tricks_data = process_data(tricks_data)

    tricks_heatmap, tricks_labels = create_heatmap_data(
        tricks_data
    )

    # 4. Run Cards strategy

    print("\nProcessing Cards strategy...")

    iterate_all_combos_for_points(deck_files=new_deck_files)

    cards_data = load_data(
        "points.db",
        "combo_stats"
    )

    cards_data = process_data(cards_data)

    cards_heatmap, cards_labels = create_heatmap_data(
        cards_data
    )

    print(f"\n{n_decks:,} new decks successfully added.")
    print(f"Results now include {total_decks:,} total decks.\n")

    # 5. Display BOTH graphs

    plot_heatmap(
        tricks_heatmap,
        tricks_labels,
        n_decks=total_decks,
        strategy="tricks"
    )

    plot_heatmap(
        cards_heatmap,
        cards_labels,
        n_decks=total_decks,
        strategy="cards"
    )


if __name__ == "__main__":

    n_decks = int(
        input("How many additional decks would you like to simulate? ")
    )

    start_time = time.perf_counter()

    main(
        n_decks=n_decks
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    print(f"\nTotal run time: "f"{minutes} minutes, {seconds:.2f} seconds")




