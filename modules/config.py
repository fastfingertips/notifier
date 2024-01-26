class Config:

    history_file_name = 'history.txt'

    sep_char = '<:>'
    line_char = '-'
    pass_char = '#'

    history = True
    loop = True
    
    notifier_duration = 7 # sec
    new_choice_time = 60*5 # sec

class Constants:

    FILE_FORMATS = ('.txt', '.json') # supports
    HISTORY_KEYS = ['h', 'history']
    LOOP_KEYS = ['l', 'loop']