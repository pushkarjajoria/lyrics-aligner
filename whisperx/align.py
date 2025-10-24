import os
import pandas as pd
from tqdm import tqdm
import whisperx

device = "cuda"  # or "cpu"
output_dir = "/nethome/pjajoria/Github/lyrics-aligner/results/whisperx_sepa_vocals"


def align(audio_path: str, text_line: str, name: str) -> None:
    # 1. Load audio
    audio = whisperx.load_audio(audio_path)
    duration_sec = len(audio) / 16000.0

    # 2. Wrap your lyrics in a segment-like dict
    # Replace with your full lyrics text
    segments = [
        {
            "id": 0,
            "seek": 0,
            "start": 0.0,
            "end": duration_sec,
            "text": text_line
        }
    ]

    # 3. Load alignment model
    align_model, metadata = whisperx.load_align_model(language_code="it", device=device)

    # 4. Run alignment
    result = whisperx.align(
        segments,        # list of segments
        align_model,
        metadata,
        audio,
        device,
        return_char_alignments=False
    )

    # # 5. Save alignment
    # import os
    # os.makedirs(output_dir, exist_ok=True)
    # with open(f"{output_dir}/alignment.json", "w") as f:
    #     json.dump(result, f, indent=2)

    # 6. Optional: convert to CSV
    import csv
    with open(f"{output_dir}/{name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "start"])
        for seg in result["segments"]:
            for word in seg["words"]:
                writer.writerow([word["word"], word["start"]])

    print(f"Alignment saved for {name}")


if __name__ == "__main__":
    dataset_path = "/nethome/pjajoria/Github/lyrics-aligner/dataset/Aria_Dataset"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Collect only valid aria directories
    arias = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    num_arias = len(arias)

    # Confirm total count
    print(f"Found {num_arias} aria directories.")
    assert num_arias == 24, f"Expected 24 arias, but found {num_arias}."

    # Add progress bar
    for aria in tqdm(arias, total=24, desc="Aligning arias", ncols=80):
        aria_dir = os.path.join(dataset_path, aria)
        audio_path = os.path.join(aria_dir, "separated_vocals", f"{aria}_vocals.wav")
        labels_path = os.path.join(aria_dir, "labels.tsv")

        # Skip if files are missing
        if not os.path.isfile(audio_path) or not os.path.isfile(labels_path):
            print(f"Skipping {aria}: missing audio or labels.")
            continue

        # Load labels and build lyrics text
        labels = pd.read_csv(labels_path, sep="\t")
        words = labels["Text"]
        lyrics_text = " ".join(words.astype(str))

        # Run alignment
        align(audio_path, lyrics_text, aria)
