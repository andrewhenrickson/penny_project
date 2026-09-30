# %%
import time

from src.datagen import make_decks, get_next_seed, save_decks, generate_decks, get_total_decks
from src.processing import iterate_all_combos, iterate_all_combos_for_points
from src.make_fig import (load_data, process_data, create_heatmap_data, plot_heatmap
)

def main(n_decks):

    # generate new decks

    new_deck_files = generate_decks(n_decks=n_decks, batch_size=1000)

    print(f"Created {n_decks} new decks.")

    # count all saved decks

    total_decks = get_total_decks()

    print(f"Total decks available: {total_decks}")

    # run tricks strategy

    print("\nProcessing Tricks strategy...")

    # scores the decks
    iterate_all_combos(deck_files=new_deck_files)

    # loads old data
    tricks_data = load_data(
    "data/tricks.db",
    "trick_stats")

    # formats the data and keeps only what we need for the heatmaps
    tricks_data = process_data(tricks_data)

    # makes heatmap labels
    tricks_heatmap, tricks_labels = create_heatmap_data(
        tricks_data
    )

    # run cards strategy

    print("\nProcessing Cards strategy...")

    # scores the decks
    iterate_all_combos_for_points(deck_files=new_deck_files)

    # loads old data
    cards_data = load_data(
        "data/points.db",
        "combo_stats"
    )

    cards_data = process_data(cards_data)

    cards_heatmap, cards_labels = create_heatmap_data(
        cards_data
    )

    print(f"\n{n_decks:,} new decks successfully added.")
    print(f"Results now include {total_decks:,} total decks.\n")

    # create both plots

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


# runs the actual function including the input, and times it because I was curious.
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