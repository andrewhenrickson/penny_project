import numpy as np

# Load the file
file_path = "/Users/andrewhenrickson/Desktop/repo/penny_project/data/decks/decks_100x52_seed_36.npz"
data = np.load(file_path)

# View all array keys stored inside the archive
print("Keys:", data.files)

# Inspect the shape and datatype of each array
for key in data.files:
    print(f"{key}: shape={data[key].shape}, dtype={data[key].dtype}")

# Access a specific array
decks = data[data.files[0]]

print(decks)