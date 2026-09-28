import json
import numpy as np
from pathlib import Path
from datetime import datetime as dt

PATH_DECKS = Path('data/decks/')
PATH_SEED_LOG = Path('data/seed.json')
SEED_BASE = 1


def make_decks(seed: int, 
               n_decks: int,
               n_cards: int = 10
              ) -> np.ndarray:
    
    rng = np.random.default_rng(seed)
    
    all_decks = []

    for i in range(n_decks):
        deck = [0, 1] * (n_cards // 2)
        rng.shuffle(deck)
        all_decks.append(deck)

    return np.array(all_decks, dtype=np.uint8)
        
def get_next_seed() -> int:
    '''
    Read the last seed used, increment by 1,
    and update seed.json.
    '''
    # make sure the parent directory exists, parent is the data folder, exist_ok says its chill if it already exists
    PATH_SEED_LOG.parent.mkdir(parents=True,exist_ok=True)

    # determine the next seed
    if not PATH_SEED_LOG.exists():
        print(f'no seed log found, starting with {SEED_BASE}')
        seed = SEED_BASE
    else:
        with PATH_SEED_LOG.open('r') as f:
            seed_log = json.load(f)
        seed = seed_log['seed'] + 1

    # update the log
    seed_log = {
        'seed': seed,
        'seed_time': str(dt.now())
    }

    # write new seed
    with PATH_SEED_LOG.open('w') as f:
        json.dump(seed_log, f)
    
    return seed



def save_decks(
    decks: np.ndarray,
    seed: int
) -> Path:

    PATH_DECKS.mkdir(
        parents=True,
        exist_ok=True)

    n_decks = decks.shape[0]
    n_cards = decks.shape[1]

    packed_decks = np.packbits(
        decks,
        axis=1,
        bitorder="little" )

    filename = (
        PATH_DECKS /
        f"decks_{n_decks}x{n_cards}_seed_{seed}.npz" )

    np.savez(
        filename,
        decks=packed_decks,
        n_cards=n_cards,
        seed=seed)

    return filename
    

def generate_decks(
    n_decks: int,
    n_cards: int = 52,
    batch_size: int = 1000
):
    """
    Generate and save decks in batches.

    Each batch contains at most 1000 decks and
    receives a new seed.
    """

    deck_files = []

    decks_remaining = n_decks

    while decks_remaining > 0:

        # determine how many decks go in this batch
        current_batch_size = min(
            batch_size,
            decks_remaining
        )

        # get a new seed for every batch
        seed = get_next_seed()

        # make the decks
        decks = make_decks(
            seed=seed,
            n_decks=current_batch_size,
            n_cards=n_cards
        )

        # save them
        filename = save_decks(
            decks=decks,
            seed=seed
        )

        deck_files.append(filename)

        # update number still needed
        decks_remaining -= current_batch_size

    return deck_files

def get_total_decks() -> int:

    total_decks = 0

    for file_path in PATH_DECKS.glob("*.npz"):

        with np.load(file_path) as data:
            total_decks += data["decks"].shape[0]

    return total_decks
