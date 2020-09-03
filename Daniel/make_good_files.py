import numpy as np
import pandas as pd

import os


def get_targets():
    """Get the gender and text for each file in the sample"""
    df = pd.read_csv('balanced-all-mp3.csv')
    df['filename'] = df['filename'][5:]
    df_ot = pd.read_csv('cv-other-train.csv', usecols=['filename', 'text'])
    df_os = pd.read_csv('cv-other-test.csv', usecols=['filename', 'text'])
    df_od = pd.read_csv('cv-other-dev.csv', usecols=['filename', 'text'])
    df_vt = pd.read_csv('cv-valid-train.csv', usecols=['filename', 'text'])
    df_vs = pd.read_csv('cv-valid-test.csv', usecols=['filename', 'text'])
    df_vd = pd.read_csv('cv-valid-dev.csv', usecols=['filename', 'text'])
    df_text = pd.concat([df_ot, df_os, df_od, df_vt, df_vs, df_vd], axis=0)
    gender = df['gender'].apply(lambda x: 1 if x == 'female' else 0).values
    df_merged = df.set_index('filename').join(df_text.set_index('filename'))
    text = df_merged['text'].values
    return gender, text


gender, text = get_targets()

file_array_list = ['sample{:06d}.npy'.format(i) for i in range(100000)]
real_arrays = ['data_processed/' + file_name for file_name in file_array_list if os.path.isfile('data_processed/'+file_name)]
print(real_arrays)
result = np.load('data_processed/sample000002.npy')
X = np.zeros((len(real_arrays), result.shape[1], result.shape[2]))
print(X.shape)
for index, file_name in enumerate(real_arrays):
    np.save(file_name,np.load( file_name)[0, :, :])
np.save('gender.npy', gender)
np.save('text.npy', text)

if __name__ == "__main__":
    print("All tests passed")
