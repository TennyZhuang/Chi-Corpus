from io import StringIO
import sys
import warnings
from itertools import combinations

import Levenshtein
from absl import logging

logging.set_verbosity(logging.ERROR)
warnings.simplefilter("ignore")

stdout, sys.stdout = sys.stdout, StringIO()
import synonyms
sys.stdout = stdout

fns = sys.argv[1:]

errors = 0
warns = 0
for fn in fns:
    with open(fn, mode="r") as f:
        vegetables = f.read().strip().split('\n')

    for _seq1, _seq2 in combinations(enumerate(vegetables, 1), 2):
        idx1, seq1 = _seq1
        idx2, seq2 = _seq2
        min_len = min(len(seq1), len(seq2))

        dist = Levenshtein.distance(seq1, seq2)
        if dist < 2 and min_len > 2:
            errors += 1
            print("\n".join(
                [f"{fn}:{idx1}:{idx2}: ERROR: Duplicate sentences", seq1, seq2, f"(distance={dist})"]))
        elif dist < 6:
            sim = synonyms.compare(seq1, seq2)
            if sim > 0.9:
                warns += 1
                print("\n".join([f"{fn}:{idx1}:{idx2}: WARNING: Possible duplicate sentences",
                                 seq1, seq2, f"(distance={dist}, similarity={sim})"]))

print("-"*10)
print(f"Total: {errors} error(s). {warns} warning(s).")

if errors > 0:
    exit(1)

