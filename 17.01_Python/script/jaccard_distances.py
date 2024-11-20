import multiprocessing as mp
from functools import partial
import numpy as np
from scipy.spatial.distance import pdist, squareform
import torch

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

def calculate_jaccard_distances(sample_X, X):
    combined_X = np.vstack([sample_X, X])
    distances = squareform(pdist(combined_X, metric='jaccard'))
    return distances[len(sample_X):, :len(sample_X)]

def parallelize_jaccard(sample, X):
    combined_X = np.vstack([sample, X])
    sample_distances = pdist(combined_X, metric='jaccard')[1:]
    return sample_distances

if __name__ == '__main__':
    print(f"Using device: {'MPS' if torch.backends.mps.is_available() else 'GPU' if torch.cuda.is_available() else 'CPU'}")
    # sample_X = ...
    # remaining_X = ...

    num_cores = mp.cpu_count()  # Nombre de cœurs disponibles
    pool = mp.Pool(num_cores)  # Créer un pool de processus

    jaccard_distances = []
    func = partial(parallelize_jaccard, X=remaining_X)
    for distance in pool.map(func, sample_X):
        jaccard_distances.append(distance)

    pool.close()
    pool.join()

    jaccard_distances = np.array(jaccard_distances)

    # Faites quelque chose avec jaccard_distances
    # ...