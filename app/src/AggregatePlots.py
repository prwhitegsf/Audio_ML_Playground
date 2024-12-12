

from app.src.FeatureExtractors import AudioFeatures as af
from matplotlib.figure import Figure

class PlotAggregator():

    def __init__(self, af):
        self.af = af

        self.fig = Figure(figsize=(5, 10),layout='constrained')

    def get_record_viz(self,n_mels=128, n_mfcc=40):

        axs = self.fig.subplot_mosaic(
            """
            AAAA
            BBBB
            CCCC
            DDDD
            """
        )

        wav = self.af.get_waveform(ax=axs["A"])
        axs["A"].tick_params(axis='y',labelsize=7)
        axs["A"].tick_params(axis='x',labelsize=7)



        spectro = self.af.get_spectrogram()
        specplot = self.af.plot_spectrogram(spectro[0], title='Spectrogram',ax=axs["B"])
        axs["B"].tick_params(axis='y',labelsize=7)
        axs["B"].tick_params(axis='x',labelsize=7)
        axs["B"].set_yticks(ticks=[0,105,210,315,420],
                            labels=[0,5000,10000,15000,20000])
        axs["B"].set_xticks(ticks=[0,50,100,150,200,250,300], 
                            labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
        
        spec_cb = self.fig.colorbar(specplot,format='%+2.0f dB')
        spec_cb.ax.tick_params(axis='y',labelsize=7)

        mel = self.af.get_mel_spectrogram(n_mels=n_mels)
        melplot = self.af.plot_mel(mel[0], title='Mel Spectrogram',ax=axs["C"])
        axs["C"].tick_params(axis='y',labelsize=7)
        axs["C"].tick_params(axis='x',labelsize=7)
        axs["C"].set_yticks(ticks=[0,30,60,90,120],
                            labels=[0,512,1024,2048,4096])
        axs["C"].set_xticks(ticks=[0,50,100,150,200,250,300], 
                            labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
        
        mel_cb = self.fig.colorbar(melplot,format='%+2.0f dB')
        mel_cb.ax.tick_params(axis='y',labelsize=7)

        
        mfcc = self.af.get_mfcc(n_mels=n_mels, n_mfcc=n_mfcc)
        mfccplot = self.af.plot_mfcc(mfcc[0],title='MFCC',ax=axs["D"])
        axs["D"].tick_params(axis='y',labelsize=7)
        axs["D"].tick_params(axis='x',labelsize=7)
        
        axs["D"].set_xticks(ticks=[0,50,100,150,200,250,300], 
                            labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
        
        mfcc_cb = self.fig.colorbar(mfccplot,format='%+2.0f')
        mfcc_cb.ax.tick_params(axis='y',labelsize=7)



        #self.fig.tight_layout()

        return self.af.fig_to_buf(self.fig)