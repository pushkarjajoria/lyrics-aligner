import csv
import os
import pickle
from typing import List, Optional, Tuple
import textgrid
from textgrid import TextGrid, IntervalTier

from util import clean_words, is_compound_word, subdivide, resolve_conflicts, create_lyrics_from_labels, create_tsv_file


def get_word_tuples_from_tg(textgrid_filepath):
    """

    Args:
        textgrid_filepath:

    Returns: Word tuple is a list of tuples (word_str, start_time, end_time) which are the labels for a text grid file.

    """
    word_labels = []
    tg = textgrid.TextGrid.fromFile(textgrid_filepath)
    for tier in tg:
        for interval in tier:
            text = interval.mark
            start_time = interval.minTime
            end_time = interval.maxTime
            text = clean_words(text)
            if is_compound_word(text):
                # Equally divide the interval for each word in the compound word
                subdivisions = subdivide(text, start_time, end_time)
                for w, s, e in subdivisions:
                    word_labels.append((w, s, e))
            else:
                text = text.replace(" ", "")
                if not text:
                    print(f"Empty annotation.")
                    continue
                word_labels.append((text, start_time, end_time))
    return word_labels


def create_labels_from_textgrid(textgrid_filepath):
    word_tuples = get_word_tuples_from_tg(textgrid_filepath)
    word_tuples = sorted(word_tuples, key=lambda x: x[1])
    resolved_word_tuples = resolve_conflicts(word_tuples)
    final_labels = list(map(lambda x: (clean_words(x[0]), round(x[1], 2), round(x[2], 2)), resolved_word_tuples))
    return final_labels


def create_labels_from_multiple_textgrid(textgrid_filepath_arr):
    final_labels = []
    for textgrid_filepath in textgrid_filepath_arr:
        part_labels = create_labels_from_textgrid(textgrid_filepath)
        final_labels += part_labels
    final_labels = sorted(final_labels, key=lambda x: x[1])
    return final_labels


def create_textgrid(word_tuples, tier_name='words'):
    # Create an empty TextGrid
    grid = TextGrid()

    # Calculate the max end time to set the TextGrid maxTime
    max_end_time = max(word_tuples, key=lambda x: x[2])[2]
    grid.maxTime = max_end_time

    # Create an IntervalTier
    tier = IntervalTier(name=tier_name, maxTime=max_end_time)

    # Add each word to the IntervalTier
    for word, start_time, end_time in word_tuples:
        tier.add(start_time, end_time, word)

    # Add the IntervalTier to the TextGrid
    grid.append(tier)

    return grid


def combine_textgrid_files_and_return_labels(file_list):
    word_labels = []
    for i, file_path in enumerate(file_list):
        tg = textgrid.TextGrid.fromFile(file_path)
        for tier in tg:
            for interval in tier:
                text = interval.mark
                start_time = interval.minTime
                end_time = interval.maxTime
                if is_compound_word(text):
                    # Equally divide the interval for each word in the compound word
                    subdivisions = subdivide(text, start_time, end_time)
                    for w, s, e in subdivisions:
                        word_labels.append((w, s, e))
                else:
                    text = text.replace(" ", "")
                    if not text:
                        print(f"Empty annotation.")
                        continue
                    word_labels.append((text, start_time, end_time))

    return word_labels


def _word_timestamps_from_phoneme_timestamps(phoneme_onset, word2phoneme, lyrics) -> List[tuple]:
    """
    Args:
        phoneme_onset: List of phoneme onset tuples. List[(ARPABET PHONEME, time in float seconds)]
        word2phoneme: word to corresponding ARPAbet phoneme dictionary
        lyrics: song lyrics as a list of words

    Returns: List[(str, float, float)]

    """
    phoneme_idx = 0
    word_timestamps = []
    for word in lyrics:
        phonemes_in_word = word2phoneme[word].split(" ")
        start_time = -1
        while phonemes_in_word:
            curr_phoneme = phonemes_in_word.pop(0)
            # TODO: Bug somewhere here, the pointers are not moving correctly. Check the phoneme model output file.
            while curr_phoneme != phoneme_onset[phoneme_idx][0]:
                phoneme_idx += 1
            if start_time == -1:
                start_time = phoneme_onset[phoneme_idx][1]
        phoneme_idx += 1
        end_time = phoneme_onset[phoneme_idx][1]
        word_timestamps.append((word, start_time, end_time))
    return word_timestamps


