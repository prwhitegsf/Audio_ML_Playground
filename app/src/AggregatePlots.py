
from matplotlib.figure import Figure

class PlotAggregator():

    def __init__(self, af):
        self.af = af

        self.fig = Figure(figsize=(5, 10),layout='constrained')

    def get_record_viz(self,sess,n_mels=128, n_mfcc=40):
        
        axs = self.fig.subplot_mosaic(
            """
            AAAA
            BBBB
            CCCC
            DDDD
            """
        )

        wav = self.af.plot_waveform(ax=axs["A"])
        axs["A"].tick_params(axis='y',labelsize=7)
        axs["A"].tick_params(axis='x',labelsize=7)



        spectro = self.af.get_spectrogram()
        specplot = self.af.plot_spectrogram(spectro[0], title='Spectrogram',ax=axs["B"])
        axs["B"].tick_params(axis='y',labelsize=7)
        axs["B"].tick_params(axis='x',labelsize=7)
        axs["B"].set_yticks(ticks=[0,200,400,600,800,1000],
                           labels=[0,1600,3200,4800,6400,8000])
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
        #mfcc = self.af.get_mfcc_from_npy(sess)
        mfccplot = self.af.plot_mfcc(mfcc[0],title='MFCC',ax=axs["D"])
        #mfccplot = self.af.plot_mfcc(mfcc,title='MFCC',ax=axs["D"])
        axs["D"].tick_params(axis='y',labelsize=7)
        axs["D"].tick_params(axis='x',labelsize=7)
        
        axs["D"].set_xticks(ticks=[0,50,100,150,200,250,300], 
                            labels=[0,0.5,1.0,1.5,2.0,2.5,3.0])
        
        mfcc_cb = self.fig.colorbar(mfccplot,format='%+2.0f')
        mfcc_cb.ax.tick_params(axis='y',labelsize=7)


        return self.af.fig_to_buf(self.fig)
    

    def get_mfcc_plots_for_label(self, sess):
        
        fig = Figure(figsize=(9, 10),layout='constrained')
        
        mfccs, ids = self.af.get_mfcc_group_from_npy(sess)

        plt_count = len(mfccs)

        axs = fig.subplots(4,2)

        col = 2
        row = 4
        i = 0
        j = 0
        k = 0
        for i in range(col):
            for j in range(row):
                self.af.plot_mfcc(mfccs[k],title=f'mfcc: {ids[k]}',ylabel=None,ax=axs[j,i])
                axs[j,i].set_xticks(ticks=[])
                axs[j,i].set_yticks(ticks=[])
                k+=1
        

        return self.af.fig_to_buf(fig)
