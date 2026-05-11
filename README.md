<!-- Badges -->
[![LREC 2026](https://img.shields.io/badge/LREC-2026%20accepted-2ea44f)](https://lrec2026.lrec-conf.org/)
[![Hugging Face Dataset](https://img.shields.io/badge/🤗%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/REPLACE_WITH_YOUR_ORG_AND_NAME)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

# Audio–Lyrics Alignment for Italian Opera Arias

Companion repository for *Audio–Lyrics Alignment Dataset for Italian Arias*, accepted at the **15th Language Resources and Evaluation Conference (LREC 2026)**, Palma de Mallorca.

We release the **first audio–lyrics alignment dataset for Italian opera arias** — 24 arias spanning Handel to Puccini, ~1h 53m of audio, hand-annotated with **word-level timestamps** and per-word ARPAbet phoneme strings. We use it to benchmark five state-of-the-art alignment systems and to test whether a small amount of in-domain data can adapt a popular-music aligner to opera. The short answer: **existing systems take a ~44% PCO hit when moving from pop to opera**, and few-shot fine-tuning helps locally but not globally — both findings are detailed below.

<p align="center">
  <img src="images/Logo-Universität_des_Saarlandes.svg.png" height="64" alt="Universität des Saarlandes">&nbsp;&nbsp;
  <img src="images/cafoscari_logo.png" height="64" alt="Università Ca' Foscari Venezia">&nbsp;&nbsp;
  <img src="images/UoG%20Logo.png" height="56" alt="University of Galway">&nbsp;&nbsp;
  <img src="images/Seal_of_the_University_of_Bologna.svg.png" height="64" alt="Alma Mater Studiorum – Università di Bologna">
</p>

---

## Contents

- [Why this dataset](#why-this-dataset)
- [Headline results](#headline-results)
- [The Aria Dataset](#the-aria-dataset)
- [Getting the data](#getting-the-data)
- [Quick start](#quick-start)
- [Reproducing the paper](#reproducing-the-paper)
- [Repository structure](#repository-structure)
- [Citation](#citation)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Maintainer notes](#maintainer-notes)

---

## Why this dataset

Most audio–lyrics alignment work targets **English pop**. Public datasets reflect that: MUSDB18, Jamendo, DALI are all dominated by pop/rock in mostly Germanic languages. Italian opera sits at the opposite end of the space — a **trained**, **stylised** vocal technique on a **century-old** lyrical register, with **archaic vocabulary**, frequent **apocope**, and orchestral accompaniment that crowds the vocal line. It is exactly the kind of corner where a model's training distribution should — and does — show its limits.

Two things make Italian arias a particularly interesting alignment problem:

1. **The voice is engineered, not natural.** Opera singing prioritises projection and timbre over text intelligibility — vowels are reshaped, consonants are softened, durations stretch with the music. Speech-trained acoustic models and pop-trained singing models both have to bridge this gap.
2. **The text is not modern Italian.** Words like *cor*, *core*, *desire*, *deggio*, *degg'io* require grapheme-to-phoneme rules that the standard Italian SPARSAR pipeline does not ship with. We build those rules and release the resulting ARPAbet transcription alongside the timings.

This release fills a concrete gap in the audio–lyrics alignment literature: a **non-pop, non-English, non-contemporary** benchmark with rigorously validated annotations.

---

## Benchmarking

We benchmark five alignment systems on the 24 arias — three music aligners (PLLA, LA-JPD, ALT) and two speech forced aligners (MMS-FA, WhisperX), with and without Spleeter-separated vocals (`SV`). Numbers are mean ± standard error across all 24 arias.

| Model | Multilingual | RMSE ↓ [s] | MAE ↓ [s] | MedAE ↓ [s] | PCO₀.₃ ↑ [%] |
|---|:---:|---:|---:|---:|---:|
| *Music alignment models* | | | | | |
| PLLA (Schulze-Forster et al., 2021) | ✗ | 25.24 ± 7.7 | 20.94 ± 6.7 | 18.36 ± 6.5 | 30.45 ± 5.8 |
| LA-JPD (Huang et al., 2022) | ✓ | **9.44 ± 3.1** | **6.14 ± 2.3** | **3.46 ± 1.4** | 52.98 ± 5.6 |
| ALT (Gupta et al., 2019) | ✗ | 18.49 ± 4.3 | 13.51 ± 3.7 | 9.58 ± 3.3 | 20.69 ± 3.5 |
| *Speech models* | | | | | |
| MMS-FA (Ashraf, 2024) | ✓ | 11.47 ± 3.2 | 7.45 ± 2.8 | 3.99 ± 2.1 | 55.43 ± 5.9 |
| MMS-FA-SV | ✓ | 11.26 ± 3.3 | 7.30 ± 2.8 | 3.98 ± 2.1 | **56.02 ± 6.0** |
| WhisperX (Bain et al., 2023) | ✓ | 39.43 ± 12.7 | 34.61 ± 12.1 | 33.37 ± 12.7 | 23.34 ± 4.4 |
| WhisperX-SV | ✓ | 41.35 ± 13.5 | 36.02 ± 12.6 | 34.64 ± 12.9 | 28.60 ± 5.7 |

**What we see:**

- For the **same model family**, PCO falls from **94% on Jamendo to ~53% on the arias** — a **~44% relative decline** (and roughly an 8× increase in gross errors with >0.3 s offset).
- **Multilingual training matters more than music-vs-speech.** Both top systems (LA-JPD, MMS-FA) saw Italian in their pretraining; the monolingual-English PLLA and ALT trail by 20–30 PCO points.
- **Vocal separation is uneven.** It helps WhisperX (+5 PCO) but is essentially a wash for MMS-FA.

We then ask: can a few in-domain arias close the gap? We fine-tune PLLA on a 17/7 train/test split (5 random folds, 15 epochs, LR 1e-5, gradient accumulation = 4) with pitch-shift, additive noise, reverb, and frequency-masking augmentation.

| Model | RMSE ↓ [s] | MAE ↓ [s] | MedAE ↓ [s] | PCO₀.₃ ↑ [%] |
|---|---:|---:|---:|---:|
| Baseline PLLA | 23.77 ± 3.0 | 19.95 ± 2.7 | 17.23 ± 2.3 | 26.38 ± 1.5 |
| **Fine-tuned PLLA (ours)** | **21.32 ± 3.3** | **17.44 ± 2.9** | **14.91 ± 2.3** | **27.37 ± 2.1** |

Gains are small in aggregate, but per-aria the picture is more nuanced — *Puccini, Turandot: "Nessun dorma"* improves substantially, while *Verdi, Rigoletto: "Caro nome"* gets worse at the boundaries. We read this as **localised adaptation without global feature learning**, which is the expected behaviour at this data scale.

![Benchmark RMSE](images/fig_benchmark_rmse.png)

![Few-shot gain](images/fig_fewshot_gain.png)

---

## The Aria Dataset

**24 arias, 1 hour 53 minutes**, mean duration 284 s (range 125–570 s). Selected by two musicologists (co-authors) to cover the operatic repertoire that has both institutional prominence and audience appeal, balanced across composers, registers, and vocal traditions.

| Composer | Operas | Arias | Period | Genre |
|---|---|:---:|---|---|
| Handel | *Giulio Cesare* | 6 | early 18th c. | opera seria |
| Mozart | *Le nozze di Figaro*, *Don Giovanni* | 4 | late 18th c. | opera buffa |
| Rossini | *Il barbiere di Siviglia* | 3 | early 19th c. | opera buffa |
| Bellini | *I Puritani*, *Norma* | 2 | early 19th c. | melodramma |
| Verdi | *Rigoletto*, *La Traviata*, *Il Trovatore* | 8 | mid-19th c. | melodramma |
| Puccini | *Turandot* | 1 | early 20th c. | melodramma |

**Annotation effort.** Praat TextGrids were prepared by a single annotator at roughly **1h 20m per minute of audio**, then validated and corrected by a musicologist — **~19 working days** total.

**Phonetic transcription.** Each word is also given an ARPAbet string (Italian variant from Arango et al., 2021 — 30 base phonemes + 20 geminates) produced via the Italian SPARSAR system (Delmonte, 2019). Because operatic Italian is **not** modern Italian, we extended SPARSAR with a specialised module covering:

- archaic lexemes (e.g. *conturba*, *desire*, *core*, *sparafucile*, *maledivami*),
- apocopated forms (e.g. *cor*, *quell*, *altr*, *poss*, *uom*, *amor*),
- contractions omitting *v*, *gl*, *i* (e.g. *godea*, *vedea*, *sentìa*, *dee*),
- and special cases requiring word-boundary-aware rules (notably *deggio* vs. *degg'io*, which differ in stress assignment and palatal-affricate formation).

**Sample annotation** — Bellini, *I puritani* (*Suoni la tromba*), from [`publication/word_align_csv/Bellini_Puritani_Suoni_la_tromba.csv`](publication/word_align_csv/Bellini_Puritani_Suoni_la_tromba.csv):

| Word | Start (s) | End (s) | ARPAbet |
|---|---:|---:|---|
| suoni | 2.24 | 3.17 | S W OW N IY |
| la | 3.27 | 3.37 | L AA |
| tromba | 3.47 | 4.04 | T R AO M B AA |
| e | 4.14 | 4.24 | EY |
| intrepido | 4.34 | 5.94 | IY N T R EH P IY D OW |
| io | 6.13 | 6.64 | IY OW |
| pugnerò | 6.74 | 7.53 | P UW N Y EY R OW |
| da | 7.63 | 8.01 | D AA |

---

## Getting the data

We ship **annotations** (timestamps + phonemes + lyrics) on Hugging Face. We **do not** redistribute audio — copyright on operatic recordings is performance-specific and we cannot license it. Instead, we provide the exact YouTube source mapping we annotated against, plus a download script that fetches and resamples to 16 kHz.

### 1. Annotations — Hugging Face

The dataset card on the Hub ships:

- **Per-aria CSVs** with columns `word`, `start_time`, `end_time`, `phonemes`
- `youtube_sources.tsv` — the source URL for each aria, with full third-party notice
- `download_audio.py` / `verify_audio.py` — helpers to reconstruct a local training tree
- The dataset summary CSV and the third-party audio notice

```bash
pip install datasets
```

```python
from datasets import load_dataset
ds = load_dataset("REPLACE_WITH_YOUR_ORG_AND_NAME")
```

> 📌 The HF URL will be set in the badge above once the dataset is published.

### 2. Audio — your responsibility, our script

Because the audio is third-party content, **you obtain it yourself** and accept the terms of the source platform.

```bash
python scripts/download_youtube_audio.py        # interactive consent
python scripts/download_youtube_audio.py --yes  # skip the prompt (CI/scripts)
```

The script prints the full third-party notice and requires an explicit `YES` before any download. After it finishes, the directory tree mirrors `dataset/Aria_Dataset/<AriaName>/audio/song.mp3`. You can then verify locally:

```bash
python scripts/verify_youtube_audio.py
```

which checks duration consistency and chroma cosine similarity against the annotated reference.

### 3. Local layout (what the code expects)

```text
dataset/Aria_Dataset/
├── <AriaName>/
│   ├── audio/song.mp3          # 16 kHz mono, single channel
│   ├── text/song.txt           # whitespace-tokenised lyrics, matches labels
│   └── labels.tsv              # columns: Text, Start Time, End Time
├── word2phonemes.pickle        # global word → ARPAbet[] lexicon
└── aria_dataset_summary.csv    # per-aria duration / sample-rate table
```

> ⚠️ Several folder names contain spaces (e.g. `Norma_Casta Diva`, `Rigoletto_Pari siamo`, `Traviata_Sempre libera`). Preserve them verbatim — the loaders match on exact folder names.

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/pushkarjajoria/lyrics-aligner.git
cd lyrics-aligner

# 2. Environment (pick one)
conda env create -f environment_gpu.yml   # GPU
conda env create -f environment_cpu.yml   # CPU

# 3. Get annotations + audio (see "Getting the data" above)

# 4. Sanity check the layout
pytest tests/test_lyrics_labels_consistency.py
```

For the few-shot fine-tuning experiments you'll additionally need the baseline weights at `checkpoint/base/model_parameters.pth` and `files/phoneme2idx.pickle` (see [§ Reproducing the paper](#reproducing-the-paper)).

---

## Reproducing the paper

### Table 4 — alignment benchmarks

All five benchmark entry points are Python modules under [`benchmarks/`](benchmarks/). From the repository root:

```bash
python -m benchmarks.benchmark_schufo
python -m benchmarks.benchmark_whisperx
python -m benchmarks.benchmark_gc
python -m benchmarks.benchmark_HBE
python -m benchmarks.benchmark_forced_aligner    # needs ctc_forced_aligner installed separately
```

See [`benchmarks/README.md`](benchmarks/README.md) for the per-script input/output layout and which paper system each module corresponds to. Each writes predictions and per-aria metrics under `benchmarks/results/`. **Frozen result pickles** are committed there so plot scripts (`box_plot.py`, `scatter_plot.py`, `overlaid_bar_plot.py`, …) work without re-running every system.

Metrics — RMSE, MAE, MedAE, PCO@0.3 — are computed in [`evaluate_helper.py`](evaluate_helper.py); the tolerance window is 300 ms by default.

### Table 5 — few-shot fine-tuning

```bash
python train.py --dataset_path dataset/Aria_Dataset --epochs 15
```

Run `python train.py --help` for the full flag list (learning rate, seed, augmentation toggles, save interval, etc.). Defaults resolve relative to [`repo_paths.py`](repo_paths.py); the script logs to Weights & Biases and saves per-fold checkpoints. The paper's setting is 17/7 train/test splits across **5 random seeds**, **15 epochs**, **LR = 1e-5**, and **gradient accumulation = 4** (we found per-step optimisation unstable on this data scale). Evaluation against the frozen baseline runs automatically at the end of each fold.

The data-augmentation stack (pitch shift, additive Gaussian noise, RIR reverb from OpenSLR, frequency masking) lives in [`data_augmentation.py`](data_augmentation.py); augmented samples are pickled and reused on subsequent epochs.

### Regenerating the per-aria CSVs

```bash
python scripts/export_aria_word_csvs.py --yes
```

This produces `publication/word_align_csv/<AriaName>.csv` from your local `labels.tsv` + `song.txt` + `word2phonemes.pickle`. Those CSVs are what get bundled and uploaded to Hugging Face.

---

## Repository structure

```
lyrics-aligner/
├── benchmarks/             # Benchmark entry points (one module per system)
│   ├── benchmark_*.py      # benchmark_schufo, benchmark_whisperx, benchmark_gc, …
│   ├── results/            # Frozen per-aria metrics and predictions
│   └── README.md           # Per-system input/output layout
├── scripts/                # Dataset packaging and YouTube tooling
│   ├── export_aria_word_csvs.py
│   ├── download_youtube_audio.py
│   ├── verify_youtube_audio.py
│   ├── build_hf_dataset_bundle.py
│   ├── ingest_youtube_docx.py
│   ├── validate_youtube_aria_mapping.py
│   └── textgrid_processing.py
├── hf_dataset_bundle/      # What gets uploaded to Hugging Face (regenerated)
├── publication/            # Word-level CSV exports + third-party notice
├── metadata/               # youtube_sources.tsv, ingest/validation reports
├── files/                  # phoneme2idx.pickle (tracked)
├── checkpoint/base/        # Baseline PLLA weights (not tracked)
├── tests/                  # Lyrics ↔ labels consistency check
├── images/                 # Figures and institution logos
├── train.py                # Few-shot fine-tuning entry point
├── model.py                # InformedOpenUnmix3 (PLLA architecture)
├── align.py                # Inference / phoneme-to-word onset logic
├── datahandler.py          # AriaDataset, sparse-alpha label construction
├── data_augmentation.py    # Pitch / noise / reverb / freq-mask
├── evaluate_helper.py      # RMSE / MAE / MedAE / PCO metrics
├── repo_paths.py           # Portable root resolution
└── requirements.txt
```

This repo is a **fork of [schufo/lyrics-aligner](https://github.com/schufo/lyrics-aligner)** (Schulze-Forster et al., TASLP 2021). The core alignment model (`model.py`, `align.py`, `make_word_list.py`, `make_word2phoneme_dict.py`) is upstream; the dataset, training pipeline, benchmark suite, and publication tooling are new.

---

## Citation

If you use this dataset or code, please cite:

```bibtex
@inproceedings{jajoria_2026_audio,
  author    = {Jajoria, Pushkar and Graciotti, Arianna and Casali, Giovanna and
               Alabi, Jesujoba O. and Delmonte, Rodolfo and Pompilio, Angelo and
               Tripodi, Rocco and McDermott, James and Klakow, Dietrich},
  title     = {Audio-Lyrics Alignment Dataset for Italian Arias},
  booktitle = {Proceedings of the 15th Language Resources and Evaluation
               Conference (LREC 2026)},
  year      = {2026},Gains are small in aggregate, but per-aria the picture is more nuanced — Puccini, Turandot: "Nessun dorma" improves substantially, while Verdi, Rigoletto: "Caro nome" gets worse at the boundaries. We read this as localised adaptation without global feature learning, which is the expected behaviour at this data scale.


  publisher = {ELRA Language Resources Association},
  address   = {Palma de Mallorca, Spain},
  month     = may,
}
```

If you use the underlying alignment model, please also cite Schulze-Forster et al.:

```bibtex
@article{schulze2021phoneme,
  author    = {Schulze-Forster, Kilian and Doire, Clement S. J. and
               Richard, Ga{\"e}l and Badeau, Roland},
  title     = {Phoneme Level Lyrics Alignment and Text-Informed Singing Voice Separation},
  journal   = {IEEE/ACM Transactions on Audio, Speech, and Language Processing},
  volume    = {29},
  pages     = {2382--2395},
  year      = {2021},
  doi       = {10.1109/TASLP.2021.3091817},
}
```

---

## Acknowledgements

Pushkar Jajoria was funded by the **Deutsche Forschungsgemeinschaft (DFG)** — Project-ID 232722074 — SFB 1102. This work was also supported by the **Polifonia Project** of the European Union's Horizon 2020 research and innovation programme under grant agreement No. 101004746.

We thank **Badr M. Abdullah** for guidance on the augmentation stack, and **Aravind Krishnan**, **Janaki Viswanathan**, and other members of the **LSV Lab at Saarland University** for feedback on the manuscript.

This repository builds on the open-source release of [schufo/lyrics-aligner](https://github.com/schufo/lyrics-aligner) by Schulze-Forster et al. We are grateful for the upstream work.

---

## License

The **code** in this repository is released under the [MIT License](LICENSE). The **annotations** released on Hugging Face are similarly permissively licensed (see the dataset card for the exact terms). **Audio** is not redistributed — see the third-party notice in `publication/THIRD_PARTY_AUDIO_NOTICE.md` and on the Hugging Face dataset card.

---

## Maintainer notes

<details>
<summary>Releasing a new version of the dataset on Hugging Face</summary>

1. Regenerate the bundle that gets uploaded:
   ```bash
   python scripts/export_aria_word_csvs.py --yes
   python scripts/build_hf_dataset_bundle.py
   ```
2. Authenticate once with `huggingface-cli login`, then upload from the repository root:
   ```bash
   huggingface-cli upload YOUR_ORG/YOUR_DATASET_NAME hf_dataset_bundle . --repo-type dataset
   ```
3. Update the badge URL at the top of this README.

</details>

<details>
<summary>Regenerating the YouTube source mapping from the working DOCX</summary>

```bash
python scripts/ingest_youtube_docx.py --docx "/path/to/0Arie_Music alignment Nov 2023.docx"
python scripts/validate_youtube_aria_mapping.py --write-report metadata/YOUTUBE_VALIDATION_REPORT.md
```

The ingest step writes `metadata/youtube_sources.tsv` and a Markdown report flagging unmatched rows. One historical DOC row ("La vendetta") does **not** correspond to any of the 24 LREC arias and is intentionally flagged in the report.

</details>