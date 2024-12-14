
fe_filter_form_data = [
    ({'sex'       : 'all', 
    'statement'  : 'all',
    'emotion'    : 'all',
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'sex'       : 'male', 
    'statement'  : 'all',
    'emotion'    : 'all',
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'sex'       : 'male', 
    'statement'  : '1',
    'emotion'    : ['calm','happy','sad'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'sex'       : 'male', 
    'statement'  : '1',
    'emotion'    : ['all','calm','happy','sad'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    })]        

fe_filter_form_least_results = {
    'sex'       : 'female', 
    'statement'  : '1',
    'emotion'    : 'calm',
    'intensity'  : '1',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }