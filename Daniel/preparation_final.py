import numpy as np
import librosa


def extract_spectrum(file_name, file_length=5, bin_factor=4, **kwargs):
    """
    file_length is the target time length of the file in seconds
    bin_factor is the amount by which we enlarge the time bins from 512 samples:
    Extract mel spectrogram from audio file `file_name`
    """

    X, sample_rate = librosa.core.load(file_name)
    target_name = file_name[:-4]
    target_length = int(file_length * sample_rate)
    target = np.zeros(target_length)
    if X.shape[0] >= target_length:
        target = X[:target_length]
    else:
        target[:X.shape[0]] = X
    X = target
    mel = librosa.feature.melspectrogram(X, sr=sample_rate, hop_length=512 * bin_factor).T
    print(mel.shape)
    np.save(target_name, mel)


if __name__ == "__main__":
    extract_spectrum(".\\rear_right.wav")
    print("All tests passed")
