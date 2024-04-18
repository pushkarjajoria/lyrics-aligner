# Finetuning phoneme level model trained on english pop music for Italian Arias.

This repo contains the code to fine-tune a phoneme level lyrics aligner on Italian arias. The contents of the initial repository can be found [here](https://github.com/schufo/lyrics-aligner).

We are fine tuning a part of the pretrained model that is described in the paper [Phoneme Level Lyrics Alignment and Text-Informed
Singing Voice Separation](https://telecom-paris.hal.science/hal-03255334/file/2021_Phoneme_level_lyrics_alignment_and_text-informed_singing_voice_separation.pdf).

## Dataset Structure

The dataset folder should be place in the root directory. Each subdirectory inside corresponds to a single aria d'opera. Each of this subdirectoy should contain the files needed to train the model:

- `di_quella_pira/` (or some other name corresponding to any aria d'opera):
  - `word2phonemes.pickle`: A pickle file that contains mappings from words to their phonetic representations 
  using ARPAbet. This is generated from the tsv file containing the transcriptions 
  (For example: _casta_diva/norma_transcription.tsv_) and running the script `make_word2phoneme_dict.py`.
  - `labels.tsv`: A tab-separated values file that includes labels or annotations. It maps the lyrics to its start and end time in the audio file. See `scripts/textgrid_processing.py` for generating the tsv file from textgrid files.

- `audio/`:
  - `song.mp3`: An audio file in MP3 format that contains the recording of the song or aria used in the project. This is provided as part of the dataset. The name should be `song.mp3`.

- `text/`:
  - `song.txt`: A text file that contains the lyrics or text of the song or aria included in the project. This is generated as part of the script `scripts/textgrid_processing.py` by using the text provided in the textgrid file.

Each subdirecty in the dataset folder contains everything required to run that particular aria through the model.

## Training

The script `train_on_hpc` contains the code run this code on the ichec hpc. It can be slightly modified for running it on another machine. Run `sh train_on_hpc.sh --help` to look at the usage along with their default values.

The file `train.py` contains all the training code. It also has a function named `forward_sanity_test` which runs a single forward pass over the full dataset to ensure everything is in order before running the main training loop.

The file `model.py` contains the PyTorch model. The model class `InformedOpenUnmix3` is similar to original code provided by the author of the paper mentioned above. The changes are in the forward method where instead of performing voice seperate, we stop at the alignment.

The file `datahandler.py` contains all the code which creates the `torch.data.Dataset` from directory structure described above. Inside this file, you'll find a function named `words_to_phonemes()` which tries to map each word to its corresponding ARPAbet pronunciation. Incase such a word is not found in the `word2phonemeglobal.pickle` dict, it prints the closests 5 words in the dict and asks the user to add the transcription for that word manually.
This file also has the functions which convert word level labels into phoneme level labels required for computing the loss. Look at `get_phonemes_in_intervals()` and `phoneme_to_stft_frame()` to understand more about this.

