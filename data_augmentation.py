import datetime

import random
from pathlib import Path
import torchaudio
import torchaudio.transforms as T
import torchaudio.functional as F
import librosa
import torch
# Code from Badr's repo https://github.com/badrex/arabic-dialect-identification/blob/main/data_augmentation/apply_data_augmentations.py

# specify directories for audio that simulate room impulse responses (RIRs)
# Download the dataset from https://www.openslr.org/28/
rir_dirs = [
    "/data/corpora/RIRS_NOISES/pointsource_noises",
    "/data/corpora/RIRS_NOISES/real_rirs_isotropic_noises"
]

# get paths for RIR wav files
RIR_FILES = []

RIR_FILES.extend(
    str(p)
    for rir_dir in rir_dirs
    for p in list(Path(rir_dir).rglob("*.wav"))
)

print(f"Num of RIR files :{len(RIR_FILES)}")


def pad_to_match(tensor: torch.Tensor, target_tensor: torch.Tensor) -> torch.Tensor:
    """
    Pad a 1D tensor with zeros at the end to match the size of target_tensor.
    """
    assert tensor.dim() == 1 and target_tensor.dim() == 1, "Both tensors must be 1D"

    target_len = target_tensor.size(0)
    curr_len = tensor.size(0)

    if curr_len >= target_len:
        return tensor[:target_len]  # truncate if necessary
    else:
        pad_size = target_len - curr_len
        padding = torch.zeros(pad_size, dtype=tensor.dtype, device=tensor.device)
        return torch.cat([tensor, padding], dim=0)


def create_spectrogram(waveform, power=1.0):
    """
    Create spectrogram from waveform
    """
    spectrogram = T.Spectrogram(
        n_fft=400,
        win_length=None,
        hop_length=None,
        center=True,
        pad_mode="reflect",
        power=power
    )
    return spectrogram(waveform)


def reconstruct_waveform(spec, rate=16000):
    """
    Convert spectrogram back to audio waveform
    """
    # Convert complex spectrogram to magnitude spectrogram for GriffinLim
    if torch.is_complex(spec):
        spec = torch.abs(spec)

    griffin_lim = T.GriffinLim(
        n_fft=400,
        n_iter=32,
        win_length=None,
        hop_length=None,
        power=1.0  # Important: use power=1.0 with magnitude spectrogram
    )

    # Reconstruct audio
    waveform = griffin_lim(spec)
    return waveform


def mask_frequency(waveform, freq_mask_param=160):
    """
    Apply frequency masking to spectrogram
    """
    # set random seed
    torch.random.manual_seed(42)

    # 1. Load and process audio
    # waveform, _ = process_audio_file(audio_path)

    # 2. Create complex spectrogram
    spec = create_spectrogram(waveform)

    # 3. Apply frequency masking
    freq_masking = T.FrequencyMasking(freq_mask_param)

    # 4. Apply mask
    freq_masked_spec = freq_masking(spec)
    freq_masked_waveform = reconstruct_waveform(freq_masked_spec)

    # 5. Make both waveforms of the same size by padding with 0s
    freq_masked_waveform = pad_to_match(freq_masked_waveform, waveform)

    return freq_masked_waveform


def mask_time(waveform, time_mask_param=80):
    """
    Apply time masking to spectrogram
    """
    # set random seed
    torch.random.manual_seed(42)

    # 1. Load and process audio
    # waveform, _ = process_audio_file(audio_path)

    # 2. Create complex spectrogram
    spec = create_spectrogram(waveform)

    # 3. Apply time masking
    time_masking = T.TimeMasking(time_mask_param)

    # 4. Apply mask
    time_masked_spec = time_masking(spec)
    time_masked_wave = reconstruct_waveform(time_masked_spec)

    # 5. Make both waveforms of the same size by padding with 0s
    time_masked_wave = pad_to_match(time_masked_wave, waveform)

    # 5. Convert to waveform and return
    return time_masked_wave


def additive_noise(waveform, noise_param=0.01):
    """Add Gaussian white noise to the audio signal."""
    # Suppose `waveform` is your 1D audio tensor
    length = waveform.size(0)

    # Generate standard Gaussian noise
    noise = torch.randn(length, dtype=waveform.dtype, device=waveform.device)

    # Optionally scale it to a desired standard deviation
    std = noise_param
    noise = noise * std
    noised = waveform + noise_param * noise
    # Normalize to prevent clipping
    noised = torch.clip(noised, -1.0, 1.0)
    return noised


def pitch_shift(waveform, pitch_shift_param):
    """
    Apply pitch shifting to audio
    """
    # 1. Load and process audio
    # waveform, _ = process_audio_file(audio_path)

    # 2. Apply pitch shifting
    pitch_shift = T.PitchShift(sample_rate=16000, n_steps=pitch_shift_param)

    # 3. Apply pitch shift
    with torch.no_grad():
        shifted_waveform = pitch_shift(waveform)

    # 4. Make both waveforms of the same size by padding with 0s
    shifted_waveform = pad_to_match(shifted_waveform, waveform)
    return shifted_waveform


def apply_rir(waveform):
    """
    Given an audio and RIR, apply room impulse response to audio
    """
    # 1. Load and process audio
    # waveform, _ = process_audio_file(audio_path)

    # print(audio_path, rir_path)

    # this was a quick and dirty solution around the issue of
    # some RIR files not being loaded, it is not the best solution
    # TODO: find a better solution, and even better, prevent the issue
    it_works = False

    while not it_works:
        # 2. Sample a RIR wav
        rir_path = random.choice(RIR_FILES)

        try:
            # 3. Load and process RIR with specific parameters
            rir_raw, sample_rate = torchaudio.load(
                rir_path,
                normalize=True,  # Normalize the audio
                channels_first=True,  # Ensure channels are first
            )
            rir_raw_mono = torch.mean(rir_raw, dim=0, keepdim=True).squeeze()
            rir = rir_raw_mono[int(sample_rate * 1.01):int(sample_rate * 1.3)]
            if torch.min(rir) < 0 and torch.max(rir) > 0.0:
                it_works = True

        except RuntimeError as e:
            # print("Error loading RIR file: ", rir_path)
            # print(e)
            # print("Trying another RIR file ...")
            # try another RIR file
            it_works = False

    # Process RIR
    rir = rir / torch.linalg.vector_norm(rir, ord=2)

    # Apply convolution
    augmented = F.fftconvolve(waveform, rir)

    augmented = pad_to_match(augmented, waveform)
    return augmented


if __name__ == "__main__":
    PITCH_SHIFT_STEPS = [-8, -6, -4, -2, 2, 4, 6, 8]
    # Load an audio file

    y, sr = torchaudio.load("/nethome/unknown_user/Github/lyrics-aligner/dataset/Aria_Dataset/Bellini_Puritani_Suoni_la_tromba/audio/song.mp3")
    resampler = T.Resample(sr, 16000)
    start = datetime.datetime.now()
    audio = resampler(y)
    end = datetime.datetime.now()
    print(end - start)
    # Convert to mono by averaging the channels
    if y.shape[0] > 1:  # more than 1 channel
        y = torch.mean(y, dim=0, keepdim=True).squeeze()
    y_1 = pitch_shift(y, random.choice(PITCH_SHIFT_STEPS))
    y_2 = additive_noise(y)
    y_3 = mask_frequency(y)
    y_4 = apply_rir(y)
    print("Done")
