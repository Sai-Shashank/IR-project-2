import os
import pickle
import sys
import time
from pathlib import Path
from sys import stderr, path

project_dir = Path(__file__).parent.resolve()
if str(project_dir) not in path:
    path.append(str(project_dir))
if str(project_dir / 'src') not in path:
    path.append(str(project_dir / 'src'))

from src.lsh import Index
from src.query import find_similar_docs
from src.utils import SHINGLE_LEN

project_dir = Path(__file__).parent.resolve()
if str(project_dir) not in path:
    path.append(str(project_dir))
if str(project_dir / 'src') not in path:
    path.append(str(project_dir / 'src'))


def gen_index(file: Path, index: Index):
    """
    Generates index from all corpus docs
    :param file: Path of the file containing genomes
    :param index: Index object
    :return: None
    """
    print("\n----- Creating Shingles ...")
    for line in open(file, encoding='unicode_escape'):
        if len(line) >= SHINGLE_LEN + 2:
            index.add_shingles(line)
    print("----- Shingles created.")
    index.create_signature_matrix()
    index.lsh()


def main():
    """
    Starter function for either indexing or querying
    :param: None
    :return: None
    """
    arguments = sys.argv
    if len(arguments) != 3:
        stderr.write("Please provide arguments in proper format!")
        exit(1)
    if arguments[1] == "index":
        if not os.path.isfile(arguments[2]):
            stderr.write("Corpus is not a Valid File!")
            exit(1)
        index = Index()
        gen_index(Path(arguments[2]), index)
        with open('index.pk', 'wb+') as f:
            pickle.dump(index, f)
        print('\n----- Index generated in index.pk')
    elif arguments[1] == "query":
        if not os.path.isfile(arguments[2]):
            stderr.write("Query is not a Valid File!")
            exit(1)
        try:
            with open('index.pk', 'rb') as f:
                index = pickle.load(f)
        except FileNotFoundError:
            stderr.write("Generated Index not found!")
            exit(1)
        find_similar_docs(Path(arguments[2]), index)
    else:
        stderr.write("Please provide arguments in proper format!")
        exit(1)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("\nTotal Execution Time = " + str(time.time() - start_time) + " seconds")
