# Similarity Functions
#
# Mathematical utilities used to
# compare embedding vectors.
#
# Independent of storage, search,
# and embedding generation.

import numpy as np


def cosine_similarity(v1, v2):

    return (
        np.dot(v1, v2)
        /
        (np.linalg.norm(v1) * np.linalg.norm(v2))
    )