import random
import zlib
from collections import defaultdict

import numpy as np

from src.utils import NO_OF_HASHES, create_shingles, BANDS, BAND_SIZE


class Index:
    """
    The index which contains all the information to find similarity between corpus docs
    like signature matrix, hash functions, etc.
    """
    def __init__(self):
        self.doc_matrix = None
        self.shingle_set = set()
        self.matrix = []
        self.doc_sets = []
        random.seed(10)
        self.HASHES = [random.sample(range(1, 2 * NO_OF_HASHES), 2) for _ in range(NO_OF_HASHES)]
        self.buckets = []
        self.doc_names = []

    def add_shingles(self, text: str):
        """
        SHINGLING STEP:
        Add the shingles from the text to the shingles set
        :param text: The contents of the document
        :return: None
        """
        new_shingles = create_shingles(text)
        self.doc_sets.append(new_shingles)
        self.shingle_set.update(new_shingles)

    def create_signature_matrix(self):
        """
        MIN-HASHING STEP:
        Create signature matrix using set of shingles and corpus docs
        :param: None
        :return: None
        """
        print("\n----- Generating signature matrix ..")
        self.shingle_set = list(self.shingle_set)
        n = len(self.shingle_set)
        self.matrix = np.full((NO_OF_HASHES, len(self.doc_sets)), n)

        for row, shingle in enumerate(self.shingle_set):
            row += 1
            hashes = [(h[0] * row + h[1]) % n for h in self.HASHES]
            for j, doc_set in enumerate(self.doc_sets):
                if shingle in doc_set:
                    self.matrix[:, j] = np.where(self.matrix[:, j] > hashes, hashes, self.matrix[:, j])
        self.doc_names = [i+1 for i in range(len(self.doc_sets))]
        self.doc_sets.clear()
        print("----- Signature Matrix generated.")

    def lsh(self):
        """
        LSH STEP:
        Apply Locality Sensitivity Hashing using signature matrix and create groups of similar docs
        :param: None
        :return: None
        """
        for band in range(BANDS):
            band_map = defaultdict(set)
            start = band * BAND_SIZE
            end = min((band + 1) * BAND_SIZE, NO_OF_HASHES)
            for j, doc in enumerate(self.doc_names):
                hash_col = self.matrix[start: end, j]
                hash_value = int(zlib.crc32(bytes(hash_col)))
                band_map[hash_value].add(doc)
            self.buckets.append(band_map)
