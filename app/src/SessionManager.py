
#from app.src.DatabaseController import DBControl as dbc

class SessionManager():


    def __init__(self, dbc):
        
        self.dbc = dbc
        self.group_size=8


    def is_new_session(self, sess):

        if 'records' in sess:
            print('old sess')
            return False
        else:
            print("new_sess")
            return True
        
    def _reset_curr_record_to_zero(self, sess):
        sess['curr_record'] = {'record_index'   : 0,
                               'group_index'    : 0,
                                'audio_path'    : sess['records'][0][0],
                                'rec_id'        : sess['records'][0][1]}
    
    def _set_visual_message(self, sess,start_index):
        sess["visual_message"] = f'Records {start_index} though {start_index + self.group_size} of {sess['record_count']}'

    
    def init_sess(self, sess,form):
        if self.is_new_session(sess):
            
            sess['filters'] = form.data
           
            sess['records'] = self.dbc.get_all_records()
            sess['record_count'] = len(sess['records'])
            self._reset_curr_record_to_zero(sess)
            if sess['record_count'] > self.group_size:
                sess['record_group_indices'] = list(range(0,self.group_size))
            else:
            # need to flesh out error handling here
                print('not enough records to init')
            
            self._set_visual_message(sess,0)
            sess["audio_message"] = f'Play record {sess['curr_record']['rec_id']}'      
            sess["single_message"] = f'Showing record {1} of {sess['record_count']}'     

            

    def set_filters(self, form, sess):
        sess['filters'] = form.data




    def set_form_data(self,form, sess):
        
        if 'filters' in sess:
                form.sex.data       = sess['filters']['sex']
                form.statement.data = sess['filters']['statement']
                form.emotion.data   = sess['filters']['emotion']
                form.intensity.data = sess['filters']['intensity']
                
                form.num_mels.data  = sess['filters']['num_mels']
                form.num_mfcc.data  = sess['filters']['num_mfcc']


    def set_record_list(self, sess):
        
        sess['records'] = self.dbc.get_filtered_records(sess)
        sess['ids'] = [rec[1] for rec in sess['records']]
        sess['record_count'] = len(sess['records'])
        sess["single_message"] = f'Showing record {1} of {sess['record_count']}' 
        
        # Set initial group
        if sess['record_count'] > self.group_size:
            sess['record_group_indices'] = list(range(0, self.group_size))
            self._reset_curr_record_to_zero(sess)
            self._set_visual_message(sess, 0)
            sess["audio_message"] = f'Play record {sess['curr_record']['rec_id']}' 

       



    def advance_record_group(self, sess):
        
        curr_max_index = sess['record_group_indices'][-1] + 1
     
        
        if curr_max_index + self.group_size <= sess['record_count']:
            sess['record_group_indices'] = list(range(curr_max_index, (curr_max_index + self.group_size)))
            
        else:
            sess['record_group_indices'] = list(range(curr_max_index, sess['record_count']))
        
        sess['curr_record']['group_index'] = 0
        sess['curr_record']['rec_id'] = sess['records'][sess['record_group_indices'][0]][1]
        self._set_visual_message(sess,sess['record_group_indices'][0])
        sess["audio_message"] = f'Play record {sess['curr_record']['rec_id']}' 
    

    def advance_record_within_group(self,sess):

        sess['curr_record']['group_index'] += 1

        # wrap around back to 0 if we've exceeded group size
        if sess['curr_record']['group_index'] >= self.group_size:
            sess['curr_record']['group_index'] = 0

        record_index = sess['record_group_indices'][sess['curr_record']['group_index']]
        id = sess['records'][record_index][1]
        sess["audio_message"] = f'Play record {id}' 


    def get_num_mels(self, sess):
        return int(sess['filters']['num_mels'])
    
    def get_num_mfcc(self, sess):
        return int(sess['filters']['num_mfcc'])
    
    
    def get_next_record(self, sess):
        
        next_rec = sess['curr_record']['record_index'] + 1

        if next_rec < sess['record_count']:
            sess['curr_record']['record_index'] = next_rec
            
        sess["single_message"] = f'Showing record {sess['curr_record']['record_index']+1} of {sess['record_count']}' 