from . import json

class ListHelper(list):
    def __init__(self, items):
        super().__init__(items)

    def valid_contents(self, _pass='*'):
        # add valid content to new list
        return [content for content in self if content[0] != _pass]

    def invalid_contents(self, _pass='*'):
        # add invalid content to new list
        return [content for content in self if content[0] == _pass]
  
class ItemHelper(str):
    def __new__(cls, item):
        return super().__new__(cls, item)

    def parse_item(self, sep_char):
        sep_index = self.find(sep_char)
        if sep_index != -1:
            title = self[:sep_index].strip()
            description = self[sep_index + 1:].strip()
            return title, description
        else:
            return None
        
class ContentHelper:
    def __init__(self, content):
        self.content = content
    
    def get_json_items(self, sep_char):
        data = []
        for title, description in self.content.items():
            data.append(f'{title}{sep_char}{description}')
        return data
    
    def get_txt_items(self):
        return self.content.splitlines()

    @staticmethod
    def json_content(args):
        return json.load(open(**args))

    @staticmethod
    def txt_content(args):
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