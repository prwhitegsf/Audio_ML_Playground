


class SessionManager():

    def __init__(self, sess):
        self.sess = sess
        # session defaults
          
        
        #self.sess['record_num'] = 0

    def is_new_session(self):
         
        if 'file_list' in self.sess:
            return False
        else:
            return True

    def initialize_session(self, get_files):
        if self.is_new_session():
        
            
            self.sess['filters'] = {'sex'         : 'all', 
                                    'statement'  : 'all',
                                    'emotion'    : 'all',
                                    'intensity'  : 'all',
                                    'num_mels'   : '128',
                                    'num_mfcc'   : '40'
                                    } 
            
            self.sess['file_list'] = get_files
            self.sess['record_count'] = len(self.sess['file_list'])
            self.sess['record_num']=0
            self.sess['fp'] = self.sess['file_list'][self.sess['record_num']]
            self.sess['record_message'] = f'Displaying record {self.sess['record_num']+1} of {self.sess['record_count']}'

        

    def set_filters(self, form):

        self.sess['filters'] = {'sex'         : form.sex.data, 
                                'statement'  : form.statement.data,
                                'emotion'    : form.emotion.data,
                                'intensity'  : form.intensity.data,
                                'num_mels'   : form.mel_filter_count.data,
                                'num_mfcc'   : form.mfcc_count.data}        

    def set_form_data(self,form):

        if 'filters' in self.sess:
                form.sex.data       = self.sess['filters']['sex']
                form.statement.data = self.sess['filters']['statement']
                form.emotion.data   = self.sess['filters']['emotion']
                form.intensity.data = self.sess['filters']['intensity']
                
                form.mel_filter_count.data  = self.sess['filters']['num_mels']
                form.mfcc_count.data        = self.sess['filters']['num_mfcc']

    def set_file_list(self, get_files):
        self.sess['file_list']= get_files
        self.sess['record_count'] = len(self.sess['file_list'])
        self.sess['record_num']=0
        self.sess['fp'] = self.sess['file_list'][0]
        self.sess['record_message'] = f'Displaying record {self.sess['record_num']+1} of {self.sess['record_count']}'


    def get_next_record(self):
        self.sess['record_num'] += 1

        if self.sess['record_num'] < self.sess['record_count']:
            self.sess['fp'] = self.sess['file_list'][self.sess['record_num']]
            self.sess['record_message'] = f'Displaying record {self.sess['record_num']+1} of {self.sess['record_count']}'
        else:
             self.sess['record_message'] = f'Displaying record {self.sess['record_count']} of {self.sess['record_count']}'


    def get_num_mels(self):
        return int(self.sess['filters']['num_mels'])
    
    def get_num_mfcc(self):
        return int(self.sess['filters']['num_mfcc'])