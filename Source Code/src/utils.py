import zlib
from typing import Set

SHINGLE_LEN = 10
NO_OF_HASHES = 200
BANDS = 10
BAND_SIZE = int(NO_OF_HASHES / BANDS)


def create_shingles(text: str, is_query: bool = False) -> Set[int]:
    """
    Creates hashed k-grams or shingles of the given text
    :param is_query: a boolean value deciding whether given text is of query or of corpus
    :param text: A String of which shingles are required
    :return: A Set of shingles present in the text
    """
    text = text.lower()
    end = len(text) - SHINGLE_LEN + 1 if is_query else len(text) - SHINGLE_LEN - 1
    return set(zlib.crc32(bytes(text[head:head + SHINGLE_LEN].encode('utf-8'))) for head in range(0, end))