def _model_output_from_files(filepath: str, w2p_dict_file_path, lyrics_file_path) -> List[tuple]:
    """
    Returns:
        object: List[(str, float, float)]
    """
    with open(filepath, "r") as handle:
        phoneme_timestamps = [line.rstrip() for line in handle]
    phoneme_timestamps = list(map(lambda x: tuple(x.split('\t')), phoneme_timestamps))
    phoneme_onset = list(map(lambda x: (x[0], float(x[1])), phoneme_timestamps))

    with open(w2p_dict_file_path, "rb") as handle:
        word2phoneme = pickle.load(handle)

    with open(lyrics_file_path, "r") as handle:
        lyrics = [line.rstrip() for line in handle]
    lyrics = list(map(lambda x: x.split(" "), lyrics))
    lyrics = [word for line in lyrics for word in line]  # Creating a list of words from lyrics file
    lyrics = list(map(clean_words, lyrics))  # Removing unwanted symbols
    lyrics = list(filter(lambda x: x, lyrics))  # Removing Nones

    word_timestamps = _word_timestamps_from_phoneme_timestamps(phoneme_onset, word2phoneme, lyrics)
    return word_timestamps


def create_textgrid_file_from_model_output(filepath: str,
                                           word_timestamps: Optional[List[tuple]] = None,
                                           model_phoneme_output_file: Optional[str] = None,
                                           w2p_dict_file_path: Optional[str] = None,
                                           lyrics_file_path: Optional[str] = None) -> None:
    """

    Args:
        filepath:
        word_timestamps:
        model_phoneme_output_file:
        w2p_dict_file_path:
        lyrics_file_path:

    Returns:

    """
    WORD, WORD_START_TIME, WORD_END_TIME, LAST_ENTRY = 0, 1, 2, -1
    if not word_timestamps:
        if not model_phoneme_output_file or not w2p_dict_file_path or not lyrics_file_path:
            raise FileNotFoundError("Provide the location of files which contains the model phoneme output, "
                                    "lyrics and word to phoneme dictionary ")
        word_timestamps = _model_output_from_files(model_phoneme_output_file, w2p_dict_file_path, lyrics_file_path)
    max_time = word_timestamps[LAST_ENTRY][WORD_END_TIME]
    tg = textgrid.TextGrid(name=None,
                           minTime=0.0,
                           maxTime=max_time)
    model_output_tier = textgrid.IntervalTier(name="Standard Voice 1", minTime=0.0, maxTime=max_time)
    for word, start_time, end_time in word_timestamps:
        interval = textgrid.Interval(minTime=start_time, maxTime=end_time, mark=word)
        model_output_tier.addInterval(interval)
    tg.append(tier=model_output_tier)
    with open(filepath, 'w') as f:
        tg.write(f)
    print(f"Text grid file created at {filepath}")


