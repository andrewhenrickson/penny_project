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
    PATH_SEED_LOG.parent.mkdir(parents=True, exist_ok=True)

    # Determine the next seed
    if not PATH_SEED_LOG.exists():
        print(f'No seed log found, starting with {SEED_BASE}')
        seed = SEED_BASE
    else:
        with PATH_SEED_LOG.open('r') as f:
            seed_log = json.load(f)
        seed = seed_log['seed'] + 1

    # Update the log
    seed_log = {
        'seed': seed,
        'seed_time': str(dt.now())
    }
    with PATH_SEED_LOG.open('w') as f:
        json.dump(seed_log, f)
    
    return seed




def save_decks(decks: np.ndarray, 
               seed: int
              ) -> Path:
              
    '''
    This doesn't actually save anything,
    it is just a demo of how I might construct
    the filename.
    '''

    PATH_DECKS.mkdir(parents=True, exist_ok=True)

    n_decks = decks.shape[0]
    n_cards = decks.shape[1]

    packed_decks = np.packbits(
    decks,
    axis=1,
    bitorder="little")

    filename = PATH_DECKS / f'decks_{n_decks}x{n_cards}_seed_{seed}.npz'

    np.savez(
        filename,
        decks=packed_decks,
        n_cards=n_cards,
        seed=seed
    )

    return filename


make_decks(seed = SEED_BASE, n_decks = 20, n_cards = 10)


seed = get_next_seed()
print(seed)

deck_size = 52
num_decks = 100
num_batches = 10

for n in range(num_batches):
    seed = get_next_seed()
    decks = make_decks(seed, num_decks, deck_size)
    save_decks(decks, seed)