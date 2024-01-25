from modules.helpers import (
  ContentHelper,
  ListHelper, 
  ItemHelper
)

from modules import (
  toast,
  os,
)

from modules.errors import InvalidInputError
from datetime import datetime
import pathlib
import random
import time
import sys

class ListNotifier():
    notifier_duration = 7 # 7 sec
    new_choice_time = 60*5 # + notifierDuration
    history_file_name = 'history.txt' #: history file name
    sep_char = ':' #: seperator
    pass_char = '#' #: pass char
    line_char = '-'

    def __init__(self, user_input): 
        self.user_input = user_input
        self._content_type = None
        self._content = None
        self._items = []

    def __str__(self):
        return self.user_input

    @property
    def items(self):
        if not self._items:
            match self.content_type:
                case '.json':
                    self._items = ContentHelper(self.content).get_json_items(self.sep_char)
                case '.txt':
                    self._items = ContentHelper(self.content).get_txt_items()

            if len(self._items):
                print(F'File read successfully! ({len(self._items)} contents)')
                return self._items
            else:
                print('File is empty!')
                exit()

    @property
    def content_type(self):
        if self._content_type is None:
            self._content_type = pathlib.Path(self.user_input).suffix
        return self._content_type

    @property
    def content(self):
        if self._content is None:
            args = {
                'file': self.user_input,
                'mode':  'r',
                'encoding': 'utf-8'
            }
            try:
                match self.content_type:
                    case '.json':
                        self._content = ContentHelper.json_content(args)
                    case '.txt':
                        self._content = ContentHelper.txt_content(args)
                    case _:
                        print('File extension not supported')
            except FileNotFoundError as e:
                raise FileNotFoundError(f'File not found: {e}')
            except Exception as e:
                raise Exception(f'Unexpected error: {e}')
        return self._content

    # -- Setter --

    @content.setter
    def content(self, value):
        self._content = value

    @content_type.setter
    def content_type(self, value):
        self._content_type = value

    @items.setter
    def items(self, value):
        self._items = value
    
    def run_notifier(self, title, description):
        # https://pypi.org/project/win11toast/
        toast(
            title,
            description,
            #selection=['Apple', 'Banana', 'Grape'], button='Submit',
            #on_click='https://www.python.org'
            )
        # self.notifier.show_toast(title, description, duration=self.notifier_duration) # win10toast

    def terminal_printer(self, title, description):
        print(f'{time.strftime("%X")} | {title}: {description}') #: print on terminal

    def runner(self):
        items = ListHelper(self.items) 
        items = items.valid_contents(self.pass_char)
        while True: #: infinite loop
            item = ItemHelper(random.choice(items))
            title, description = item.parse_item(self.sep_char) #: edit content
            self.terminal_printer(title, description) #: print on terminal
            self.write_history(title, description) #: write history
            self.run_notifier(title, description) #: show toast
            time.sleep(self.new_choice_time) #: wait for new choice   

    def write_history(self, title, description):
        mode = 'a' if os.path.exists(self.history_file_name) else 'w'

        with open(self.history_file_name, mode) as hf:
            history_content = ContentHelper.txt_content({'file': self.history_file_name, 'mode':  'r'})
            last_content_date = ContentHelper.get_txt_line(history_content, range=(0, 10))

            if self.line_char*10 != last_content_date:
                if  last_content_date != datetime.now().strftime("%d/%m/%Y"):
                    sep_newday = f'{self.line_char*10} {self.line_char*8} | {self.line_char*19}'
                    print(sep_newday[11:])
                    hf.write(sep_newday+'\n') #: write history

            hf.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {title}: {description}\n')

if __name__ == '__main__':
    try:
        user_input = sys.argv[1]
        if not user_input.endswith(('.txt', '.json')):
            raise InvalidInputError("File format not supported")
    except IndexError:
        user_input = input('Enter list: ')
    except InvalidInputError as e:
        print(f'Invalid input: {e}')
        exit()
    except Exception as e:
        print(f'Unexpected error: {e}')
        exit()

    notifier = ListNotifier(user_input)
    notifier.runner()