def create_textgrid_file_from_model_output_resume(filepath: str, ass_obj,
                                                  word_timestamps: Optional[List[tuple]] = None,
                                                  model_phoneme_output_file: Optional[str] = None,
                                                  w2p_dict_file_path: Optional[str] = None,
                                                  lyrics_file_path: Optional[str] = None) -> None:
    """

    Args:
        filepath:
        word_timestamps:
        model_phoneme_output_file:
        w2p_dict_file_path:
        lyrics_file_path:

    Returns:

    """
    WORD, WORD_START_TIME, WORD_END_TIME, LAST_ENTRY = 0, 1, 2, -1
    if not word_timestamps:
        if not model_phoneme_output_file or not w2p_dict_file_path or not lyrics_file_path:
            raise FileNotFoundError("Provide the location of files which contains the model phoneme output, "
                                    "lyrics and word to phoneme dictionary ")
        word_timestamps = _model_output_from_files(model_phoneme_output_file, w2p_dict_file_path, lyrics_file_path)
    max_time = word_timestamps[LAST_ENTRY][WORD_END_TIME]
    tg = textgrid.TextGrid(name=None,
                           minTime=0.0,
                           maxTime=max_time)
    model_output_tier = textgrid.IntervalTier(name="Standard Voice 1", minTime=0.0, maxTime=max_time)
    aegi_sub_lines = ass_obj.events._lines
    prev_max = 0.0
    for i, (word, start_time, end_time) in enumerate(word_timestamps):
        aegi_sub_dialogue = aegi_sub_lines[i]
        if int(aegi_sub_dialogue.start.total_seconds()) < 100:
            start_time = aegi_sub_dialogue.start.total_seconds()
            end_time = aegi_sub_dialogue.end.total_seconds()
        prev_max = max(end_time, prev_max)
        interval = textgrid.Interval(minTime=start_time, maxTime=end_time, mark=word)
        try:
            model_output_tier.addInterval(interval)
        except ValueError as e:
            print(prev_max)
            print(interval.maxTime)
            print(interval.maxTime < prev_max)
            if interval.maxTime < prev_max:
                interval.maxTime = prev_max + 0.5
            interval.minTime = prev_max + 0.1
            model_output_tier.addInterval(interval)

    tg.append(tier=model_output_tier)
    with open(filepath, 'w') as f:
        tg.write(f)
    print(f"Text grid file created at {filepath}")


def collect_textgrid_files(textgrid_dir):
    files = {}
    datapoints_found = set()

    # Get all immediate subdirectories (datapoint folders)
    for entry in os.listdir(textgrid_dir):
        entry_path = os.path.join(textgrid_dir, entry)
        if os.path.isdir(entry_path):
            datapoints_found.add(entry)

    # Recursively find .TextGrid files
    for root, dirs, filenames in os.walk(textgrid_dir):
        for filename in filenames:
            if filename.endswith(".TextGrid"):
                full_path = os.path.join(root, filename)
                # The top-level folder name is the first part of rel_path
                rel_path = os.path.relpath(full_path, textgrid_dir)
                datapoint = rel_path.split(os.sep)[0]

                if datapoint not in files:
                    files[datapoint] = []
                files[datapoint].append(full_path)

    # Report any datapoint folders without a .TextGrid
    for datapoint in sorted(datapoints_found):
        if datapoint not in files:
            print(f"[ERROR] No .TextGrid file found for datapoint '{datapoint}'")
            files[datapoint] = []

    return files


def load_labels_tsv(tsv_path):
    labels = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                label = row['Text']
                start = float(row['Start Time'])
                end = float(row['End Time'])
                labels.append((label, start, end))
            except KeyError:
                raise ValueError(f"Missing expected headers in {tsv_path}. Required: 'label', 'start', 'end'")
    return labels


# if __name__ == "__main__":
#     """
#     Single Textgrid file for a single folder.
#     """
#     textgrid_files = ["../dataset/casta_diva/Casta diva_Norma.TextGrid"]
#     for tg_file_path in textgrid_files:
#         aria_folder = os.path.dirname(tg_file_path)
#         labels = create_labels_from_textgrid(tg_file_path)
#         # Save labels in tsv
#         # Generate filepath based on Dataset structure.
#         filepath = aria_folder + "/labels.tsv"
#         create_tsv_file(labels, filepath)
#
#         # Creating lyrics from labels.
#         lyrics_filepath = aria_folder + "/text/song.txt"    # As per the dataset structure
#         # Save lyrics in text file as per Dataset structure.
#         list_of_words = list(map(lambda x: x[0], labels))
#         lyrics = create_lyrics_from_labels(list_of_words, lyrics_filepath)


