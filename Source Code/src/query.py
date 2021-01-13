import zlib
from pathlib import Path
import numpy as np

from src.lsh import Index
from src.utils import create_shingles, SHINGLE_LEN, NO_OF_HASHES, BANDS, BAND_SIZE


def find_similar_docs(query: Path, index: Index):
    """
    Apply all 3 steps on the query and find similar docs from the corpus
    :param query: Path of the query file
    :param index: Index object
    :return: None
    """
    file = open(query, encoding='unicode_escape')
    content = file.read()
    print("Query Content = ", content)
    if len(content) < SHINGLE_LEN:
        print("Query content must be at least the size of " + str(SHINGLE_LEN) + "!")
        return

    # Shingling
    shingles = create_shingles(content, True)
    n = len(index.shingle_set)

    # MinHashing
    sig_list = np.full(NO_OF_HASHES, n)
    for row, shingle in enumerate(index.shingle_set):
        row += 1
        hashes = [(h[0] * row + h[1]) % n for h in index.HASHES]
        if shingle in shingles:
            sig_list = np.where(sig_list > hashes, hashes, sig_list)

    # LSH
    similar_docs = set()
    for band in range(BANDS):
        hash_col = sig_list[band * BAND_SIZE: min((band + 1) * BAND_SIZE, NO_OF_HASHES)]
        hash_value = int(zlib.crc32(bytes(hash_col)))
        index_set = index.buckets[band][hash_value]
        if len(index_set) > 0:
            similar_docs.update(index_set)

    # Showing Results
    if len(similar_docs) > 0:
        print("Sequences similar to the given query:", sorted(similar_docs))
    print(str(len(similar_docs)) + " similar sequences found.")
