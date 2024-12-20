import torch
import torchaudio
import torchaudio.functional as F
import torchaudio.transforms as T
import pandas as pd
import librosa

import base64
from io import BytesIO
from matplotlib.figure import Figure
import numpy as np

from matplotlib.colors import Normalize
from matplotlib import colormaps
import matplotlib.pyplot as plt

class AudioFeatures():

    def __init__(self, file="app/static/datasets/RAVDESS/audio/Actor_05/03-01-05-01-01-01-05.wav", id=0):
        
        self.wav, self.sr = torchaudio.load(file)
        self.fig = Figure()
        self.id = id
        self.n_mels = 128
        self.n_mfcc = 40
        self.filtered_df = self.load_initial_data()
        self.full_df = pd.DataFrame()

    def load_initial_data(self):
        np_path = f'app/static/datasets/RAVDESS/features/mfcc/ravdess_{self.n_mels}_{self.n_mfcc}.npy'
        ds = np.load(np_path, allow_pickle=True)
        return pd.DataFrame(ds,columns=['features','feature_viz','id'])




    def change_audio_file(self, sess):
        new_record = sess['records'][sess['curr_record']['record_index']]
        self.wav, self.sr = torchaudio.load(new_record[0])

    def change_group_audio_file(self, sess):
        record_index = sess['record_group_indices'][sess['curr_record']['group_index']]
        fp = sess['records'][record_index][0]
        self.wav, self.sr = torchaudio.load(fp)




    def get_spectrogram(self):
        spectro = T.Spectrogram(n_fft=2048,hop_length=128,)
        return spectro(self.wav)
    
    def get_mel_spectrogram(self,n_mels):
        mel_spectrogram = T.MelSpectrogram(sample_rate=self.sr,n_fft=2048,hop_length=128,
                        center=True,normalized=True,pad_mode="reflect",power=2.0,
                        norm="slaney",n_mels=n_mels,mel_scale="slaney",f_max = 8000,)
        return mel_spectrogram(self.wav)

    def get_mfcc(self, n_mels=128, n_mfcc=40):
        mfcc_transform = T.MFCC(sample_rate=self.sr,n_mfcc=n_mfcc, 
                        melkwargs={"n_fft": 2048,"n_mels": n_mels,
                                    "hop_length": 128,"mel_scale": "slaney",
                                    "center": True},)
        return mfcc_transform(self.wav) 
        


    def choose_npy_array(self, sess):
        self.n_mels= sess['filters']['num_mels']
        self.n_mfcc = sess['filters']['num_mfcc']

        np_path = f'app/static/datasets/RAVDESS/features/mfcc/ravdess_{self.n_mels}_{self.n_mfcc}.npy'
        ds = np.load(np_path, allow_pickle=True)
        self.full_df = pd.DataFrame(ds,columns=['features','feature_viz','id'])
        
        # feels like this should be a separate function
        self.full_df['label'] = self.full_df['id'].isin(sess['ids'])
        self.filtered_df = self.full_df[self.full_df['label']].copy()
        self.filtered_df.reset_index(inplace=True)

    def get_mfcc_from_npy(self, sess):
        id = sess['curr_record']['rec_id']
        df = self.filtered_df.loc[self.filtered_df['id'] == id]
        return torch.from_numpy(df['feature_viz'].iloc[0])

    def get_mfcc_group_from_npy(self, sess):
        mfccs =[]
        ids = []
        for i in sess['record_group_indices']:
            id = sess['records'][i][1]
            ids.append(id)
            print("id loop: ",id)
            df = self.filtered_df.loc[self.filtered_df['id'] == id]
            mfccs.append(torch.from_numpy(df['feature_viz'].iloc[0]))
        return mfccs, ids

    def get_features_and_labels(self):
        if 'label' in self.full_df.columns:
            features = np.vstack(self.full_df['features'])
            labels = np.array(self.full_df['label'])
            return features, labels        

    # move to aggregate plots
    def plot_waveform(self,title='waveform', ax=None):
        waveform = self.wav.numpy()

        num_channels, num_frames = waveform.shape
        time_axis = torch.arange(0, num_frames) / self.sr

        fig = Figure(figsize=(3,2.25))
        if ax is None:
            ax = fig.subplots(num_channels, 1)
        
        ax.plot(time_axis, waveform[0], linewidth=1)
        ax.grid(True)
        ax.set_xlim([0, time_axis[-1]])
        ax.set_title(title)
        ax.title.set_size(10)
        fig.tight_layout()
        return fig

    def plot_spectrogram(self,spectro,title=None, ylabel='Hz', ax=None):
        fig = Figure(figsize=(4,3))
        if ax is None:
            ax = fig.subplots()
        if title is not None:
            ax.set_title(title)
            ax.title.set_size(10)
        
        ax.set_ylabel(ylabel)
        return ax.imshow(librosa.power_to_db(spectro), origin="lower", aspect="auto", interpolation="nearest",cmap=colormaps['seismic'])


    def plot_mel(self,spectro,title=None, ylabel='Hz', ax=None):
        fig = Figure(figsize=(4,3))
        if ax is None:
            ax = fig.subplots()
        if title is not None:
            ax.set_title(title)
            ax.title.set_size(10)
      
        ax.set_ylabel(ylabel)
        return ax.imshow(librosa.power_to_db(spectro), origin="lower", aspect="auto", interpolation="nearest",cmap=colormaps['seismic'],norm=Normalize(vmin=-80,vmax=0))

    def plot_mfcc(self,mfcc, title=None, ylabel="frequency bin", ax=None):
        fig = Figure(figsize=(4,3))
        if ax is None:
            ax = fig.subplots(1, 1)
        if title is not None:
            ax.set_title(title)
            ax.title.set_size(10)
        ax.set_ylabel(ylabel)
        return ax.imshow(mfcc, origin="lower", aspect="auto",norm=Normalize(vmin=-30,vmax=30),cmap=colormaps['seismic'])
    


    

    # move to agg plots
    def fig_to_buf(self, fig):
        buf = BytesIO()
        fig.savefig(buf,format='png')
        buf.seek(0)
        return buf

    
       

    def get_audio_data(self):
        buf = BytesIO()
        torchaudio.save(buf, self.wav, self.sr, format="wav")
        buf.seek(0)
        
        return buf
    
