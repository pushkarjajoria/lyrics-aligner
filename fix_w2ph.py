import pickle
import re


arpabet_phonemes = [
    "AA", "AE", "AH", "AO", "AW", "AY",
    "B",
    "CH",
    "D", "DH",
    "EH", "ER", "EY",
    "F",
    "G",
    "HH",
    "IH", "IY",
    "JH",
    "K",
    "L",
    "M",
    "N", "NG",
    "OW", "OY",
    "P",
    "R",
    "S", "SH",
    "T", "TH",
    "UH", "UW",
    "V",
    "W",
    "Y",
    "Z", "ZH"
]


def extract_manual_phonemes(log_text, phoneme_dict):
    lines = log_text.strip().splitlines()

    current_word = None
    capture_next_line = False

    for line in lines:
        # Match the line indicating a missing word
        match = re.match(r"Unable to find the match for word: (.+?) in Aria:", line)
        if match:
            current_word = match.group(1).strip()
        elif current_word and line.startswith("Enter the phoneme string for"):
            # Now get the phoneme input on the next line
            capture_next_line = True
        elif capture_next_line and current_word and line.strip():
            # This should be the phoneme line
            phoneme = line.strip()
            # if current_word not in phoneme_dict:
            if phoneme not in phoneme_dict:
                phoneme_dict[current_word] = phoneme.split(" ")
                print(f"Added: {current_word} -> {phoneme}")
            current_word = None
            capture_next_line = False

    return phoneme_dict


def sanity_check(phoneme_dict):
    i = 1
    for k, phs in phoneme_dict.items():
        if type(phs) != list:
            print(f"{i}. [Bad Transcription] {k} -> {phs}")
        for ph in phs:
            if ph not in arpabet_phonemes:
                print(f"{i}. [Bad Transcription] {k} -> {phs}")
                i += 1
                break


if __name__ == "__main__":
    "l'arte -> l - o n t e   - >   L   O W   N   T   E Y"
    with open("phoneme_update_logs.txt", "r", encoding="utf-8") as f:
        log_contents = f.read()
    word2phoneme_dict_path = "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria Dataset/word2phonemes.pickle"
    with open(word2phoneme_dict_path, 'rb') as file:
        word2phoneme_dict = pickle.load(file)
    sanity_check(word2phoneme_dict)
    # phoneme_mapping = extract_manual_phonemes(log_contents, word2phoneme_dict)
    # word2phoneme_dict["douphol"] = ['D', 'UW', 'F', 'AO', 'L']
    # word2phoneme_dict["l'"] = ['L']
    # with open(word2phoneme_dict_path, 'wb') as file:
    #     pickle.dump(word2phoneme_dict, file)
    # print("Saved updated word2phonemes dictionary.")
    # Optionally, print final dict
    # print(phoneme_mapping)
