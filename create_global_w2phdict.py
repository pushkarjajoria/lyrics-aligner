import csv
import glob
import os
import pickle
from typing import Dict, List

from scripts.util import combine_dicts


def load_transcription_tsv(tsv_path: str) -> Dict[str, List[str]]:
    """
    Expects a TSV with headers 'word' and 'phonemes', where phonemes
    is a space- or comma-separated string.
    """
    d = {}
    with open(tsv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            word = row[0]
            # adjust splitting logic to your format:
            phonemes = row[1].split()
            d[word] = phonemes
    return d


# List of ARPAbet phonemes (as per CMUdict)
phonemes = ["AA","AE","AH","AO","AW","AY","B","CH","D","DH","EH","ER",
            "EY","F","G","HH","IH","IY","JH","K","L","M","N","NG",
            "OW","OY","P","R","S","SH","T","TH","UH","UW","V","W","Y","Z","ZH"]


def greedy_decode(s):
    i = 0
    result = []
    while i < len(s):
        # Try a 2-letter phoneme first
        if i+2 <= len(s) and s[i:i+2] in phonemes:
            result.append(s[i:i+2])
            i += 2
        # Otherwise try a 1-letter phoneme
        elif s[i:i+1] in phonemes:
            result.append(s[i:i+1])
            i += 1
        else:
            # Greedy step fails
            return None
    return result


def backtracking_decode(s):
    memo = {}

    def helper(i):
        if i == len(s):
            return [[]]  # reached end successfully
        if i in memo:
            return memo[i]
        solutions = []
        # Try a 2-letter phoneme
        if i+2 <= len(s) and s[i:i+2] in phonemes:
            for tail in helper(i+2):
                solutions.append([s[i:i+2]] + tail)
        # Try a 1-letter phoneme
        if s[i:i+1] in phonemes:
            for tail in helper(i+1):
                solutions.append([s[i:i+1]] + tail)
        memo[i] = solutions
        return solutions

    sols = helper(0)
    return sols  # list of lists of phoneme tokens (may be empty)


def fix_global_dict(combined):
    # Scan merged dict for error entries
    error_count = 0
    for key, value in combined.items():
        if "ERROR" in value:
            error_count += 1
            # Extract the raw phoneme string (remove arrow and quotes)
            raw = value[0].split("----->")[0].strip().strip("'\"")
            # Attempt greedy decode (explained below)
            tokens = greedy_decode(raw)
            if not tokens:
                print(f"Cannot greedily decode '{raw}'. Trying Backtracking.")
                tokens = backtracking_decode(raw)
                if not tokens:
                    print(f"Cannot backtrack decode '{raw}'")
                    print(f"Enter the Phoneme for {raw} space separated and all caps.")
                    user_input = input().strip()
                    tokens = user_input.split()
            combined[key] = tokens

    print(f"Found and corrected {error_count} error entries.")
    return combined


if __name__ == "__main__":
    base_dir = "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria Dataset"
    dicts = []

    # find all immediate subfolders
    for datapoint in os.listdir(base_dir):
        dp_path = os.path.join(base_dir, datapoint)
        if not os.path.isdir(dp_path):
            continue

        # look for ANY file matching "*transcription.tsv"
        matches = glob.glob(os.path.join(dp_path, "*transcription*"))
        if not matches:
            raise FileNotFoundError(f"No transcription.tsv found in '{datapoint}'")
        if len(matches) > 1:
            raise RuntimeError(f"Multiple transcription.tsv files in '{datapoint}': {matches}")

        tsv_path = matches[0]
        d = load_transcription_tsv(tsv_path)
        print(f"[INFO] Loaded {len(d)} entries from {os.path.basename(tsv_path)}")
        dicts.append(d)

    # combine all dicts (interactive on conflict)
    global_w2ph = combine_dicts(*dicts)
    global_w2ph = fix_global_dict(global_w2ph)
    # save to pickle
    out_path = os.path.join(base_dir, "word2phoneme_global.pickle")
    with open(out_path, "wb") as f:
        pickle.dump(global_w2ph, f)
    print(f"[SUCCESS] Wrote global word→phoneme dict to {out_path}")
    print("Done")