# if __name__ == "__main__":
#     """
#     Multiple textgrid files for a single folder
#     """
#     textgrid_parts = ["/Users/unknown_namejajoria/Desktop/Aria data prep/pari_siamo/Rigoletto_PariSiamo_0_212.TextGrid",
#                       "/Users/unknown_namejajoria/Desktop/Aria data prep/pari_siamo/Rigoletto_PariSiamo_213_240.TextGrid"]
#     labels = create_labels_from_multiple_textgrid(textgrid_parts)
#     aria_folder = os.path.dirname(textgrid_parts[0])
#     # Save labels in tsv
#     # Generate filepath based on Dataset structure.
#     filepath = aria_folder + "/labels.tsv"
#     create_tsv_file(labels, filepath)
#
#     # Creating lyrics from labels.
#     lyrics_filepath = aria_folder + "/text/song.txt"  # As per the dataset structure
#     # Save lyrics in text file as per Dataset structure.
#     list_of_words = list(map(lambda x: x[0], labels))
#     lyrics = create_lyrics_from_labels(list_of_words, lyrics_filepath)

# if __name__ == "__main__":
#     textgrid_dir = "/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria Dataset"
#     files = collect_textgrid_files(textgrid_dir)
#
#     all_labels = {}
#     for datapoint, paths in files.items():
#         if len(paths) == 0:
#             # Load from labels.tsv if present
#             tsv_path = os.path.join(textgrid_dir, datapoint, "labels.tsv")
#             if os.path.exists(tsv_path):
#                 labels = load_labels_tsv(tsv_path)
#                 print(f"[INFO] Loaded labels.tsv for '{datapoint}' with {len(labels)} entries.")
#             else:
#                 raise FileNotFoundError(f"No TextGrid or labels.tsv found for '{datapoint}'")
#         elif len(paths) == 1:
#             labels = create_labels_from_textgrid(paths[0])
#         elif len(paths) == 2:
#             labels = create_labels_from_multiple_textgrid(paths)
#             # labels = None   # Max time bug with the split Pari siamo TG files
#         else:
#             raise ValueError(f"Unexpected number of datapoints: {len(paths)}")
#         all_labels[datapoint] = labels
#
#     with open(textgrid_dir + "/processed_dataset.pickle", "wb") as f:
#         pickle.dump(all_labels, f)
#     print(f"Saved a total of {len(all_labels.items())} datapoints.")


if __name__ == "__main__":
    base_dir = "/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria Dataset"
    pickle_path = os.path.join(base_dir, "processed_dataset.pickle")

    # 1. Load the processed labels dict: datapoint -> List[Tuple[word, start, end]]
    with open(pickle_path, "rb") as f:
        all_labels: dict[str, List[Tuple[str, float, float]]] = pickle.load(f)

    # 2. Iterate over each datapoint
    for datapoint, labels in all_labels.items():
        if not labels:
            raise FileNotFoundError(f"{datapoint} does not have any labels stored in the pickle file")
        dp_folder = os.path.join(base_dir, datapoint)

        # a) Prepare the text/ folder
        text_folder = os.path.join(dp_folder, "text")
        os.makedirs(text_folder, exist_ok=True)

        # b) Extract just the words, in order
        words = [word for word, start, end in labels]

        # c) Write song.txt
        song_txt_path = os.path.join(text_folder, "song.txt")
        create_lyrics_from_labels(words, song_txt_path)

        # d) Write labels.tsv
        tsv_path = os.path.join(dp_folder, "labels.tsv")
        with open(tsv_path, "w", encoding='utf-8') as tsv:
            # Header
            tsv.write("Text\tStart Time\tEnd Time\n")
            # One row per word
            for word, start, end in labels:
                tsv.write(f"{word}\t{start}\t{end}\n")

        print(f"[OK] Wrote text/song.txt and labels.tsv for '{datapoint}'")
