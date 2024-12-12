

from app.src.FeatureExtractors import AudioFeatures as af
from matplotlib.figure import Figure

class PlotAggregator():

    def __init__(self, af):
        self.af = af

        self.fig = Figure(figsize=(4, 10))

    def get_record_viz(self,n_mels=128, n_mfcc=40):

        axs = self.fig.subplot_mosaic(
            """
            AAAA
            BBBB
            CCCC
            DDDD
            """
        )

        self.af.get_waveform_plot(ax=axs["A"])

        spectro = self.af.get_spectrogram()
        self.af.plot_spectrogram(spectro[0], title='Spectrogram',ax=axs["B"])


        mel = self.af.get_mel_spectrogram(n_mels=n_mels)
        self.af.plot_spectrogram(mel[0], title='Mel Spectrogram',ax=axs["C"])

        mfcc = self.af.get_mfcc(n_mels=n_mels, n_mfcc=n_mfcc)
        self.af.plot_mfcc(mfcc[0],title='MFCC',ax=axs["D"])

        self.fig.tight_layout()

        return self.af.fig_to_buf(self.fig)