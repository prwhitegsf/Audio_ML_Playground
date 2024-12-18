
#from app.src.DatabaseController import DBControl as dbc

class SessionManager():


    def __init__(self, dbc):
        
        self.dbc = dbc


    def is_new_session(self, sess):
         
        if 'file_list' in sess:
            print('old sess')
            return False
        else:
            print("new_sess")
            return True

    def initialize_session(self, sess):
        if self.is_new_session(sess):
        
            
            sess['filters'] = {'sex'         : 'all', 
                                    'statement'  : 'all',
                                    'emotion'    : 'all',
                                    'intensity'  : 'all',
                                    'num_mels'   : '128',
                                    'num_mfcc'   : '40'
                                    } 
            
            files, ids = self.dbc.get_full_file_list()

            sess['file_list'] = files
            sess['record_count'] = len(sess['file_list'])
            sess['record_num']=0
            sess['fp'] = sess['file_list'][sess['record_num']]
            sess['record_message'] = f'Displaying record {sess['record_num']+1} of {sess['record_count']}'

        

    def set_filters(self, form, sess):

        sess['filters'] = {'sex'         : form.sex.data, 
                            'statement'  : form.statement.data,
                            'emotion'    : form.emotion.data,
                            'intensity'  : form.intensity.data,
                            'num_mels'   : form.mel_filter_count.data,
                            'num_mfcc'   : form.mfcc_count.data}        

    def set_form_data(self,form, sess):

        if 'filters' in sess:
                form.sex.data       = sess['filters']['sex']
                form.statement.data = sess['filters']['statement']
                form.emotion.data   = sess['filters']['emotion']
                form.intensity.data = sess['filters']['intensity']
                
                form.mel_filter_count.data  = sess['filters']['num_mels']
                form.mfcc_count.data        = sess['filters']['num_mfcc']

    def set_file_list(self, sess):
        files, ids = self.dbc.get_filtered_file_list(sess)
        sess['file_list'] = files
        sess['record_count'] = len(sess['file_list'])
        sess['record_num'] = 0
        sess['fp'] = sess['file_list'][0]
        sess['record_message'] = f'Displaying record {sess['record_num']+1} of {sess['record_count']}'


    def get_next_record(self, sess):
        sess['record_num'] += 1

        if sess['record_num'] < sess['record_count']:
            sess['fp'] = sess['file_list'][sess['record_num']]
            sess['record_message'] = f'Displaying record {sess['record_num']+1} of {sess['record_count']}'
        else:
             sess['record_message'] = f'Displaying record {sess['record_count']} of {sess['record_count']}'


    def get_num_mels(self, sess):
        return int(sess['filters']['num_mels'])
    
    def get_num_mfcc(self, sess):
        return int(sess['filters']['num_mfcc'])