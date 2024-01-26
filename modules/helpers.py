from . import (
    # .errors
    InvalidInputError,
    InvalidSyntax,
    InvalidArg,
    # .config
    Constants,
    Config,
    # built-in
    datetime,
    pathlib,
    time,
    json,
    sys,
    os
)

class List(list):

    def __init__(self, items):
        super().__init__(items)

    def valid_contents(self, _pass='*'):
        # add valid content to new list
        v = [content for content in self if content[0] != _pass]
        print('Valid contents:', len(v))
        return v

    def invalid_contents(self, _pass='*'):
        # add invalid content to new list
        v = [content for content in self if content[0] == _pass]
        print('Invalid contents:', (v))
        return v

class Item(str):

    def __new__(cls, item):
        return super().__new__(cls, item)

    def parse(self, sep_char):
        sep_index = self.find(sep_char)
        if sep_index != -1:
            title, description = map(
                str.strip,
                self.split(Config.sep_char)
                )
            return title, description
        else:
            raise InvalidSyntax('Parsing argumant not found.')

class Input(str):

    def __new__(cls):
        file_name = cls.get_file()
        return super().__new__(cls, file_name)
    
    @staticmethod
    def get_arg(arg=1):
        return sys.argv[arg]
    
    @staticmethod
    def get_args():
        return sys.argv

    @classmethod
    def get_file(cls):
        # feature: file path
        try:
            arg = cls.get_arg(1)
        except IndexError:
            arg = input('Enter list file name: ')
        if not arg.endswith(Constants.FILE_FORMATS):
            raise InvalidInputError("File extension not supported.")
        return arg
    
    @property
    def loop(self):
        try:
            arg = self.get_arg(2)
            if '=' in arg:
                key, arg = arg.split('=')
                if key not in Constants.LOOP_KEYS:
                     raise InvalidArg("Loop key not supported.")
            if arg.lower() == 'true':
                arg = True
            elif arg.lower() == 'false':
                arg = False
            else:
                raise InvalidArg("Loop arg not supported.")
        except IndexError:
            arg = Config.loop
        print('Loop feature:', arg)
        return arg

    @property
    def history(self):
        try:
            arg = self.get_arg(3)
            if '=' in arg:
                key, arg = arg.split('=')
                if key not in Constants.HISTORY_KEYS:
                     raise InvalidArg("History key not supported.")
            if arg.lower() == 'true':
                arg = True
            elif arg.lower() == 'false':
                arg = False
            else:
                raise InvalidArg("History arg not supported.")
        except IndexError:
            arg = Config.history
        print('History feature:', arg)
        return arg

    @property
    def suffix(self):
        return pathlib.Path(self).suffix

class Content:

    def __init__(self, user_input):
        self.user_input = user_input
        self.content_type = self.user_input.suffix
        self._content = None
        self._items = []

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
                        self._content = self.json_content(args)
                    case '.txt':
                        self._content = self.txt_content(args)
                    case _:
                        print('File extension not supported')
            except FileNotFoundError as e:
                raise FileNotFoundError(f'File not found: {e}')

        return self._content

    @property
    def items(self):
        if not self._items:
            match self.content_type:
                case '.json':
                    try: 
                        items = self.content.items()
                    except:
                        raise InvalidSyntax('Invalid .json file data')
                    data = []
                    for title, description in items:
                        data.append(f'{title}{Config.sep_char}{description}')
                    self._items = data 
                case '.txt':
                    self._items = self.content.splitlines()

            if len(self._items):
                print(f'File read successfully! ({len(self._items)} contents)')
                self._items = List(self._items).valid_contents(Config.pass_char)
                return self._items
            else:
                print('File is empty!')
                exit()

    # -- Setter --

    @content.setter
    def content(self, value):
        self._content = value

    @items.setter
    def items(self, value):
        self._items = value

    # -- Static --

    @staticmethod
    def json_content(args):
        return json.load(open(**args))

    @staticmethod
    def txt_content(args):
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xfd in position 323: invalid start byte
        with open(**args) as f:
            return f.read()

    @staticmethod
    def get_txt_line(content, line=-1, range=(0, -1)): 
        try:
            start, end = range
            line = content.splitlines()[line][start:end]
        except IndexError:
            return None
        return line

class Terminal:

    @staticmethod
    def print(title, description):
        print(f'{time.strftime("%X")} | {title}: {description}')

class History:

    @staticmethod
    def add(title, description):
        mode = 'a' if os.path.exists(Config.history_file_name) else 'w'

        with open(Config.history_file_name, mode) as hf:
            history_content = Content.txt_content({
                'file': Config.history_file_name,
                'mode':  'r'
                })
            last_content_date = Content.get_txt_line(
                history_content,
                range=(0, 10)
                )

            if Config.line_char*10 != last_content_date:
                if  last_content_date != datetime.now().strftime("%d/%m/%Y"):
                    sep_newday = f'{Config.line_char*10} {Config.line_char*8} | {Config.line_char*19}'
                    print(sep_newday[11:])
                    hf.write(sep_newday+'\n')

            hf.write(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | {title}: {description}\n')

    def add_to_history(cls, title, description):
        cls.add(title, description)