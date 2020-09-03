import glob
import os
import pandas as pd
import numpy as np
import shutil
import librosa
from tqdm import tqdm


def extract_feature_uniform(file_name, file_length=5, **kwargs):
    """
    file_length is the target time length of the file
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    X, sample_rate = librosa.core.load(file_name)
    target = np.zeros(file_length * sample_rate)
    if X.shape[0] >= file_length * sample_rate:
        target = X[:file_length * sample_rate]
    else:
        target[:X.shape[0]] = X
    X = target
    if chroma or contrast:
        stft = np.abs(librosa.stft(X))
    result = []
    if mfcc:
        mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T
        result.append(mfccs)
    if chroma:
        chroma = librosa.feature.chroma_stft(S=stft, sr=sample_rate).T
        result.append(chroma)
    if mel:
        mel = librosa.feature.melspectrogram(X, sr=sample_rate).T
        result.append(mel)
    if contrast:
        contrast = librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T
        result.append(contrast)
    if tonnetz:
        tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T
        result.append(tonnetz)
    return np.array(result)


dirname = "data_processed"

if not os.path.isdir(dirname):
    os.mkdir(dirname)

csv_files = glob.glob("*.csv")

for j, csv_file in enumerate(csv_files):
    print("[+] Preprocessing", csv_file)
    df = pd.read_csv(csv_file)
    # only take filename and gender columns
    new_df = df[["filename", "gender"]]
    print("Previously:", len(new_df), "rows")
    # take only male & female genders (i.e droping NaNs & 'other' gender)

    audio_files = df['filename'].values
    for i, audio_file in tqdm(list(enumerate(audio_files)), f"Extracting features of balanced dataset"):
        src_path = audio_file
        target_path = '{}/sample{:06d}.npy'.format(dirname, i)

        features = extract_feature_uniform(src_path, mel=True)
        np.save(target_path, features)

if __name__ == "__main__":
    print("All tests passed")

if __name__ == "__main__":
    print("All tests passed")
